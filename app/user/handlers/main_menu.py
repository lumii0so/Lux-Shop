from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery

from app.paths import main_menu_image_path
from app.user.keyboards.main_menu_keyboard import main_menu_keyboard
from app.database.queries import create_user

router = Router()

async def show_main_menu(message: Message) -> None:
    await message.answer_photo(
            photo=FSInputFile(main_menu_image_path),
            caption='<b>🛒 Welcome to <i>Lux Shop</i>! 🛒\n🔽 Please select an action from the menu 🔽</b>',
            reply_markup=main_menu_keyboard,
            parse_mode='HTML'
        )

@router.message(Command('start'))
async def start_handler(message: Message) -> None:
    user = message.from_user

    await create_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
    )

    await show_main_menu(message)

@router.callback_query(F.data == 'main_menu')
async def main_menu_button_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await show_main_menu(callback.message)

    await callback.answer()