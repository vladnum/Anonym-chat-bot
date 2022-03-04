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

@dp.message_handler('start')
async def asd():
    pass