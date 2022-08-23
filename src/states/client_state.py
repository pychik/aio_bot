from aiogram.dispatcher.filters.state import State, StatesGroup


class ClientDialog(StatesGroup):
    client_choose = State()
    product_show = State()

