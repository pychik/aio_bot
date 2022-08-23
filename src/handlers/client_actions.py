from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,\
                        KeyboardButton, Message, ReplyKeyboardMarkup

from main import dp
from utility import  check_users, hkb, random_em
from states import ClientDialog
from storages import cur


@dp.message_handler(Text(equals="Выбрать товар 🛍️"))
async def cmd_link(message: Message):
    cur.execute("SELECT name FROM products")
    product_obj = cur.fetchall()
    products = list(map(lambda x: x[0], product_obj))
    buttons = [KeyboardButton(text=f"{p} {random_em()}") for p in products]
    kb = ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    kb.add(*buttons)
    kb.add("Отмена 🔙")
    await ClientDialog.client_choose.set()
    await message.answer("Выберите товар из предложенных в <b>меню</b>", reply_markup=kb, )


@dp.message_handler(state=ClientDialog.client_choose)
async def process_vpr_1(message: Message, state: FSMContext):
    kb = hkb()
    if await check_users(message):
        kb.add("Настройка 🔧")
    if message.text == 'Отмена 🔙':
        await message.answer('Действие отменено.\n<b>Главное меню</b>', reply_markup=kb)
        await state.finish()
    else:
        cur.execute("SELECT name FROM products")
        product_obj = cur.fetchall()
        products = list(map(lambda x: x[0], product_obj))
        p = message.text[:-2]
        if p not in products:
            await state.finish()
            await message.answer("Обнаружена странная активность", reply_markup=kb)
        else:

            cur.execute(f"SELECT description, photo_id FROM products WHERE name='{p}'")
            data = cur.fetchone()
            ikb = InlineKeyboardMarkup()
            ikb.row(InlineKeyboardButton(text="Инструкция", callback_data="call_instruction"),
                    InlineKeyboardButton(text="Видео", callback_data="call_product_video"))
            ikb.row(InlineKeyboardButton(text="Вернуться к просмотру товаров", callback_data="call_view_products"))

            await state.finish()
            await message.answer_photo(photo=data[1], caption=f'<b>{p}</b>\n<i>Описание</i>: {data[0][:900]}', reply_markup=ikb)
            # await message.answer(text=f'Описание: {data[0]}', reply_markup=ikb)


@dp.callback_query_handler(text="call_instruction", )
async def products_instr(call: CallbackQuery, ):
    ikb = InlineKeyboardMarkup()
    ikb.row(InlineKeyboardButton(text="Вернуться к просмотру товаров", callback_data="call_view_products"))
    p = call.message.caption.split('\n')[0]
    cur.execute(f"SELECT file_id FROM products WHERE name='{p}'")
    data = cur.fetchone()[0]
    await call.message.answer_document(document=data, caption="<b>Инструкция</b> по эксплуатации", reply_markup=ikb)


@dp.callback_query_handler(text="call_product_video", )
async def products_video(call: CallbackQuery,):
    ikb = InlineKeyboardMarkup()
    ikb.row(InlineKeyboardButton(text="Вернуться к просмотру товаров", callback_data="call_view_products"))
    p = call.message.caption.split('\n')[0]
    cur.execute(f"SELECT video_id FROM products WHERE name='{p}'")
    data = cur.fetchone()[0]
    await call.message.answer_video(video=data, caption="<b>Видеообзор</>", reply_markup=ikb)


@dp.callback_query_handler(text="call_view_products")
async def all_products(call: CallbackQuery):
    await cmd_link(message=call.message)

