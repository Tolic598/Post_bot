from aiogram import Dispatcher, types, Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Any, Dict
from aiogram.filters.command import Command
from aiogram.handlers import CallbackQueryHandler
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard.inline import menu, add_text, add_but, del_ph, menu_gotov,menu_menu
import time
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pymysql
from pymysql.cursors import DictCursor
import pymysql.cursors
from config import host, user, password, db_name

from typing import Any, Dict, Optional

from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
start_time = time.time()

dt = datetime.datetime.today().strftime('%d.%m %H:%M')
end_time = (time.time()) - start_time

print((f'Бот запущен\nДата запуска: {dt}\nВремя запуска: {round(end_time,1)} секунды\n'))

try:
    connection = pymysql.connect(host = host,
                                user = user,
                                password = password,
                                database = db_name,
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=DictCursor)
except Exception as ex:
    print(ex)

router = Router()

class statistics(StatesGroup):
    username = State()
    img = State()
    text_1 = State()
    but_1 = State()
    linc_1 = State()

channels_privat = []
photo_privat = []
video_privat = []
text_privat = []
but_privat = []
linc_privat = []
canal_linc = []
text_privat = []
canal_name_post = []
channel_general = []
channel_id = []

# start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, bot):
    id = message.from_user.id
    photo_privat.clear()
    video_privat.clear()
    text_privat.clear()
    but_privat.clear()
    linc_privat.clear()
    canal_linc.clear()
    channel_id.clear()
    await state.clear()
    await message.answer("Добро пожаловать", reply_markup = menu)

# добавить пост
@router.callback_query(F.data == 'add_post')
async def add_post(call: types.CallbackQuery, state: FSMContext, bot):
    if len(canal_name_post) > 0:
        inline_buttons = [InlineKeyboardButton(text = channel, callback_data = f'button_{channel}') for channel in canal_name_post]
        canal = InlineKeyboardMarkup(inline_keyboard=[[button] for button in inline_buttons])
        await call.message.answer(f'Выберете канал из списка:', reply_markup = canal)
        await call.message.delete()
    else:
        await call.message.answer(f'Отправте юзернейм канала c @ или перешлите сообщение с канал:', reply_markup = menu_menu)
        await state.set_state(statistics.username)
        await call.message.delete()

# обработка отправки в канал
@router.callback_query(F.data.contains('button_'))
async def button(call: types.CallbackQuery, state: FSMContext, bot):
    canal_linc.append(call.data[:7])
    await call.message.answer(f'Отправте фото или видео', reply_markup = del_ph)
    await state.set_state(statistics.img)
    await call.message.delete()

# добавления фото
@router.message(F.photo, statistics.img)
async def usename(message: Message, state: FSMContext, bot):
    processed_image = message.photo[-1].file_id
    await state.update_data(img = processed_image)
    await state.set_state(statistics.text_1)
    
    photo_privat.append(processed_image)
    await bot.send_photo(chat_id=message.chat.id, photo=processed_image)
    await message.answer(f"Фотография принята теперь отправьте текст", reply_markup = menu_menu)

# добавления видео
@router.message(F.video, statistics.img)
async def usename_video(message: Message, state: FSMContext, bot):
    video_file_id = message.video.file_id
    video_privat.append(video_file_id)
    await state.update_data(img = video_file_id)
    await state.set_state(statistics.text_1)
    
    await bot.send_video(message.chat.id, video=video_file_id)
    await message.answer(f"Видео принята теперь отправьте текст", reply_markup = menu_menu)

# не добавлять добавления видео или фото
@router.callback_query(F.data == 'del_ph_vi', statistics.img)
async def del_ph_vi(call: types.CallbackQuery, state: FSMContext, bot):
    await call.message.answer(f'Отправте текст', reply_markup = menu_menu)
    await state.set_state(statistics.text_1)
    await call.message.delete()

