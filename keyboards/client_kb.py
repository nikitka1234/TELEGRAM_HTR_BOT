from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_example = KeyboardButton('/example')
button_upload = KeyboardButton('/upload_photo')
button_website = KeyboardButton('/website')
button_help = KeyboardButton('/help')

# параматр one_time_keyboard=True прячет клавиатуру после того, как пользователь воспользовался ей один раз
client_kb = ReplyKeyboardMarkup(resize_keyboard=True)
client_kb.add(button_upload).row(button_example, button_website).add(button_help)
