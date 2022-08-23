from functools import wraps

from .keyboards import akb1, hkb
from config import settings
from main import bot

# def user_check(func):
#     @wraps(func)
#     async def wrap(message, *args, **kwargs):
#         cur.execute(f"SELECT COUNT(*) FROM admins WHERE username='{message.from_user.username}'")
#         d = cur.fetchone()[0]
#         if d == 0:
#             kb = hkb()
#             await message.answer('Ты не администратор!', reply_markup=kb)
#         else:
#             return await func(message, *args, **kwargs)
#     return wrap


def user_check(func):
    @wraps(func)
    async def wrap(message, *args, **kwargs):

        chat_admins = await bot.get_chat_administrators(settings.GROUP_ID)
        admins = list(map(lambda x: x.user.id, chat_admins))
        if message.from_user.id not in admins:
            kb = hkb()
            await message.answer('Ты не администратор!', reply_markup=kb)
        else:
            return await func(message, *args, **kwargs)
    return wrap