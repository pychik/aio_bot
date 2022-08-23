from aiogram.types import Message
from main import bot
from config import settings


async def check_users(message: Message):
    chat_admins = await bot.get_chat_administrators(settings.GROUP_ID)
    admins = list(map(lambda x: x.user.id, chat_admins))
    if message.from_user.id in admins:
        return True
    else:
        return False
