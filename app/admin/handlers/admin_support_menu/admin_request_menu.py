from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.user.keyboards.support_menu_keyboards.request_menu_keyboard import request_notification_keyboard
from app.admin.keyboards.admin_request_menu_keyboard import admin_request_menu_keyboard, admin_request_reply_keyboard, admin_notification_keyboard
from app.database.queries import get_request, get_request_messages, add_request_message, get_request_telegram_id
from app.user.states import AdminReplyRequest
from app.config import admin_ids
from app.admin.filters import IsAdmin

router = Router()

async def show_request_menu(message: Message, request_id: int, username: str, messages: list[tuple]) -> None:
    text = (
        f'🆘 <b>Support request №{request_id} (Admin)</b>\n\n'
        f'👤 <b>@{username}</b>\n\n'
    )

    for sender_type, message_text, created_at in messages:
        if sender_type == 'user':
            text += f'👤 <b>User ({created_at}): </b> {message_text}\n\n'
        else:
            text += f'🛠 <b>Admin ({created_at}): </b> {message_text}\n\n'

    await message.answer(
                text=text,
                reply_markup=admin_request_menu_keyboard(request_id),
                parse_mode='HTML'
            )

@router.callback_query(F.data.startswith('admin:requestid:'), IsAdmin(admin_ids))
async def admin_menu_button_handler(callback: CallbackQuery) -> None:
    request_id = int(callback.data.split(':')[-1])

    request = await get_request(request_id=request_id)
    if request is None:
        await callback.answer('❌ Request not found.', show_alert=True)
        return

    messages = await get_request_messages(request_id)

    await callback.message.delete()

    await show_request_menu(message=callback.message, request_id=request[0], username=request[2], messages=messages)

    await callback.answer()

@router.callback_query(F.data.startswith('admin:request:reply:'))
async def reply_request_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    request_id = int(callback.data.split(':')[-1])

    prompt_message = await callback.message.answer(
            text='💬 Enter your reply:',
            reply_markup=admin_request_reply_keyboard(request_id)
        )

    await state.update_data(request_id=request_id, prompt_message_id=prompt_message.message_id)
    await state.set_state(AdminReplyRequest.message)

    await callback.answer()

@router.message(AdminReplyRequest.message)
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
        sender_type='admin',
        message=message.text
    )

    await message.bot.send_message(
        chat_id=telegram_id,
        text=f'🛠 <b>Admin has responded to your request №{request_id} 🛠</b>',
        reply_markup=request_notification_keyboard(request_id),
        parse_mode='HTML'
    )

    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=prompt_message_id
    )

    await state.clear()

    await message.answer(
        '✅ <b>Your support request response has been sent.</b>',
        reply_markup=admin_notification_keyboard(request_id),
        parse_mode='HTML'
    )