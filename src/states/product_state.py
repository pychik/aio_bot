from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductEdit(StatesGroup):
    add_product = State()
    add_description = State()
    add_photo = State()
    add_file = State()
    add_video = State()


class ProductRemove(StatesGroup):
    remove_product = State()
