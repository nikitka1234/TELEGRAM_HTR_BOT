from aiogram import types, Dispatcher
from os import remove
from create_bot import bot
from keyboards import client_kb

from db import add_to_bd
# form object_storage import add_to_os
import settings


# @dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Этот хендлер вызывается когда пользователь отправляет `/start'
    """
    # Добавляем данные пользователя в таблицу
    if not await add_to_bd.is_user_exist(message.from_user.id):
        await add_to_bd.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name,
                                     user_surname=message.from_user.last_name, username=message.from_user.username)

        await message.answer(f"Привет, {message.from_user.first_name}!\nЯ HTR_Bot!")
        await message.answer(settings.HELP_MESSAGE, reply_markup=client_kb)

    await message.answer("Если тебе нужна помощь с ботом используй команду /help")


# @dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    Этот хендлер вызывается когда пользователь отправляет `/help'
    """
    await message.answer(settings.HELP_MESSAGE, reply_markup=client_kb)


# @dp.message_handler(commands=['example'])
async def send_example(message: types.Message):
    """
    Этот хендлер вызывается когда пользователь отправляет `/example'
    """
    await bot.send_photo(message.from_user.id, types.InputFile('tmp\\example\\example.jpg'),
                         caption='Пример работы бота')
    await message.answer("Вы также можете распознать свой текст.\nПросто отправьте боту команду:\n/upload_photo")


# @dp.message_handler(commands=['website'])
async def send_website(message: types.Message):
    """
    Этот хендлер вызывается когда пользователь отправляет `/example'
    """
    await message.answer(settings.WEBSITE_URL)


# @dp.message_handler(content_types=['photo'])
async def download_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await add_to_bd.update_photo_number(user_id=message.from_user.id)

    # photo_number = await add_to_bd.get_photo_number(message.from_user.id)

    await bot.download_file(file_path, f"tmp\\{message.from_user.id}.jpg")

    # await add_to_os.upload_file(object_name=f"tmp\\{message.from_user.id}.jpg", bucket_name=getenv("BUCKET_NAME"),
                                # object_bucket_name=f"{message.from_user.id}/{photo_number}.jpg")

    remove(f"tmp\\{message.from_user.id}.jpg")

    # Убедитесь, что каталог /tmp/somedir существует!
    # Используем индекс [-1], чтобы взять большее по размеру изображение
    # await message.photo[-1].download(destination_dir=f'tmp\\{message.from_user.id}')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_message_handler(send_example, commands=['example'])
    dp.register_message_handler(send_website, commands=['website'])
    dp.register_message_handler(download_photo, content_types=['photo'])
