from aiogram import types, Dispatcher

from os import remove

from create_bot import bot
from keyboards import client_kb

from photo_processing import send_photo
from photo_processing import get_history
from photo_processing import get_text
from photo_processing import start_processing

from db import add_to_bd
# form object_storage import add_to_os
import settings

import asyncio


async def send_welcome(message: types.Message):
    # Добавляем данные пользователя в таблицу
    if not await add_to_bd.is_user_exist(message.from_user.id):
        await add_to_bd.db_table_val(user_id=message.from_user.id, user_name=message.from_user.first_name,
                                     user_surname=message.from_user.last_name, username=message.from_user.username)

        await message.answer(f"Привет, {message.from_user.first_name}!\n\n"
                             "Бот поможет тебе пеобразовать рукописный текст в печатный\n\n"
                             "Для начала работы просто отправь боту фото с текстом, который нужно преобразовать")
        await message.answer(settings.HELP_MESSAGE, reply_markup=client_kb)

    else:
        await message.answer("Ты уже зарегистрирован\n\n"
                             "Просто загрузи фотографию для начала работы или воспользуйся кнопками ниже",
                             reply_markup=client_kb)


async def send_help(message: types.Message):
    await message.answer(settings.HELP_MESSAGE, reply_markup=client_kb)


async def send_example(message: types.Message):
    await bot.send_photo(message.from_user.id, types.InputFile('tmp/example/example.jpg'),
                         caption='Пример работы бота')

    # await bot.send_photo(message.from_user.id, types.InputFile('tmp\\example\\example.jpg'),
                         # caption='Пример работы бота')

    await message.answer("Вы также можете распознать свой текст.\nПросто отправьте боту фото")


async def send_website(message: types.Message):
    await message.answer(settings.WEBSITE_URL)


async def send_history(message: types.Message):
    history = await get_history.get_history(tag=f'{message.from_user.id}')

    if "No results" in history:
        await message.answer(text="Вы еще не отправляли боту фотографий")

    else:
        await bot.send_message(chat_id=message.from_user.id, text=history)


async def download_photo(message: types.Message):
    msg = await message.answer(text="Ваша фотография успешно загружена.\nНачинается обработка...")

    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await add_to_bd.update_photo_number(user_id=message.from_user.id)

    photo_number = await add_to_bd.get_photo_number(message.from_user.id)

    await bot.download_file(file_path, f"tmp/{message.from_user.id}.jpg")

    file_id = await check_file_id(message=message)

    await send_photo.post_request(file=f"/home/telegram_bot/TELEGRAM_HTR_BOT/tmp/{message.from_user.id}.jpg",
                                  file_id=file_id, tag=f'{message.from_user.id}',
                                  photo_number=photo_number)

    remove(f"tmp/{message.from_user.id}.jpg")

    await asyncio.sleep(2)

    await start_processing.start_processing(file_id=file_id + photo_number)

    text = await get_text.get_text(tag=f'{message.from_user.id}',
                                   name=f'{file_id + photo_number}.jpg')

    await text_for_user(message=message, text=text)

    await msg.delete()

    # await add_to_os.upload_file(object_name=f"tmp\\{message.from_user.id}.jpg", bucket_name=getenv("BUCKET_NAME"),
    # object_bucket_name=f"{message.from_user.id}/{photo_number}.jpg")


async def download_file_photo(message: types.Message):
    if 'jpg' or 'jpeg' or 'png' in message.document.file_name:
        msg = await message.answer(text="Ваша фотография успешно загружена.\nНачинается обработка...")

        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path

        await add_to_bd.update_photo_number(user_id=message.from_user.id)

        photo_number = await add_to_bd.get_photo_number(message.from_user.id)

        await bot.download_file(file_path, f"tmp/{message.from_user.id}."
                                           f"{message.document.file_name.split('.')[-1]}")

        file_id = await check_file_id(message=message)

        await send_photo.post_request(file=f"/home/telegram_bot/TELEGRAM_HTR_BOT/tmp/{message.from_user.id}."
                                           f"{message.document.file_name.split('.')[-1]}",
                                      file_id=file_id, tag=f'{message.from_user.id}',
                                      photo_number=photo_number)

        remove(f"tmp/{message.from_user.id}."
               f"{message.document.file_name.split('.')[-1]}")

        await asyncio.sleep(2)

        await start_processing.start_processing(file_id=file_id + photo_number)

        text = await get_text.get_text(tag=f'{message.from_user.id}',
                                       name=f'{file_id + photo_number}.{message.document.file_name.split(".")[-1]}')

        await text_for_user(message=message, text=text)

        await msg.delete()

        # await add_to_os.upload_file(object_name=f"tmp\\{message.from_user.id}.jpg", bucket_name=getenv("BUCKET_NAME"),
        # object_bucket_name=f"{message.from_user.id}/{photo_number}.jpg")


async def text_for_user(message: types.Message, text: str):
    if len(text) <= 1024:
        await bot.send_message(chat_id=message.from_user.id, text=f"Ваш текст:\n\n{text}")

    else:
        with open(f"tmp/text_file/{message.from_user.id}.txt", 'w', encoding='utf-8') as file:
            file.write(text)

            await bot.send_file(chat_id=message.from_user.id,
                                text="Так как ваш текст превышает количество символов в одном сообщении -"
                                     "мы отправили его вам в виде файла",
                                file=f"tmp/text_file/{message.from_user.id}.txt")

        remove(f"tmp/text_file/{message.from_user.id}.txt")


async def check_file_id(message: types.Message):
    if message.from_user.id > 5:
        result = str(message.from_user.id)[0:6]

        return int(result)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])
    dp.register_message_handler(send_example, commands=['example'])
    dp.register_message_handler(send_website, commands=['website'])
    dp.register_message_handler(send_history, commands=['history'])
    dp.register_message_handler(download_photo, content_types=['photo'])
    dp.register_message_handler(download_file_photo, content_types=['document'])

    dp.register_message_handler(send_help, lambda message: message.text == 'Помощь')
    dp.register_message_handler(send_example, lambda message: message.text == 'Пример')
    dp.register_message_handler(send_website, lambda message: message.text == 'Сайт')
    dp.register_message_handler(send_history, lambda message: message.text == 'История')
