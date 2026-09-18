from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.user.keyboards.support_keyboards.user_requests_keyboard import user_requests_keyboard
from app.database.queries import get_user_requests

router = Router()

@router.callback_query(F.data == "support:my_requests")
async def show_my_requests_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    requests_per_page = 5
    page = 1

    requests, has_next_page = await get_user_requests(telegram_id=callback.from_user.id,page=page, requests_per_page=requests_per_page)

    if not requests:
        await callback.message.answer(
            text=('💬 <b>You haven\'t submitted any requests yet. 💬</b>'),
            reply_markup=user_requests_keyboard([], page, False),
            parse_mode='HTML'
        )

        await callback.answer()
        return

    await callback.message.answer(
        text='💬 <b>Your requests 💬\nSelect a request from the list to continue</b>',
        reply_markup=user_requests_keyboard(
            requests,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()

@router.callback_query(F.data.startswith('user_requests:page:'))
async def products_page_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    requests_per_page = 5
    page = int(callback.data.split(':')[-1])

    requests, has_next_page = await get_user_requests(telegram_id=callback.from_user.id,page=page, requests_per_page=requests_per_page)

    await callback.message.answer(
        text='💬 <b>Open requests 💬\nSelect a request from the list to continue</b>',
        reply_markup=user_requests_keyboard(
            requests,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()