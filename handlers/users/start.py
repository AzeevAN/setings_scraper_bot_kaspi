from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import ADMINS
from loader import dp
from utils.db_api.ftp_connect import return_brands_ftp

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
