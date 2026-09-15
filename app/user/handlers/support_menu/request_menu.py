from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.config import admin_ids
from app.admin.keyboards.admin_request_menu_keyboard import admin_notification_keyboard
from app.user.keyboards.support_menu_keyboards.request_menu_keyboard import opened_request_keyboard, closed_request_keyboard, user_support_request_keyboard, reply_keyboard
from app.database.queries import get_request, get_request_messages, add_request_message, get_request_telegram_id
from app.user.states import UserReplyRequest

router = Router()

async def show_request_menu(message: Message, request_id: int, username: str, messages: list[tuple]) -> None:
    text = (
        f'🆘 <b>Support request №{request_id} (User)</b>\n\n'
        f'👤 <b>@{username}</b>\n\n'
    )

    for sender_type, message_text, created_at in messages:
        if sender_type == 'user':
            text += f'👤 <b>User ({created_at}): </b> {message_text}\n\n'
        else:
            text += f'🛠 <b>Admin ({created_at}): </b> {message_text}\n\n'

    await message.answer(
                text=text,
                reply_markup=opened_request_keyboard(request_id),
                parse_mode='HTML'
            )

@router.callback_query(F.data.startswith('requestid:'))
async def add_product_handler(callback: CallbackQuery) -> None:
    request_id = int(callback.data.split(':')[-1])

    request = await get_request(request_id=request_id)
    if request is None:
        await callback.answer('❌ Request not found.', show_alert=True)
        return

    messages = await get_request_messages(request_id)

    await callback.message.delete()

    await show_request_menu(message=callback.message, request_id=request[0], username=request[2], messages=messages)

    await callback.answer()

@router.callback_query(F.data.startswith('request:reply:'))
async def reply_request_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    request_id = int(callback.data.split(':')[-1])

    prompt_message = await callback.message.answer(
            text='💬 Enter your reply:',
            reply_markup=reply_keyboard(request_id)
        )

    await state.update_data(request_id=request_id, prompt_message_id=prompt_message.message_id)
    await state.set_state(UserReplyRequest.message)

    await callback.answer()

@router.message(UserReplyRequest.message)
async def admin_reply_message_handler(
    message: Message,
    state: FSMContext
) -> None:
    data = await state.get_data()

    request_id = data['request_id']
    prompt_message_id = data['prompt_message_id']

    if not message.text:
        await message.answer('❌ Please send a text message.')
        return

    telegram_id = await get_request_telegram_id(request_id)

    if telegram_id is None:
        await message.answer('❌ User not found.')
        await state.clear()
        return

    await add_request_message(
        request_id=request_id,
        sender_type='user',
        message=message.text
    )

    for admin_id in admin_ids: 
            await message.bot.send_message( 
                chat_id=admin_id, 
                text=(
                    f'🆘 <b>New user response in request №{request_id}</b>\n\n' 
                    f'👤 <b>@{message.from_user.username or "No username"}</b>\n\n' 
                    f'💬 {message.text}' 
                ), 
                reply_markup=admin_notification_keyboard(request_id), 
                parse_mode='HTML' 
            )

    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=prompt_message_id
    )

    await state.clear()

    await message.answer(
        f'✅ <b>Your message on request №{request_id} has been sent.</b>',
        reply_markup=user_support_request_keyboard,
        parse_mode='HTML'
    )