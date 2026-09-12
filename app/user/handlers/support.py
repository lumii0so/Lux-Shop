from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.fsm.context import FSMContext

from app.user.keyboards.support_menu_keyboard import support_menu_keyboard, support_request_keyboard
from app.paths import support_menu_image_path
from app.user.states import SupportRequest
from app.database.queries import get_user_id, create_support_request

router = Router()

async def show_support_menu(message: Message):
    await message.answer_photo(
                    photo=FSInputFile(support_menu_image_path),
                    caption=('💬 <b>If you have any questions or problems,\nin support menu you can contact our support team. 💬\n✍️ Click "Make a support request" or press "Back" button to go back.</b> 🔽'),
                    reply_markup=support_menu_keyboard,
                    parse_mode='HTML'
                )

@router.callback_query(F.data == 'support')
async def support_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await show_support_menu(callback.message)

    await callback.answer()

@router.callback_query(F.data == "support:create")
async def create_support_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    await state.set_state(SupportRequest.message)

    await callback.message.answer(
        '💬 ✍️ <b>Enter your support message\nor press "Back" button to go back.</b> 🔽',
        reply_markup=support_request_keyboard,
        parse_mode="HTML"
    )

    await callback.answer()

@router.message(SupportRequest.message)
async def support_message_handler(message: Message, state: FSMContext) -> None:
    user_id = await get_user_id(message.from_user.id)

    if user_id is None:
        await message.answer(
            '❌ <b>Could not find your user account. It means you somehow missed /start command and should call it.</b>',
            reply_markup=support_request_keyboard,
            parse_mode='HTML'
        )
        return

    await create_support_request(
        user_id=user_id,
        username=message.from_user.username,
        message=message.text
    )

    await state.clear()

    await message.answer(
        "✅ <b>Your support request has been submitted.</b>",
        reply_markup=support_request_keyboard,
        parse_mode='HTML'
    )
