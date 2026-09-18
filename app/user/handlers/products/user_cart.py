from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile

from app.paths import cart_menu_image_path
from app.user.keyboards.products_keyboards.cart_keyboard import cart_keyboard, cart_buy_confirmation_keyboard, return_to_cart_keyboard
from app.database.queries import get_user_id, get_cart_id, get_cart_contents, check_cart_stock

router = Router()

async def empty_cart_message(message: Message):
    await message.answer_photo(
                photo=FSInputFile(cart_menu_image_path),
                caption=('🛒 <b>Your cart is currently empty. 🛒\n📦 Add some products from the catalog and come back.</b> 📦'),
                reply_markup=cart_keyboard([], 1, False, None),
                parse_mode='HTML'
            )

@router.callback_query(F.data.startswith('products:cart:empty'))
async def empty_cart_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await empty_cart_message(callback.message)

    await callback.answer()

@router.callback_query(F.data.startswith('products:cart:'))
async def cart_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    items_per_page = 5
    page = 1

    cart_id = int(callback.data.split(':')[-1])

    items, total_price, has_next_page = await get_cart_contents(cart_id=cart_id, page=page, items_per_page=items_per_page)
    if not items:
        await empty_cart_message(callback.message)
        return

    text = (
            '🛒 <b>Your cart 🛒</b>\n'
            f'💵 <b>Total price of the items in your cart is ${total_price}</b>\n'
            '<b>to proceed with placing your order click "Buy all"</b>\n\n'
            '<b>If you wish to change anything click on the item and choose corresponding action</b>'
    )

    await callback.message.answer_photo(
        photo=FSInputFile(cart_menu_image_path),
        caption=text,
        reply_markup=cart_keyboard(
            items,
            page,
            has_next_page,
            cart_id
        ),
        parse_mode='HTML'
    )

    await callback.answer()

@router.callback_query(F.data.startswith('cart:page:'))
async def cart_page_handler(callback: CallbackQuery) -> None:
    await callback.message.delete()

    items_per_page = 5
    page = int(callback.data.split(':')[-1])

    user_id = await get_user_id(callback.from_user.id)
    cart_id = await get_cart_id(user_id)

    items, total_price, has_next_page = await get_cart_contents(cart_id=cart_id, page=page, items_per_page=items_per_page)

    text = (
            '🛒 <b>Your cart 🛒</b>\n'
            f'💵 <b>Total price of the items in your cart is ${total_price}</b>\n'
            '<b>to proceed with placing your order click "Buy all"</b>\n\n'
            '<b>If you wish to change anything click on the item and choose corresponding action</b>'
        )
    
    await callback.message.answer_photo(
        photo=FSInputFile(cart_menu_image_path),
        caption=text,
        reply_markup=cart_keyboard(
            items,
            page,
            has_next_page,
            cart_id if cart_id else None
        ),
        parse_mode='HTML'
    )

    await callback.answer()

@router.callback_query(F.data.startswith('cart:buy_confirmation:'))
async def cart_buy_confirmation_handler(callback: CallbackQuery) -> None:
    cart_id = int(callback.data.split(':')[-1])

    stock_errors = await check_cart_stock(cart_id)
    if stock_errors:
        await callback.answer()
        error_text = ['⚠️ <b>Cannot proceed to checkout, stock has changed:</b>\n']

        for item_name, requested, available in stock_errors:
            error_text.append(f'📦 <b><i>{item_name}</i>: requested {requested}, available {available}</b>')

        error_text.append('\n<b>Please adjust quantities in your cart and try again.</b>')

        await callback.message.answer(
            text='\n'.join(error_text),
            reply_markup=return_to_cart_keyboard(cart_id),
            parse_mode='HTML'
        )
        return

    items, total_price, _ = await get_cart_contents(cart_id=cart_id, page=1, items_per_page=100)

    await callback.message.delete()

    text = ['💳 <b>Order confirmation</b>\n']

    for item in items:
        text.append(f'🛒 <b><i>{item[1]}</i> - 💵 ${item[2]} - 📦 {item[3]}x</b>')

    text.append(f'\n💵 <b>Total amount to pay: ${total_price}\nDo you wish to proceed to checkout?</b>')

    await callback.message.answer(
        text='\n'.join(text),
        reply_markup=cart_buy_confirmation_keyboard(cart_id),
        parse_mode='HTML'
    )

    await callback.answer()