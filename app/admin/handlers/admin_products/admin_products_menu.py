from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from app.admin.keyboards.admin_products_keyboards.admin_products_menu_keyboard import admin_products_keyboard
from app.config import admin_ids
from app.admin.filters import IsAdmin

router = Router()

async def show_admin_products_menu(message: Message):
    await message.answer(
                '📦 <b>Products menu</b> ⚙️',
                reply_markup=admin_products_keyboard,
                parse_mode='HTML'
            )

@router.callback_query(F.data == 'admin:products', IsAdmin(admin_ids))
async def admin_menu_button_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await show_admin_products_menu(callback.message)

    await callback.answer()