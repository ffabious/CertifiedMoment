from aiogram import html

dev_tg_username = "didukyril"

def start_message_gen_(user_name: str, user_lang: str):
    if user_lang == 'en':
        start_msg = f"""Hey, {html.bold(user_name)}! 👋
I was created by some chill and (maybe) ADHD guy @{dev_tg_username} to help you (as well as himself) remember stuff.
{html.italic("Don't forget it!")}
"""
        return start_msg
    start_msg = f"""Привет, {html.bold(user_name)}! 👋
Меня создал один чилловый и (вероятно) СДВГ парень @{dev_tg_username}, чтобы помочь тебе (и себе самому) запоминать события.
{html.italic("Не забывай об этом!")}
"""
    return start_msg

def lang_change_success_gen_(lang: str):
    message = f"""{lang_change_success_text[lang]}

    - {html.italic(language_text[lang])}
"""
    return message

# Button texts
menu_button_text = {
    'en': "📖 Menu",
    'ru': "📖 Меню"
}
settings_button_text = {
    'en': "⚙️ Settings",
    'ru': "⚙️ Настройки"
}

language_text = {
    'en': '🇺🇸 English',
    'ru': '🇷🇺 Русский'
}

change_lang_button_text = {
    'en': 'Change Bot Language to: ' + language_text['ru'],
    'ru': 'Изменить язык бота на: ' + language_text['en']
}

lang_change_success_text = {
    'en': 'Language has been successfully changed to:',
    'ru': 'Язык был успешно изменен на:'
}

settings_message_text = {
    'en': f'''
{html.bold(settings_button_text["en"])}

Here you can:

    - {change_lang_button_text['en']}.
    
👇 Choose desired options below.''',
    'ru': f'''
{html.bold(settings_button_text["ru"])}

Здесь ты можешь:

    - {change_lang_button_text['ru']}.
    
👇 Выбирай желаемые функции ниже.'''
}

# Response texts
unknown_message_response_text = {
    'en': "😓 Unfortunately, I don't understand regular messages. Please, use buttons below to interact with me!",
    'ru': "😓 К сожалению, я не понимаю обычные сообщения. Пожалуйста, используй кнопки снизу для взаимодействия со мной!"
}
jojo_reference_text = {
    'en': "😁 Oh yeah, this guy named me.",
    'ru': "😁 Ага, этот чел придумал мне имя."
}

