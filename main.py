import sys
import asyncio
import logging
import shelve

from aiogram.types import Message, FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

from static.file_paths import start_message_image_path, chat_message_db_path
from static.texts import start_message_gen_, menu_button_text, settings_button_text
from static.texts import unknown_message_response_text, jojo_reference_text
from controller import dp, bot


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    menu_button = KeyboardButton(text=menu_button_text)
    settings_button = KeyboardButton(text=settings_button_text)
    regular_markup = ReplyKeyboardMarkup(
        keyboard=[[menu_button, settings_button]],
        resize_keyboard=True
    )
    start_photo = FSInputFile(
        path=start_message_image_path,
        filename="start_image.jpeg"
    )
    prev_message = await message.answer_photo(
        photo=start_photo,
        caption=start_message_gen_(message.from_user.full_name),
        reply_markup=regular_markup
    )

    with shelve.open(chat_message_db_path) as chat_msg_db:
        chat_msg_db[str(message.from_user.id)] = prev_message.message_id


# User chose to open menu
@dp.message(lambda msg: msg.text == menu_button_text)
async def menu_button_handler(message: Message):
    inline_button = InlineKeyboardButton(
        text="Basic Menu Button",
        callback_data="inline_menu_callback"
    )
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[[inline_button]])
    await message.answer(
        text="This is a basic menu message",
        reply_markup=inline_markup,
    )

@dp.message(lambda msg: msg.text == settings_button_text)
async def settings_button_handler(message: Message):
    inline_button = InlineKeyboardButton(
        text="Basic Settings Button",
        callback_data="settings_inline_callback"
    )
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[[inline_button]])
    await message.answer(
        text="This is a basic settings message",
        reply_markup=inline_markup
    )

# Handler for a reference I wanted to add (this doesn't influence the bot functionality)
@dp.message(lambda msg: 'ramazan' in msg.text.lower() or 'ramzeus' in msg.text.lower())
async def jojo_reference_handler(message: Message):
    await message.answer(text=jojo_reference_text)

# To handle random messages which aren't connected to the functionality of the bot
@dp.message()
async def unknown_message_handler(message: Message):
    prev_message = await message.answer(text=unknown_message_response_text)
    with shelve.open(chat_message_db_path) as chat_msg_db:
        if str(prev_message.from_user.id) in list(chat_msg_db.keys()):
            await bot.delete_message(
                chat_id=message.from_user.id,
                message_id=chat_msg_db[str(prev_message.from_user.id)]
            )
        chat_msg_db[str(prev_message.from_user.id)] = prev_message.message_id


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