# добавления текста
@router.message(statistics.text_1)
async def usename_text(message: Message, state: FSMContext, bot):
    text = message.text
    entities = message.entities
    await state.update_data(text=text, entities=entities)
    await message.answer(text = message.text,entities = message.entities, reply_markup = add_text)


# добавления кнопок под текст
@router.callback_query(F.data == 'add_buttons')
async def add_buttons(call: types.CallbackQuery, state: FSMContext, bot):
    await call.message.answer(f'Отправте название кнопки', reply_markup = menu_menu)
    await state.set_state(statistics.but_1)
    await call.message.delete()

# добавления текст кнопки в словарь
@router.message(statistics.but_1)
async def but_1(message: Message, state: FSMContext):
    await state.update_data(but_1 = message.text)
    but_1 = message.text
    await message.answer(f"Вы успешно добавили текст для кнопки: {but_1}")
    but_privat.append(but_1)
    await message.answer(f'Отправьте ссылку для кнопки', reply_markup = menu_menu)
    await state.set_state(statistics.linc_1)

# добавления ссылки кнопки в словарь
@router.message(statistics.linc_1)
async def linc_1(message: Message, state: FSMContext):
    await state.update_data(linc_1 = message.text)
    linc_1 = message.text
    await message.answer(f"Вы успешно добавили ссылку для кнопки: {linc_1}", reply_markup = add_but)
    linc_privat.append(linc_1)

# добавления канала
@router.callback_query(F.data == 'add')
async def add(call: types.CallbackQuery, state: FSMContext, bot):
    await call.message.answer(f'Отправте юзернейм канала c @ или перешлите сообщение с канал:')
    await state.set_state(statistics.username)
    await call.message.delete()

# добавления канала в словарь
@router.message(statistics.username)
async def usename(message: Message, state: FSMContext):
    if message.forward_from_chat:
        a = message.forward_from_chat.id
        title = message.forward_from_chat.title
        await state.update_data(username = a)
        username = a
        channel_id.append(a)
        channels_privat.append(a)
        canal_name_post.append(title)
        await message.answer(f"Вы успешно добавили канал: {title}", reply_markup = menu)
        channel_general.extend(canal_name_post)
        channel_general.extend(channels_privat)
    else:
        await state.update_data(username = message.text)
        username = message.text
        await message.answer(f"Вы успешно добавили канал: {username}", reply_markup = menu)
        channel_id.append(username)
        channels_privat.append(username)
        canal_name_post.append(username)
        channel_general.extend(canal_name_post)
        channel_general.extend(channels_privat)

# Предварительный просмотр
@router.callback_query(F.data == 'look')
async def look(call: types.CallbackQuery, state: FSMContext, bot):
    id = call.from_user.id
    data = await state.get_data()
    text = data['text']
    entities = data['entities']
    if len(photo_privat) > 0:
        if len(but_privat) > 0:
            inl = [InlineKeyboardButton(text = 'Отправить', callback_data="ok")]
            gl_inl = [InlineKeyboardButton(text = 'Главное меню', callback_data="menu")]
            inline_buttons = inl + gl_inl + [InlineKeyboardButton(text = but, url = linc) for linc,but in zip(linc_privat, but_privat)]
            menu_gotovo = InlineKeyboardMarkup(inline_keyboard=[[button] for button in inline_buttons])
            await bot.send_photo(id, photo_privat[0], caption = data['text'], caption_entities = data['entities'], reply_markup = menu_gotovo)
        else:
            await bot.send_photo(id, photo_privat[0], caption = data['text'], caption_entities = data['entities'], reply_markup = menu_gotov)

    elif len(video_privat) > 0:
        if len(but_privat) > 0:
            inl = [InlineKeyboardButton(text = 'Отправить', callback_data="ok")]
            gl_inl = [InlineKeyboardButton(text = 'Главное меню', callback_data="menu")]
            inline_buttons = inl + gl_inl + [InlineKeyboardButton(text = but, url = linc) for linc,but in zip(linc_privat, but_privat)]
            menu_gotovo = InlineKeyboardMarkup(inline_keyboard=[[button] for button in inline_buttons])
            await bot.send_video(id, video_privat[0], caption = data['text'], caption_entities = data['entities'], reply_markup = menu_gotovo)
        else:
            await bot.send_video(id, video_privat[0], caption = data['text'], caption_entities = data['entities'], reply_markup = menu_gotov)

    else:
        if len(but_privat) > 0:
            inl = [InlineKeyboardButton(text = 'Отправить', callback_data="ok")]
            gl_inl = [InlineKeyboardButton(text = 'Главное меню', callback_data="menu")]
            inline_buttons = inl + gl_inl + [InlineKeyboardButton(text = but, url = linc) for linc,but in zip(linc_privat, but_privat)]
            menu_gotovo = InlineKeyboardMarkup(inline_keyboard=[[button] for button in inline_buttons])
            await call.message.answer(text = data['text'], entities = data['entities'], reply_markup = menu_gotovo)
        else:
            await call.message.answer(text = data['text'], entities = data['entities'], reply_markup = menu_gotov)
    await call.message.delete()

