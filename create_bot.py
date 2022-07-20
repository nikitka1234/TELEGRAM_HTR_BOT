from aiogram import Bot, Dispatcher
from os import getenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Получаем api_token из Environment Variables
_API_TOKEN = "5470452176:AAHl7PpnuyB5wz15cFkHPntJMqknnMUkNBU"
if not _API_TOKEN:
    exit("Error: no token provided")


# Инициализируем бота и диспетчера
bot = Bot(token=_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
