from main import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from states import ProductEdit, ProductRemove
from storages import cur, conn
from utility import akb1, akbb, hkb, user_check


@dp.message_handler(Text(equals='Все товары'))
@user_check
async def view_pr(message: Message):
    kb = akb1()
    cur.execute("SELECT name FROM products")
    products = cur.fetchall()
    pr = ',\n'.join(list(map(lambda x: x[0], products)))
    await message.answer(f'Найдены товары:\n{pr}', reply_markup=kb)

@dp.message_handler(Text(equals='Добавить товар'))
@user_check
async def add_pr(message: Message):
    await ProductEdit.add_product.set()
    kb = akbb()
    await message.answer('Введите название нового товара (например стринги женские)', reply_markup=kb)


@dp.message_handler(state=ProductEdit.add_product)
async def process_pr_1(message: Message, state: FSMContext):
    if message.text == 'Отмена 🔙':
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        kb = akbb()
        await ProductEdit.next()
        await message.answer(f'Введите описание', reply_markup=kb)


@dp.message_handler(state=ProductEdit.add_description)
async def process_pr_2(message: Message, state: FSMContext):
    if message.text == 'Отмена 🔙':
        kb = akb1()
        await message.answer('Меню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['description'] = message.text
        kb = akbb()
        await ProductEdit.next()
        await message.answer(f'Загрузите фото', reply_markup=kb)


@dp.message_handler(content_types=['photo'], state=ProductEdit.add_photo)
async def process_pr_3(message: Message, state: FSMContext):
    if message.text == 'Отмена 🔙':
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        kb = akbb()
        await ProductEdit.next()
        await message.answer(f'Добавьте файл с инструкцией', reply_markup=kb)


@dp.message_handler(content_types=['document'], state=ProductEdit.add_file)
async def process_pr_4(message: Message, state: FSMContext):
    if message.text == 'Отмена 🔙':
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['file'] = message.document.file_id
        kb = akbb()
        await ProductEdit.next()
        await message.answer(f'Добавьте видео', reply_markup=kb)


@dp.message_handler(content_types=['video'], state=ProductEdit.add_video)
async def process_pr_5(message: Message, state: FSMContext):
    if message.text == 'Отмена 🔙':
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['video'] = message.video.file_id
        kb = akb1()
        async with state.proxy() as data:
            cur.execute(f"""INSERT INTO products(name, description, photo_id, file_id, video_id)
                                                        VALUES('{data['name']}', '{data['description']}',
                                                        '{data['photo']}', '{data['file']}', '{data['video']}');""")
            conn.commit()
        await state.finish()
        await message.answer(f'Товар зарегистрирован', reply_markup=kb)


@dp.message_handler(Text(equals='Удалить товар'))
@user_check
async def remove_pr(message: Message):
    await ProductRemove.remove_product.set()
    kb = akbb()
    await message.answer('Введите название товара для удаления (например стринги женские)', reply_markup=kb)


@dp.message_handler(state = ProductRemove.remove_product)
async def procecc_rem_pr1(message: Message, state: FSMContext):
    kb = akb1()
    if message.text == "Отмена 🔙":
        await state.finish()
        await message.answer("Действие отменено.\nМеню администратора", reply_markup=kb)
    else:
        cur.execute(f"SELECT name FROM products WHERE name = '{message.text}'")
        data = cur.fetchone()
        if not data:
            await state.finish()
            await message.answer(f"Товара с названием <b>{message.text}</b> нет. Действие отменено.\nМеню администратора", reply_markup=kb)
        else:
            cur.execute(f"DELETE FROM products WHERE name = '{data[0]}'")
            conn.commit()
            await state.finish()
            await message.answer(f"Товар <b>{message.text}</b> успешно удален.\nМеню администратора", reply_markup=kb)
