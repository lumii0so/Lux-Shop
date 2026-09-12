from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from app.database.queries import retrieve_products
from app.paths import products_menu_image_path
from app.user.keyboards.products_keyboard import products_keyboard

router = Router()

@router.callback_query(F.data == 'products')
async def products_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    products_per_page = 5
    page = 1

    products, has_next_page = await retrieve_products(page=page, products_per_page=products_per_page)

    if not products:
        await callback.message.answer_photo(
            photo=FSInputFile(products_menu_image_path),
            caption=('☁️ <b>There are currently no products in stock. ☁️\n📦 Please wait for a restock.</b> 📦'),
            reply_markup=products_keyboard([], page, False),
            parse_mode='HTML'
        )

        await callback.answer()
        return

    await callback.message.answer_photo(
        photo=FSInputFile(products_menu_image_path),
        caption='📦 <b>Products menu 📦\nSelect a product from the list to continue</b>',
        reply_markup=products_keyboard(
            products,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()

@router.callback_query(F.data.startswith('products:page:'))
async def products_page_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    products_per_page = 5
    page = int(callback.data.split(':')[-1])

    products, has_next_page = await retrieve_products(page=page, products_per_page=products_per_page)

    await callback.message.answer_photo(
        photo=FSInputFile(products_menu_image_path),
        caption=(
            '📦 <b>Products menu 📦\n'
            'Select a product from the list to continue</b>'
        ),
        reply_markup=products_keyboard(
            products,
            page,
            has_next_page
        ),
        parse_mode='HTML'
    )

    await callback.answer()