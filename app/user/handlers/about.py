from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from app.user.keyboards.about_menu_keyboard import about_menu_keyboard
from app.config import bot_version

router = Router()

about_text = f"""\
<b>Lux Shop is a Telegram based shopping bot</b>
<b>built to make product browsing and ordering simple.</b>

🛠️ Version: v{bot_version}
🧑‍💻 Dev: lumii0so
☁️ Status: In development

"""

async def show_about_menu(message: Message):
    await message.answer(
        text=about_text,
        reply_markup=about_menu_keyboard,
        parse_mode='HTML'
    )

@router.callback_query(F.data == 'about')
async def about_menu_button_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await show_about_menu(callback.message)

    await callback.answer()