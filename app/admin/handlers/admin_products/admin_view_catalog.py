from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.config import admin_ids
from app.admin.filters import IsAdmin
from app.admin.keyboards.admin_products_keyboards.admin_catalog_keyboard import admin_catalog_keyboard
from app.database.queries import retrieve_products

router = Router()

@router.callback_query(F.data == 'admin:products:catalog', IsAdmin(admin_ids))
async def add_product_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    products_per_page = 5
    page = 1

    products, has_next_page = await retrieve_products(page=page, products_per_page=products_per_page)

    if not products:
        await callback.message.answer(
            text=('☁️ <b>There are currently no products in stock. ☁️\n📦 You can add new products through admin panel.</b> 📦'),
            reply_markup=admin_catalog_keyboard([], page, False),
            parse_mode='HTML'
        )

        await callback.answer()
        return

    await callback.message.answer(
        text='📦 <b>Admin catalog 📦\nSelect a product from the list to continue</b>',
        reply_markup=admin_catalog_keyboard(
            products,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()

@router.callback_query(F.data.startswith('admin:products:page:'))
async def products_page_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    products_per_page = 5
    page = int(callback.data.split(':')[-1])

    products, has_next_page = await retrieve_products(page=page, products_per_page=products_per_page)

    await callback.message.answer(
        text=(
            '📦 <b>Admin catalog 📦\n'
            'Select a product from the list to continue</b>'
        ),
        reply_markup=admin_catalog_keyboard(
            products,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()