from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.config import admin_ids
from app.admin.keyboards.admin_menu_keyboard import admin_menu_keyboard
from app.admin.filters import IsAdmin

router = Router()

async def show_admin_panel(message: Message, name: str):
    await message.answer(
            f'⚙️ <b>Welcome to admin panel, {name}</b>',
            reply_markup=admin_menu_keyboard,
            parse_mode='HTML'
        )

@router.message(Command('admin'), IsAdmin(admin_ids))
async def admin_handler(message: Message) -> None:
    await show_admin_panel(message, message.from_user.first_name)

@router.callback_query(F.data == 'admin:back')
async def admin_menu_button_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await show_admin_panel(callback.message, callback.from_user.first_name)

    await callback.answer()