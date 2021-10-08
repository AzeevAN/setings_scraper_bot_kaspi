from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS
from loader import dp
from states.state import StateBrands
from utils.db_api.ftp_connect import return_brands_ftp, add_brand_name_in_bd, delete_brand_in_bd

callback_brands = CallbackData('brands', 'action', 'name')


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@dp.message_handler(commands=['brands'])
async def send_start(message: types.Message):

    if str(message.from_user.id) in ADMINS:
        await message.answer(text='Список брендов',
                             reply_markup=select_reply_markup_brands())


def select_reply_markup_brands():
    button = InlineKeyboardMarkup(row_width=1)
    list_brands = return_brands_ftp(False)
    if list_brands is not None:
        for brand in list_brands:
            button.insert(InlineKeyboardButton(f'DEL ➖ {brand}  ➖',
                                               callback_data=callback_brands.new(
                                                   action='DELL', name=f'{brand}'
                                               )))
    button.insert(InlineKeyboardButton('➕ Добавить ➕',
                                       callback_data=callback_brands.new(
                                           action='ADD', name='NEW'
                                       )))
    return button


@dp.callback_query_handler(callback_brands.filter(), state=None)
async def answer(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=15)

    action = callback_data['action']
    name = callback_data['name']
    text_message = 'Error'
    reply_markup = None
    if action == 'DELL':
        text_message = f'Из кантроля удален бренд {name}'
        delete_brand_in_bd(name)
        reply_markup = select_reply_markup_brands()
        # Удаление из базы отслеживаемого бренда
    elif action == 'ADD':
        text_message = 'Напишите наименование бренда,\n как он указан на сайте'
        await StateBrands.next()
    await call.message.edit_text(text=text_message,
                                 reply_markup=reply_markup
                                 )


@dp.message_handler(state=StateBrands.name)
async def answer(message: types.Message, state: FSMContext):
    name = message.text
    # await state.update_data(name=name)
    await state.finish()
    add_brand_name_in_bd(name)
    await message.answer(f"Бренд {name} добавлен", reply_markup=select_reply_markup_brands())

