import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatType, InlineKeyboardButton, InlineKeyboardMarkup
from sqlite import SQLite
from buttons import keyboard
from vars import *

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)

db = SQLite()

list_skipped_text = ['Найти собеседника', 'Отменить', 'Написать в поддержку', 'Завершить чат']

sup_keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = InlineKeyboardButton('Написать в поддержку', url='http://t.me/vdlikk')
sup_keyboard.add(button)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if db.get_user_in_base(message.from_user.id) is None:
        db.add_user_in_base(message.from_user.id, message.from_user.username)
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


@dp.message_handler(commands=['exit'])
async def queue_exit(message: types.Message):
    if db.get_user_in_queue(message.from_user.id) is None:
        await message.answer('Вы не в поиске')
    else:
        user_in_room_check = db.get_user_in_room(message.from_user.id)
        if user_in_room_check[0] is None and user_in_room_check[1] is None:
            db.delete_user_from_queue(message.from_user.id)
            await message.answer('Вы были удалены из поиска', reply_markup=await keyboard('start'))
        else:
            await message.answer('Вы уже общаетесь')


@dp.message_handler(commands=['stop'])
async def stop_chat(message: types.Message):
    room_id = db.get_user_id_room(message.from_user.id)
    if room_id is not None:
        room_mate_id = db.get_room_mate_id(room_id[0], message.from_user.id)
        db.delete_room(room_id[0])
        await bot.send_message(room_mate_id, 'Собеседник завершил беседу', reply_markup=await keyboard('start'))
        await message.answer('Вы завершили беседу', reply_markup=await keyboard('start'))
    else:
        await message.answer('Вы ни с кем не общаетесь')


@dp.message_handler(chat_type=ChatType.PRIVATE, content_types=['text', 'video', 'sticker', 'audio', 'game', 'voice', 'photo', 'animation', 'dice', 'video_note'])
async def get_text(message: types.Message):
    if message.text == 'Найти собеседника':
        await start_search(message)
    elif message.text == 'Отменить':
        await queue_exit(message)
    elif message.text == 'Завершить чат':
        await stop_chat(message)
    elif message.text == 'Написать в поддержку':
        await message.answer('Ведутся технические работы, проект на этапе бета-теста')

    room_id = db.get_user_id_room(message.from_user.id)
    if room_id is not None:
        if message.text in list_skipped_text:
            pass
        else:
            room_mate_id = db.get_room_mate_id(room_id[0], message.from_user.id)
            if message.text:
                await bot.send_message(room_mate_id, f'{message.text}')
            elif message.video:
                await bot.send_video(room_mate_id, message.video.file_id)
            elif message.sticker:
                await bot.send_sticker(room_mate_id, message.sticker.file_id)
            elif message.audio:
                await bot.send_audio(room_mate_id, message.audio.file_id)
            elif message.voice:
                await bot.send_voice(room_mate_id, message.voice.file_id)
            elif message.photo:
                await bot.send_photo(room_mate_id, message.photo[-1].file_id)
            elif message.video_note:
                await bot.send_video_note(room_mate_id, message.video_note.file_id)
            elif message.animation:
                await bot.send_animation(room_mate_id, message.animation.file_id)


async def connect_users():
    queue = db.get_queue()
    if queue is None:
        pass
    elif len(queue) >= 2:
        users_id = [queue[0][0], queue[1][0]]
        db.delete_user_from_queue(users_id[0])
        db.delete_user_from_queue(users_id[1])
        await bot.send_message(users_id[0], 'Собеседник найден!', reply_markup=await keyboard('exit'))
        await bot.send_message(users_id[1], 'Собеседник найден!', reply_markup=await keyboard('exit'))
        rooms = len(db.get_count_rooms())
        room_id = 0 if rooms is None else rooms+1
        db.add_new_room(room_id, users_id[0], users_id[1])
    else:
        pass


def repeat_connect_users(coro, lp):
    asyncio.ensure_future(coro(), loop=lp)
    loop.call_later(1, repeat_connect_users, coro, lp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(5, repeat_connect_users, connect_users, loop)
    executor.start_polling(dp, skip_updates=True)
