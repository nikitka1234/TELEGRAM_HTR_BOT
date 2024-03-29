from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher
from create_bot import bot
from photo_processing import get_history
from photo_processing import get_text


# async def prev_page(call: types.CallbackQuery):
#     await call.answer()
#     data = int(call.data.split(":")[1]) - 1
#     list_len = int(call.data.split(":")[2])
#     history_list = call.data.split(":")[3].lstrip('[').rstrip(']').split(', ')
#
#     if data <= -1:
#         return None
#
#     markup = InlineKeyboardMarkup().add(
#         InlineKeyboardButton("PREV", callback_data=f"prev:{data}:{list_len}:{history_list}"),
#         InlineKeyboardButton(str(data), callback_data="null"),
#         InlineKeyboardButton("NEXT", callback_data=f"next:{data}:{list_len}:{history_list}"),
#     )
#     await call.message.edit_media(media=types.InputMediaPhoto(open(history_list[data].strip('"'), 'rb')), reply_markup=markup)
#
#
# async def next_page(call: types.CallbackQuery):
#     await call.answer()
#     data = int(call.data.split(":")[1]) + 1
#     list_len = int(call.data.split(":")[2])
#     history_list = call.data.split(":")[3].lstrip('[').rstrip(']').split(', ')
#
#     if data >= list_len:
#         return None
#
#     markup = InlineKeyboardMarkup().add(
#         InlineKeyboardButton("PREV", callback_data=f"prev:{data}:{list_len}:{history_list}"),
#         InlineKeyboardButton(str(data), callback_data="null"),
#         InlineKeyboardButton("NEXT", callback_data=f"next:{data}:{list_len}:{history_list}"),
#     )
#     await call.message.edit_media(media=types.InputMediaPhoto(open(history_list[data].strip('"'), 'rb')), reply_markup=markup)
#
#
# async def handler(message: types.Message):
#     history = await get_history.get_history(tag=f'{message.from_user.id}')
#
#     if "No results" in history:
#         await message.answer("Вы еще не отправляли боту фотографий")
#
#     else:
#         for x in range(0, len(history)):
#             history[x] = '/home/api/Site_back_dev/uploaded_files/' + history[x].strip('"')
#
#     markup = InlineKeyboardMarkup().add(
#         InlineKeyboardButton("0", callback_data="null"),
#         InlineKeyboardButton("NEXT", callback_data=f"next:0:{len(history)}:{history}")
#     )
#     await message.answer_photo(open(history[0].strip('"'), 'rb'), reply_markup=markup)
#
#
# def register_history_kb(dp: Dispatcher):
#     dp.register_message_handler(handler, commands=['history_kb'])
#     dp.register_callback_query_handler(next_page, lambda c: c.data.startswith("next"))
#     dp.register_callback_query_handler(prev_page, lambda c: c.data.startswith("prev"))

async def prev_page(call: types.CallbackQuery):
    history = await get_history.get_history(tag=f'{call.from_user.id}')

    data = int(call.data.split(":")[1]) - 1

    # text = await get_text.get_text(tag=f'{call.from_user.id}', name=history[data-1].strip('"'))

    for x in range(0, len(history)):
        history[x] = '/home/api_new/Site_back_dev/uploaded_files/' + history[x].strip('"')
    await call.answer()

    if data <= 0:
        return None

    if data == 1:
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton(str(data) + "/" + str(len(history)), callback_data="null"),
            InlineKeyboardButton("NEXT", callback_data=f"next:{data}"),
        )
        await call.message.edit_media(media=types.InputMediaPhoto(open(history[data-1].strip('"'), 'rb')),
                                      reply_markup=markup)

    else:
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("PREV", callback_data=f"prev:{data}"),
            InlineKeyboardButton(str(data)+"/"+str(len(history)), callback_data="null"),
            InlineKeyboardButton("NEXT", callback_data=f"next:{data}"),
        )
        await call.message.edit_media(media=types.InputMediaPhoto(open(history[data-1].strip('"'), 'rb')),
                                      reply_markup=markup)


async def next_page(call: types.CallbackQuery):
    history = await get_history.get_history(tag=f'{call.from_user.id}')

    data = int(call.data.split(":")[1]) + 1

    # text = await get_text.get_text(tag=f'{call.from_user.id}', name=history[data-1].strip('"'))

    for x in range(0, len(history)):
        history[x] = '/home/api_new/Site_back_dev/uploaded_files/' + history[x].strip('"')
    await call.answer()

    if data > len(history):
        return None

    if data == len(history):
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("PREV", callback_data=f"prev:{data}"),
            InlineKeyboardButton(str(data) + "/" + str(len(history)), callback_data="null"),
        )
        await call.message.edit_media(media=types.InputMediaPhoto(open(history[data-1].strip('"'), 'rb')),
                                      reply_markup=markup)

    else:
        markup = InlineKeyboardMarkup().add(
            InlineKeyboardButton("PREV", callback_data=f"prev:{data}"),
            InlineKeyboardButton(str(data)+"/"+str(len(history)), callback_data="null"),
            InlineKeyboardButton("NEXT", callback_data=f"next:{data}"),
        )
        await call.message.edit_media(media=types.InputMediaPhoto(open(history[data-1].strip('"'), 'rb')),
                                      reply_markup=markup)



async def handler(call: types.CallbackQuery):
    history = await get_history.get_history(tag=f'{call.from_user.id}')

    # text = await get_text.get_text(tag=f'{call.from_user.id}', name=history[0].strip('"'))

    if "No results" in history:
        await call.answer("Вы еще не отправляли боту фотографий")
        return

    else:
        for x in range(0, len(history)):
            history[x] = '/home/api_new/Site_back_dev/uploaded_files/' + history[x].strip('"')

    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f"1/{len(history)}", callback_data="null"),
        InlineKeyboardButton("NEXT", callback_data=f"next:1")
    )

    await call.message.answer_photo(open(history[0].strip('"'), 'rb'), reply_markup=markup)

    await call.answer(cache_time=1)


def register_history_kb(dp: Dispatcher):
    # dp.register_message_handler(handler, commands=['history_kb'])
    dp.register_callback_query_handler(next_page, lambda c: c.data.startswith("next"))
    dp.register_callback_query_handler(prev_page, lambda c: c.data.startswith("prev"))

    dp.register_callback_query_handler(handler, lambda c: c.data == 'history_button')