# Отправка в канал
@router.callback_query(F.data == 'ok')
async def ok(call: types.CallbackQuery, state: FSMContext, bot):
    data = await state.get_data()
    id = data['username']
    print(id)
    if len(photo_privat) > 0:
        if len(but_privat) > 0:
            inline_buttons = [InlineKeyboardButton(text = but, url = linc) for linc,but in zip(linc_privat, but_privat)]
            menu_gotovo = InlineKeyboardMarkup(inline_keyboard=[[button] for button in inline_buttons])
            await bot.send_photo(id, photo_privat[0], caption = data['text'], caption_entities = data['entities'], reply_markup = menu_gotovo)
            await call.message.answer(f'Успешно отправлено в канал {id}', reply_markup = menu_menu)
        else:
            await bot.send_photo(id, photo_privat[0], caption = data['text'], caption_entities = data['entities'])
            await call.message.answer(f'Успешно отправлено в канал {id}', reply_markup = menu_menu)

    elif len(video_privat) > 0:
        if len(but_privat) > 0:
            inline_buttons = [InlineKeyboardButton(text = but, url = linc) for linc,but in zip(linc_privat, but_privat)]
            menu_gotovo = InlineKeyboardMarkup(inline_keyboard=[[button] for button in inline_buttons])
            await bot.send_video(id, video_privat[0], caption = data['text'], caption_entities = data['entities'], reply_markup = menu_gotovo)
            await call.message.answer(f'Успешно отправлено в канал {id}', reply_markup = menu_menu)
        else:
            await bot.send_video(id, video_privat[0], caption = data['text'], caption_entities = data['entities'])
            await call.message.answer(f'Успешно отправлено в канал {id}', reply_markup = menu_menu)

    else:
        if len(but_privat) > 0:
            inline_buttons = [InlineKeyboardButton(text = but, url = linc) for linc,but in zip(linc_privat, but_privat)]
            menu_gotovo = InlineKeyboardMarkup(inline_keyboard=[[button] for button in inline_buttons])
            await bot.send_message(id, text = data['text'], entities = data['entities'], reply_markup = menu_gotovo)
            await call.message.answer(f'Успешно отправлено в канал {id}', reply_markup = menu_menu)
        else:
            await bot.send_message(id, text = data['text'], entities = data['entities'])
            await call.message.answer(f'Успешно отправлено в канал {id}', reply_markup = menu_menu)
    await call.message.delete()

# Главное меню
@router.callback_query(F.data == 'menu')
async def menu_gl(call: types.CallbackQuery, state: FSMContext, bot):
    await call.message.answer(f'Главное меню', reply_markup = menu)
    await call.message.delete()
    await state.clear()
    photo_privat.clear()
    video_privat.clear()
    text_privat.clear()
    but_privat.clear()
    linc_privat.clear()
    canal_linc.clear()
    channel_id.clear()