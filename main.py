import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatType
from sqlite import SQLite
from buttons import keyboard
from vars import *

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)

db = SQLite('database.db')

sub_keyboard = types.InlineKeyboardMarkup()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if db.get_user_in_base(message.from_user.id) is None:
        db.add_user_in_base(message.from_user.id, message.from_user.name)
        await message.answer('Вы зарегестрированы', reply_markup=await keyboard('start'))
    else:
        await message.answer('Главное меню', reply_markup=await keyboard('start'))

@dp.message_handler(commands=['queue'])
async def start_search(message: types.Message):
    if db.get_user_in_queue(message.from_user.id) is None:
        check_user_in_room = db.get_user_in_room(message.from_user.id)
        if check_user_in_room[0] is None and check_user_in_room[1] is None:
            db.add_user_in_queue(message.from_user.id)
            await message.answer('B поиске', reply_markup=await keyboard('cancel'))
        else:
            await message.answer('Вы уже общаетесь')
    else:
        await message.answer('Вы уже в поиске')