from aiogram import Bot, Dispatcher
from os import getenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Получаем api_token из Environment Variables
_API_TOKEN = getenv("API_TOKEN")
if not _API_TOKEN:
    exit("Error: no token provided")

storage = MemoryStorage()

# Инициализируем бота и диспетчера
bot = Bot(token=_API_TOKEN)
dp = Dispatcher(bot, storage=storage)
