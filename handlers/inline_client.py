from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import client_kb
from photo_processing import get_history

import settings


async def inline_send_help(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text=settings.HELP_MESSAGE, reply_markup=client_kb)


async def inline_send_example(callback_query: types.CallbackQuery):
    await bot.send_photo(chat_id=callback_query.from_user.id, photo=types.InputFile('tmp\\example\\example.jpg'),
                         caption='Пример работы бота')
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Вы также можете распознать свой текст.\nПросто отправьте боту фото")


async def inline_send_history(message: types.Message):
    history = await get_history.get_history(tag=f'{message.from_user.id}')

    if "No results" in history.decode('utf-8'):
        await message.answer("Вы еще не отправляли боту фотографий")

    else:
        await bot.send_message(chat_id=message.from_user.id, text=history)


def register_inline_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(inline_send_help, lambda c: c.data == 'help_button')
    dp.register_callback_query_handler(inline_send_example, lambda c: c.data == 'example_button')
    dp.register_callback_query_handler(inline_send_history, lambda c: c.data == 'history_button')
