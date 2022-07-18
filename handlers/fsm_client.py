from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from db import add_to_bd
from photo_processing import send_photo
from os import remove


class FSMClient(StatesGroup):
    photo = State()


async def upload_photo(message: types.Message):
    await message.answer("Теперь можете добавить фото, которое хотите обработать.\n\
                         Чтобы отменить загрузку используйте команду /cancel")
    await FSMClient.photo.set()


async def photo_message(message: types.Message, state: FSMContext):
    await message.answer("Ваша фотография успешно загружена.\nНачинается обработка...")
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await add_to_bd.update_photo_number(user_id=message.from_user.id)

    # photo_number = await add_to_bd.get_photo_number(message.from_user.id)

    await bot.download_file(file_path, f"tmp\\{message.from_user.id}.jpg")

    await send_photo.post_request(f"C:\\Users\\mrkim\\PycharmProjects\\HTR_BOT\\tmp\\{message.from_user.id}.jpg",
                                  message.from_user.id)

    # await add_to_os.upload_file(object_name=f"tmp\\{message.from_user.id}.jpg", bucket_name=getenv("BUCKET_NAME"),
                                # object_bucket_name=f"{message.from_user.id}/{photo_number}.jpg")

    remove(f"tmp\\{message.from_user.id}.jpg")

    # Убедитесь, что каталог /tmp/somedir существует!
    # Используем индекс [-1], чтобы взять большее по размеру изображение
    # await message.photo[-1].download(destination_dir=f'tmp\\{message.from_user.id}')
    await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")


def register_handlers_photo(dp: Dispatcher):
    dp.register_message_handler(upload_photo, commands="upload_photo", state="*")
    dp.register_message_handler(photo_message, content_types=['photo'], state=FSMClient.photo)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
