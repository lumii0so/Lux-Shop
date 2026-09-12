from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from app.user.keyboards.orders_menu_keyboard import orders_menu_keyboard

router = Router()

async def show_orders_menu(message: Message):
    await message.answer_photo(
                #photo=FSInputFile(orders_menu_image_path),
                caption='',
                reply_markup=orders_menu_keyboard,
                parse_mode='HTML'
            )

@router.callback_query(F.data == 'orders')
async def about_menu_button_handler(callback: CallbackQuery) -> None:
    #await callback.message.delete()

    #await show_orders_menu(callback.message)

    await callback.answer()