from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from app.config import admin_ids
from app.admin.filters import IsAdmin
from app.admin.keyboards.admin_support_keyboards.admin_support_menu_keyboard import admin_support_keyboard

router = Router()

async def show_admin_support_menu(message: Message):
    await message.answer(
        text='💬 <b>Support menu</b> ⚙️',
        reply_markup=admin_support_keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data == 'admin:support', IsAdmin(admin_ids))
async def add_product_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await show_admin_support_menu(callback.message)

    await callback.answer()