from aiogram import html

def start_message_gen_(user_name: str):
    return f"Hello, {html.bold(user_name)}!\nThis bot was created to help you remember stuff. Don't forget it!"