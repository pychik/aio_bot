from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminDialog(StatesGroup):
    admin_add = State()
    admin_delete = State()



