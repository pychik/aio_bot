from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from main import dp
from utility import fkb, hkb, check_users


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    kb = hkb()
    if await check_users(message):
        kb.add("Настройка 🔧")
    await message.answer("Начнемс! 😉", reply_markup=kb)


@dp.message_handler(Text(equals='Назад в главное меню 👈'))
async def BTMM(message: Message):
    await cmd_start(message)


@dp.message_handler(Text(equals='Техподдержка/Отзывы 🤩'))
async def support(message: Message):
    kb = fkb()
    await message.answer("Ваш выбор..", reply_markup=kb)
