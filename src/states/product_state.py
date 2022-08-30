from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductAdd(StatesGroup):
    add_product = State()
    add_description = State()
    add_photo = State()
    add_file = State()
    add_video = State()


class ProductEdit(StatesGroup):
    edit_product_1 = State()
    edit_product_2 = State()
    edit_product_3 = State()


class ProductRemove(StatesGroup):
    remove_product = State()
