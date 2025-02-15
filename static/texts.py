from aiogram import html

def start_message_gen_(user_name: str):
    end = "Don't forget it!"
    return f"Hello, {html.bold(user_name)}! 👋\nThis bot was created to help you remember stuff.\n{html.italic(end)}"