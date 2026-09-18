from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from decimal import Decimal

from app.user.keyboards.products_keyboards.catalog_keyboard import product_keyboard, return_to_products_keyboard
from app.database.queries import get_product, add_item_to_cart, get_user_id, get_product_name
from app.paths import catalog_menu_image_path
from app.user.states import AddToCart

router = Router()

async def show_product_info(
    message: Message, 
    product_id: int, 
    product_name: str, 
    product_price: Decimal, 
    product_stock: int, 
    product_category: str
) -> None:
    text = (
         f'📋 <b>{product_name.capitalize()} (<i>№{product_id}</i>)</b>\n\n'
         f'🏷️ <b>Category: {product_category}</b>\n\n'
         f'💲 <b>Product price: ${product_price}</b>\n'
         f'📦 <b>Product stock: {product_stock}</b>'
    )

    await message.answer_photo(
        photo=FSInputFile(catalog_menu_image_path),
        caption=text,
        reply_markup=product_keyboard(product_id),
        parse_mode='HTML'
    )

@router.callback_query(F.data.startswith('product_info:'))
async def product_info_handler(callback: CallbackQuery) -> None:
    product_id = int(callback.data.split(':')[-1])

    product = await get_product(product_id=product_id)
    if product is None:
            await callback.answer('❌ Product not found.', show_alert=True)
            return

    product_name = product[1]
    product_price = product[2]
    product_stock = product[3]
    product_category = product[4]

    await callback.message.delete()

    await show_product_info(message=callback.message, 
                            product_id=product_id, 
                            product_name=product_name, 
                            product_price=product_price, 
                            product_stock=product_stock, 
                            product_category=product_category)

    await callback.answer()

@router.callback_query(F.data.startswith('products:add_to_cart:'))
async def product_add_to_cart_handler(callback: CallbackQuery, state: FSMContext) -> None:
    product_id = int(callback.data.split(':')[-1])

    product = await get_product(product_id)
    if not product:
        await callback.answer('❌ Product not found.', show_alert=True)
        return
    
    stock = product[3]
    if stock <= 0:
        await callback.answer('Sorry, this item is out of stock.', show_alert=True)
        return

    await state.update_data(
        product_id=product_id, 
        stock=stock
    )
    await state.set_state(AddToCart.quantity)

    await callback.message.delete()

    await callback.message.answer(
        text=f'Enter quantity (Available stock: <b>{stock}</b>; to cancel adding item to a cart type "cancel"):',
        parse_mode='HTML'
    )

    await callback.answer()

@router.message(StateFilter(AddToCart), F.text.casefold() == "cancel")
async def cancel_add_to_cart(
    message: Message,
    state: FSMContext
) -> None:
    await state.clear()
     
    await message.answer(
            '❌ Item adding cancelled.',
            reply_markup=return_to_products_keyboard
    )

@router.message(AddToCart.quantity)
async def item_quantity_handler(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text or not message.text.isdigit():
        await message.answer('❌ Invalid input. Please enter a valid number.')
        return

    quantity = int(message.text)
    if quantity <= 0:
        await message.answer('❌ Quantity must be greater than 0.')
        return

    data = await state.get_data()
    product_id = data.get('product_id')
    stock = data.get('stock', 0)

    if quantity > stock:
        await message.answer(f'❌ Quantity exceeds available stock ({stock}). Please enter a smaller number.')
        return

    user_id = await get_user_id(message.from_user.id)
    if not user_id:
        await message.answer('❌ Could not find your user account. It means you somehow missed /start command and should call it.')
        await state.clear()
        return

    await add_item_to_cart(
        user_id=user_id, 
        product_id=product_id, 
        quantity=quantity
    )
    await state.clear()

    product_name = await get_product_name(product_id)
    await message.answer(
        text=f'✅ Added <b>{quantity}x {product_name}</b> to your cart!',
        parse_mode='HTML',
        reply_markup=return_to_products_keyboard
    )