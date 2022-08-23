from main import dp
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from utility import akb1, akb2, akbb, hkb, user_check


@dp.message_handler(Text(equals='Настройка 🔧'))
@user_check
async def admin_control(message: Message):
    kb = akb1()
    await message.answer(f'Добро пожаловать в Админ-Панель <b><i>{message.from_user.username}!</i></b>\n'
                         f'Выберите действие', reply_markup=kb)


