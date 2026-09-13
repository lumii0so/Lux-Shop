from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.user.keyboards.support_menu_keyboards.support_menu_keyboard import support_menu_keyboard
from app.paths import support_menu_image_path

router = Router()

async def show_support_menu(message: Message):
    await message.answer_photo(
                    photo=FSInputFile(support_menu_image_path),
                    caption=('💬 <b>If you have any questions or problems\nyou can contact our support team. 💬</b>'),
                    reply_markup=support_menu_keyboard,
                    parse_mode='HTML'
                )

@router.callback_query(F.data == 'support')
async def support_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await show_support_menu(callback.message)

    await callback.answer()
