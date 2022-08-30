from main import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from states import ProductAdd, ProductEdit, ProductRemove
from storages import cur, conn
from utility import akb1, akb3, akbb, hkb, user_check


@dp.message_handler(Text(equals='Все товары'))
@user_check
async def view_pr(message: Message):
    kb = akb1()
    cur.execute("SELECT name FROM products")
    products = cur.fetchall()
    pr = ',\n'.join(list(map(lambda x: f'<b>{x[0]}</b>', products)))
    await message.answer(f'Найдены товары:\n{pr}', reply_markup=kb)


@dp.message_handler(Text(equals="Выбрать товар 🛍️"))
async def cmd_link(message: Message):
    cur.execute("SELECT name FROM products")
    product_obj = cur.fetchall()
    products = list(map(lambda x: x[0], product_obj))
    buttons = [KeyboardButton(text=f"{p} {random_em()}") for p in products]
    kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    kb.add(*buttons)
    kb.add("Отмена 🔙")
    await ClientDialog.client_choose.set()
    await message.answer("Выберите товар из предложенных в <b>меню</b>", reply_markup=kb, )


@dp.message_handler(Text(equals='Добавить товар'))
@user_check
async def add_pr(message: Message):
    await ProductAdd.add_product.set()
    kb = akbb()
    await message.answer('Введите название нового товара (например стринги женские)', reply_markup=kb)


@dp.message_handler(state=ProductAdd.add_product)
async def process_pr_1(message: Message, state: FSMContext):
    if message.text.startswith('Отмена'):
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['name'] = message.text
        kb = akbb()
        await ProductAdd.next()
        await message.answer(f'Введите описание', reply_markup=kb)


