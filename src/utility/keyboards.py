from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from secrets import choice
from config import settings


# hello keyboard
def hkb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb_buttons = ["Выбрать товар 🛍️", "Техподдержка/Отзывы 🤩"]
    kb.add(*kb_buttons)
    return kb


# choosing what we do with sku
def akb1():
    akb = ReplyKeyboardMarkup(resize_keyboard=True)
    akb.row(KeyboardButton(text="Все товары"), KeyboardButton(text="Добавить товар"),)
    akb.row(KeyboardButton(text="Редактировать товар"), KeyboardButton(text="Удалить товар"))
    akb.row(KeyboardButton(text="Назад в главное меню 👈"))
    return akb


# choosing what we do with sku
def akb2():
    akb = ReplyKeyboardMarkup(resize_keyboard=True)
    akb.row(KeyboardButton(text="Все товары"))
    akb.row(KeyboardButton(text="Добавить товар"), KeyboardButton(text="Удалить товар"))
    akb.row(KeyboardButton(text="Назад 🔙"))
    return akb


# editing sku
def akb3():
    akb = ReplyKeyboardMarkup(resize_keyboard=True)
    akb.row(KeyboardButton(text="Ред. описание"), KeyboardButton(text="Ред. фото"))
    akb.row(KeyboardButton(text="Ред. инструкцию"), KeyboardButton(text="Ред. видео"))
    akb.row(KeyboardButton(text="Отмена 🔙"))
    return akb


# keybord back
def akbb():
    akb = ReplyKeyboardMarkup(resize_keyboard=True)
    akb.row(KeyboardButton(text="Отмена 🔙"))
    return akb


def fkb():
    buttons = [
        InlineKeyboardButton(text="Техническая поддержка", url=settings.TECH_LINK),
        InlineKeyboardButton(text="Бонусы", url=settings.BONUS_LINK)
    ]
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(*buttons)
    return kb


def random_em():
    emojii_list = ['🔎', '👀', '📦', '🔍', '💎']
    return choice(emojii_list)
