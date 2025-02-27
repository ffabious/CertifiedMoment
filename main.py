import sys
import asyncio
import logging
import shelve

from aiogram.types import Message, FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

from static.file_paths import (start_message_image_path, chat_message_db_path,
                               chat_language_db_path, chat_settings_db_path,
                               chat_start_db_path)
from static.texts import (start_message_gen_, menu_button_text,
                          settings_button_text, unknown_message_response_text,
                          jojo_reference_text, change_lang_button_text,
                          settings_message_text, lang_change_success_gen_)
from controller import dp, bot


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    user_lang = ''
    with shelve.open(chat_language_db_path) as chat_lang_db:
        if str(message.from_user.id) not in chat_lang_db.keys():
            chat_lang_db[str(message.from_user.id)] = 'en'
        user_lang = chat_lang_db[str(message.from_user.id)]
    
    menu_button = KeyboardButton(text=menu_button_text[user_lang])
    settings_button = KeyboardButton(text=settings_button_text[user_lang])
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
        caption=start_message_gen_(message.from_user.full_name, user_lang),
        reply_markup=regular_markup,
        disable_notification=True
    )

    with shelve.open(chat_start_db_path) as chat_start_db:
        chat_start_db[str(message.from_user.id)] = prev_message.message_id


# Open 'menu' handler
@dp.message(lambda msg: msg.text in menu_button_text.values())
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

# Open 'settings' handler
@dp.message(lambda msg: msg.text in settings_button_text.values())
async def settings_button_handler(message: Message | CallbackQuery):
    user_lang = ''
    with shelve.open(chat_language_db_path) as chat_lang_db:
        user_lang = chat_lang_db[str(message.from_user.id)]

    inline_button = InlineKeyboardButton(
        text=change_lang_button_text[user_lang],
        callback_data="change_lang_callback"
    )
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[[inline_button]])

    # Delete 'settings' message if exists, send new message
    with shelve.open(chat_settings_db_path) as chat_sett_db:
        prev_message_id = chat_sett_db[str(message.from_user.id)]
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=prev_message_id
        )
        prev_message = await message.answer(
            text=settings_message_text[user_lang],
            reply_markup=inline_markup
        )
        chat_sett_db[str(message.from_user.id)] = prev_message.message_id

# Language change handler
@dp.callback_query(lambda c: c.data == 'change_lang_callback')
async def language_change_handler(query: CallbackQuery):

    # Retrieve language chosen by user
    user_lang = ''
    with shelve.open(chat_language_db_path) as chat_lang_db:
        key = str(query.from_user.id)
        if chat_lang_db[key] == "en":
            chat_lang_db[key] = 'ru'
            user_lang = 'ru'
        else:
            chat_lang_db[key] = 'en'
            user_lang = 'en'

    inline_button = InlineKeyboardButton(
        text=change_lang_button_text[user_lang],
        callback_data="change_lang_callback"
    )
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[[inline_button]])
    with shelve.open(chat_settings_db_path) as chat_sett_db:

        # Delete previous 'settings' message
        prev_message_id = chat_sett_db[str(query.from_user.id)]
        await bot.delete_message(
            chat_id=query.from_user.id,
            message_id=prev_message_id
        )

        # Send success message with updated reply markup
        menu_button = KeyboardButton(text=menu_button_text[user_lang])
        settings_button = KeyboardButton(text=settings_button_text[user_lang])
        regular_markup = ReplyKeyboardMarkup(
            keyboard=[[menu_button, settings_button]],
            resize_keyboard=True
        )
        await bot.send_message(
            chat_id=query.from_user.id,
            text=lang_change_success_gen_(user_lang),
            reply_markup=regular_markup
        )

        # Send new 'settings' message and save to chat_sett_db
        prev_message = await bot.send_message(
            chat_id=query.from_user.id,
            text=settings_message_text[user_lang],
            reply_markup=inline_markup
        )
        chat_sett_db[str(query.from_user.id)] = prev_message.message_id


# Reply to a specific message sent by user (this doesn't influence the bot functionality)
@dp.message(lambda msg: 'ramazan' in msg.text.lower() or 'ramzeus' in msg.text.lower())
async def jojo_reference_handler(message: Message):
    await message.answer(text=jojo_reference_text['en'])

# Reply to any message sent by user, which bot doesn't process
@dp.message()
async def unknown_message_handler(message: Message):
    prev_message = await message.answer(text=unknown_message_response_text['en'])
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
