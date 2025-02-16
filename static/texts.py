from aiogram import html

dev_tg_username = "didukyril"

def start_message_gen_(user_name: str):
    start_msg = f"""Hey, {html.bold(user_name)}! 👋
I was created by some chill and (maybe) ADHD guy @{dev_tg_username} to help you (as well as himself) remember stuff.
{html.italic("Don't forget it!")}
"""
    return start_msg

menu_button_text = "📖 Menu"
settings_button_text = "⚙️ Settings"
unknown_message_response_text = "😓 Unfortunately, I don't understand regular messages. Please, use buttons below to interact with me!"
jojo_reference_text = "Oh yeah, this guy named me 😁"