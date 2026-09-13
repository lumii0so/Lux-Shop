from aiogram.fsm.state import State, StatesGroup

class AddProduct(StatesGroup):
    name = State()
    category = State()
    price = State()
    stock = State()

class SupportRequest(StatesGroup):
    message = State()

class UserReplyRequest(StatesGroup):
    message = State()

class AdminReplyRequest(StatesGroup):
    message = State()