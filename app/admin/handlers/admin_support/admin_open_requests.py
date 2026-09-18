from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.database.queries import retrieve_open_requests
from app.admin.keyboards.admin_support_keyboards.admin_open_requests_keyboard import open_requests_keyboard

from app.config import admin_ids
from app.admin.filters import IsAdmin

router = Router()

@router.callback_query(F.data == 'admin:support:open', IsAdmin(admin_ids))
async def products_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    requests_per_page = 5
    page = 1

    requests, has_next_page = await retrieve_open_requests(page=page, requests_per_page=requests_per_page)

    if not requests:
        await callback.message.answer(
            text=('💬 <b>There are currently no open support requests. 💬\n🔔 You will be notified when one appears.</b> 🔔'),
            reply_markup=open_requests_keyboard([], page, False),
            parse_mode='HTML'
        )

        await callback.answer()
        return

    await callback.message.answer(
        text='💬 <b>Open requests 💬\nSelect a request from the list to continue</b>',
        reply_markup=open_requests_keyboard(
            requests,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()

@router.callback_query(F.data.startswith('admin:open_requests:page:'))
async def products_page_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    requests_per_page = 5
    page = int(callback.data.split(':')[-1])

    requests, has_next_page = await retrieve_open_requests(page=page, requests_per_page=requests_per_page)

    await callback.message.answer(
        text='💬 <b>Open requests 💬\nSelect a request from the list to continue</b>',
        reply_markup=open_requests_keyboard(
            requests,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()