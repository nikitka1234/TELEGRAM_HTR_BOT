from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from settings import WEBSITE_URL

button_history = InlineKeyboardButton('История обработок', callback_data='history_button')
button_example = InlineKeyboardButton('Пример', callback_data='example_button')
button_website = InlineKeyboardButton('Сайт', url=WEBSITE_URL)
button_help = InlineKeyboardButton('Помощь', callback_data='help_button')

# параматр one_time_keyboard=True прячет клавиатуру после того, как пользователь воспользовался ей один раз
client_kb = InlineKeyboardMarkup(resize_keyboard=True)
client_kb.add(button_history).row(button_example, button_website).add(button_help)
