import sys
import asyncio
import logging
import shelve

from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from static.file_paths import start_message_image_path, chat_message_db_path
from static.texts import start_message_gen_
from controller import dp, bot


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    photo = FSInputFile(path=start_message_image_path, filename="start_image.jpeg")
    prev_message = await message.answer_photo(caption=start_message_gen_(message.from_user.full_name), photo=photo)
    with shelve.open(chat_message_db_path) as chat_msg_db:
        chat_msg_db[str(prev_message.chat.id)] = prev_message.message_id
    

@dp.message()
async def echo_handler(message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.edit_message_caption()
    with shelve.open(chat_message_db_path) as chat_msg_db:
        if str(message.chat.id) in list(chat_msg_db.keys()):
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=chat_msg_db[str(message.chat.id)]
            )
    try:
        prev_message = await message.send_copy(chat_id=message.chat.id)
        with shelve.open(chat_message_db_path) as chat_msg_db:
            chat_msg_db[str(prev_message.chat.id)] = prev_message.message_id
    except TypeError:
        prev_message = await message.answer("Nice try!")
        with shelve.open(chat_message_db_path) as chat_msg_db:
            chat_msg_db[str(prev_message.chat.id)] = prev_message.message_id

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
