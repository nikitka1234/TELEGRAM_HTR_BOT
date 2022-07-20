from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher
from create_bot import bot
from photo_processing import get_history


async def prev_page(call: types.CallbackQuery):
    await call.answer()
    data = int(call.data.split(":")[1]) - 1
    list_len = int(call.data.split(":")[2])
    history_list = call.data.split(":")[3].lstrip('[').rstrip(']').split(', ')

    if data <= -1:
        return None

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("PREV", callback_data=f"prev:{data}:{list_len}:{history_list}"),
        InlineKeyboardButton(str(data), callback_data="null"),
        InlineKeyboardButton("NEXT", callback_data=f"next:{data}:{list_len}:{history_list}"),
    )
    await call.message.edit_media(media=types.InputMediaPhoto(open(history_list[data], 'rb')), reply_markup=markup)


async def next_page(call: types.CallbackQuery):
    await call.answer()
    data = int(call.data.split(":")[1]) + 1
    list_len = int(call.data.split(":")[2])
    history_list = call.data.split(":")[3].lstrip('[').rstrip(']').split(', ')

    if data >= list_len:
        return None

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("PREV", callback_data=f"prev:{data}:{list_len}:{history_list}"),
        InlineKeyboardButton(str(data), callback_data="null"),
        InlineKeyboardButton("NEXT", callback_data=f"next:{data}:{list_len}:{history_list}"),
    )
    await call.message.edit_media(media=types.InputMediaPhoto(open(history_list[data], 'rb')), reply_markup=markup)


async def handler(message: types.Message):
    history = await get_history.get_history(tag=f'{message.from_user.id}')

    if "No results" in history:
        await message.answer("Вы еще не отправляли боту фотографий")

    else:
        for x in range(0, len(history)):
            history[x] = '/home/api/Site_back_dev/uploaded_files/' + history[x].strip('"')

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("0", callback_data="null"),
        InlineKeyboardButton("NEXT", callback_data=f"next:0:{len(history)}:{history}")
    )
    await message.answer_photo(open(history[0], 'rb'), reply_markup=markup)


def register_history_kb(dp: Dispatcher):
    dp.register_message_handler(handler, commands=['history_kb'])
    dp.register_callback_query_handler(next_page, lambda c: c.data.startswith("next"))
    dp.register_callback_query_handler(prev_page, lambda c: c.data.startswith("prev"))

