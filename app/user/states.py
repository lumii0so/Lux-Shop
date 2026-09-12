from aiogram.fsm.state import State, StatesGroup

class AddProduct(StatesGroup):
    name = State()
    category = State()
    price = State()
    stock = State()

class SupportRequest(StatesGroup):
    message = State()