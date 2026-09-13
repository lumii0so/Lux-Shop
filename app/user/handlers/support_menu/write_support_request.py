from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.admin.keyboards.admin_request_menu_keyboard import admin_request_notification_keyboard
from app.user.keyboards.support_menu_keyboards.support_menu_keyboard import support_request_keyboard
from app.user.states import SupportRequest
from app.database.queries import get_user_id, create_support_request, add_request_message
from app.config import admin_ids

router = Router()

@router.callback_query(F.data == "support:create")
async def create_support_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    prompt_message = await callback.message.answer(
        '💬 ✍️ <b>Enter your support message\nor press "Back" button to go back.</b> 🔽',
        reply_markup=support_request_keyboard,
        parse_mode="HTML"
    )

    await state.update_data(prompt_message_id=prompt_message.message_id)
    await state.set_state(SupportRequest.message)

    await callback.answer()

@router.message(SupportRequest.message)
async def support_message_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    prompt_message_id = data['prompt_message_id']

    if not message.text:
        await message.answer('❌ Please send a text message.')
        return

    user_id = await get_user_id(message.from_user.id)

    if user_id is None:
        await message.answer(
            '❌ <b>Could not find your user account. It means you somehow missed /start command and should call it.</b>',
            reply_markup=support_request_keyboard,
            parse_mode='HTML'
        )
        return

    request_id = await create_support_request(
        user_id=user_id,
        message=message.text
    )

    for admin_id in admin_ids: 
        await message.bot.send_message( 
            chat_id=admin_id, 
            text=(
                f'🆘 <b>New support request №{request_id}</b>\n\n' 
                f'👤 <b>@{message.from_user.username or "No username"}</b>\n\n' 
                f'💬 {message.text}' 
            ), 
            reply_markup=admin_request_notification_keyboard(request_id), 
            parse_mode='HTML' 
        )

    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=prompt_message_id
    )
    
    await state.clear()

    await message.answer(
        '✅ <b>Your support request has been submitted.</b>',
        reply_markup=support_request_keyboard,
        parse_mode='HTML'
    )