@dp.message_handler(state=ProductAdd.add_description)
async def process_pr_2(message: Message, state: FSMContext):
    if message.text.startswith('Отмена'):
        kb = akb1()
        await message.answer('Меню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['description'] = message.text
        kb = akbb()
        kb.row(KeyboardButton(text="Нет фотографий"))
        await ProductAdd.next()
        await message.answer(f'Загрузите фото', reply_markup=kb)


@dp.message_handler(content_types=['photo', 'text'], state=ProductAdd.add_photo)
async def process_pr_3(message: Message, state: FSMContext):

    if message['photo']:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        kb = akbb()
        kb.row(KeyboardButton(text="Нет инструкций"))
        await ProductAdd.next()
        await message.answer(f'Добавьте файл с инструкцией', reply_markup=kb)
    elif message.text and message.text.startswith('Нет фотографий'):
        async with state.proxy() as data:
            data['photo'] = message.text
        kb = akbb()
        kb.row(KeyboardButton(text="Нет инструкций"))
        await ProductAdd.next()
        await message.answer(f'Добавьте файл с инструкцией', reply_markup=kb)

    elif message.text and message.text.startswith('Отмена'):
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        kb = akb1()
        await message.answer('Неизвестное действие со стороны пользователя.\n<b>Меню Админимстратора</b>',
                             reply_markup=kb)
        await state.finish()


@dp.message_handler(content_types=['document', 'text'], state=ProductAdd.add_file)
async def process_pr_4(message: Message, state: FSMContext):

    if message['document']:

        async with state.proxy() as data:
            data['file'] = message.document.file_id
        kb = akbb()
        kb.row(KeyboardButton(text="Нет видео"))
        await ProductAdd.next()
        await message.answer(f'Добавьте видео', reply_markup=kb)

    elif message.text and message.text.startswith('Нет инструкций'):
        async with state.proxy() as data:
            data['file'] = message.text
        kb = akbb()
        kb.row(KeyboardButton(text="Нет видео"))
        await ProductAdd.next()
        await message.answer(f'Добавьте видео', reply_markup=kb)
    elif message.text and message.text.startswith('Отмена'):
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        kb = akb1()
        await message.answer('Неизвестное действие со стороны пользователя.\n<b>Меню Админимстратора</b>', reply_markup=kb)
        await state.finish()


@dp.message_handler(content_types=['video', 'text'], state=ProductAdd.add_video)
async def process_pr_5(message: Message, state: FSMContext):

    if message['video']:
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
    elif message.text and message.text.startswith('Нет видео'):
        async with state.proxy() as data:
            data['video'] = message.text
        kb = akb1()
        async with state.proxy() as data:
            cur.execute(f"""INSERT INTO products(name, description, photo_id, file_id, video_id)
                                                        VALUES('{data['name']}', '{data['description']}',
                                                        '{data['photo']}', '{data['file']}', '{data['video']}');""")
            conn.commit()
        await state.finish()
        await message.answer(f'Товар зарегистрирован', reply_markup=kb)

    elif message.text and message.text.startswith('Отмена'):
        kb = akb1()
        await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
        await state.finish()
    else:
        kb = akb1()
        await message.answer('Неизвестное действие со стороны пользователя.\n<b>Меню Админимстратора</b>',
                             reply_markup=kb)
        await state.finish()


@dp.message_handler(Text(equals='Удалить товар'))
@user_check
async def remove_pr(message: Message):
    await ProductRemove.remove_product.set()
    cur.execute("""SELECT name FROM products;""")
    product_obj = cur.fetchall()
    products = list(map(lambda x: x[0], product_obj))
    buttons = [KeyboardButton(text=f"{p}") for p in products]
    kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    kb.add(*buttons)
    kb.add("Отмена 🔙")
    await message.answer('Выберите товар для удаления', reply_markup=kb)


@dp.message_handler(state=ProductRemove.remove_product)
async def process_rem_pr1(message: Message, state: FSMContext):
    kb = akb1()
    if message.text.startswith('Отмена'):
        await state.finish()
        await message.answer("Действие отменено.\nМеню администратора", reply_markup=kb)
    else:
        cur.execute(f"SELECT name FROM products WHERE name = '{message.text}';")
        data = cur.fetchone()
        if not data:
            await state.finish()
            await message.answer(f"Товара с названием <b>{message.text}</b> нет. Действие отменено.\nМеню администратора", reply_markup=kb)
        else:
            cur.execute(f"DELETE FROM products WHERE name = '{data[0]}';")
            conn.commit()
            await state.finish()
            await message.answer(f"Товар <b>{message.text}</b> успешно удален.\nМеню администратора", reply_markup=kb)


@dp.message_handler(Text(equals='Редактировать товар'))
@user_check
async def edit_pr(message: Message):
    await ProductEdit.edit_product_1.set()
    cur.execute("""SELECT name FROM products;""")
    product_obj = cur.fetchall()
    products = list(map(lambda x: x[0], product_obj))
    buttons = [KeyboardButton(text=f"{p}") for p in products]
    kb = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    kb.add(*buttons)
    kb.add("Отмена 🔙")
    await message.answer('Выберите товар для редактирования', reply_markup=kb)


@dp.message_handler(state=ProductEdit.edit_product_1)
async def process_edit_pr1(message: Message, state: FSMContext):
    kb = akb1()
    if message.text.startswith('Отмена'):
        await state.finish()
        await message.answer("Действие отменено.\nМеню администратора", reply_markup=kb)
    else:
        cur.execute(f"SELECT name FROM products WHERE name = '{message.text}';")
        data = cur.fetchone()
        if not data:
            await state.finish()
            await message.answer(f"Товара с названием <b>{message.text}</b> нет. Действие отменено.\nМеню администратора", reply_markup=kb)
        else:
            async with state.proxy() as data:
                data['name'] = message.text
            kb = akb3()
            await ProductEdit.next()
            await message.answer(f"Выбран товар: {message.text}", reply_markup=kb)


@dp.message_handler(state=ProductEdit.edit_product_2)
async def process_edit_pr2(message: Message, state: FSMContext):
    kb = akb1()
    if message.text.startswith('Отмена'):
        await state.finish()
        await message.answer("Действие отменено.\nМеню администратора", reply_markup=kb)

    elif message.text == 'Ред. описание':
        kb = akbb()
        async with state.proxy() as data:
            data['type'] = message.text
        await ProductEdit.next()
        await message.answer(f'Добавьте описание', reply_markup=kb)

    elif message.text == 'Ред. фото':
        kb = akbb()
        kb.row(KeyboardButton(text="Нет фотографий"))
        async with state.proxy() as data:
            data['type'] = message.text
        await ProductEdit.next()
        await message.answer(f'Добавьте фото', reply_markup=kb)
    elif message.text == 'Ред. инструкцию':
        kb = akbb()
        kb.row(KeyboardButton(text="Нет инструкций"))
        async with state.proxy() as data:
            data['type'] = message.text
        await ProductEdit.next()
        await message.answer(f'Добавьте файл с инструкцией', reply_markup=kb)
    elif message.text == 'Ред. видео':
        kb = akbb()
        kb.row(KeyboardButton(text="Нет видео"))
        async with state.proxy() as data:
            data['type'] = message.text
        await ProductEdit.next()
        await message.answer(f'Добавьте файл с видео', reply_markup=kb)

    else:
        kb = akb1()
        await state.finish()
        await message.answer("Действие отменено. Из-за странного ввода пользователя.\nМеню администратора", reply_markup=kb)


@dp.message_handler(content_types=['video', 'text', 'document', 'photo'], state=ProductEdit.edit_product_3)
async def process_edit_pr_3(message: Message, state: FSMContext):
    kb = akb1()
    async with state.proxy() as data:
        if message['video']:
            cur.execute(f"""UPDATE products SET video_id = '{message.video.file_id}' WHERE name = '{data["name"]}';""")
            conn.commit()
            await state.finish()
            await message.answer(f'Товар зарегистрирован', reply_markup=kb)

        elif message['document']:
            cur.execute(f"""UPDATE products SET file_id = '{message.document.file_id}' WHERE name = '{data["name"]}';""")
            # cur.execute(f"""INSERT or REPLACE products(file_id) into products
            #                                  VALUES('{message.document.file_id}') WHERE name = '{data["name"]}';""")
            conn.commit()
            await state.finish()
            await message.answer(f'Товар зарегистрирован', reply_markup=kb)
        elif message['photo']:
            cur.execute(f"""UPDATE products SET photo_id = '{message.photo[0].file_id}' WHERE name = '{data["name"]}';""")
            # cur.execute(f"""INSERT or REPLACE products(photo_id) into products
            #                                  VALUES('{message.photo[0].file_id}') WHERE name = '{data["name"]}';""")
            conn.commit()
            await state.finish()
            await message.answer(f'Товар зарегистрирован', reply_markup=kb)

        elif message.text and data["type"] == 'Ред. описание':
            cur.execute(
                    f"""UPDATE products SET description = '{message.text}' WHERE name = '{data["name"]}';""")
            # cur.execute(f"""INSERT OR REPLACE INTO products(description)
            #                                            VALUES('{data['description']}');""")
            conn.commit()
            await state.finish()
            await message.answer(f'Товар зарегистрирован', reply_markup=kb)


        elif message.text and message.text.startswith('Нет видео'):
            cur.execute(f"""UPDATE products SET video_id = '{message.text}' WHERE name = '{data["name"]}';""")
            # cur.execute(f"""INSERT or REPLACE products(video_id) into products
            #                                              VALUES('{message.text}') WHERE name = '{data["name"]}';""")
            conn.commit()
            await state.finish()
            await message.answer(f'Товар зарегистрирован', reply_markup=kb)
        elif message.text and message.text.startswith('Нет фотографий'):
            cur.execute(f"""UPDATE products SET photo_id = '{message.text}' WHERE name = '{data["name"]}';""")
            # cur.execute(f"""INSERT or REPLACE products(photo_id) into products
            #                                             VALUES('{message.text}') WHERE name = '{data["name"]}';""")
            conn.commit()
            await state.finish()
            await message.answer(f'Товар зарегистрирован', reply_markup=kb)
        elif message.text and message.text.startswith('Нет инструкций'):
            cur.execute(f"""UPDATE products SET file_id = '{message.text}' WHERE name = '{data["name"]}';""")
            # cur.execute(f"""INSERT or REPLACE products(file_id) into products
            #                                             VALUES('{message.text}') WHERE name = '{data["name"]}';""")
            conn.commit()
            await state.finish()
            await message.answer(f'Товар зарегистрирован', reply_markup=kb)

        elif message.text and message.text.startswith('Отмена'):
            await message.answer('Действие отменено.\nМеню Админимстратора', reply_markup=kb)
            await state.finish()

        else:
            await message.answer('Неизвестное действие со стороны пользователя.\n<b>Меню Админимстратора</b>',
                                 reply_markup=kb)
            await state.finish()
