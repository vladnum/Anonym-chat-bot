import asyncio
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

async def keyboard(data, message=None):
    if data == 'start':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('Личный кабинет')
        button2 = KeyboardButton('Найти собеседника')
        # button3 = KeyboardButton('Поддержка')
        keyboard.add(button1).add(button2)  # .add(button3)
    
    # В следующих версиях добавить админ панель

    elif data == 'cancel':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('Отменить')
        keyboard.add(button1)
    
    elif data == 'exit':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('Завершить чат')
        keyboard.add(button1)

    return keyboard