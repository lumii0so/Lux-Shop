from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from app.config import admin_ids
from app.admin.filters import IsAdmin

router = Router()

@router.callback_query(F.data == 'admin:products:delete', IsAdmin(admin_ids))
async def add_product_handler(callback: CallbackQuery) -> None:
    await callback.answer()