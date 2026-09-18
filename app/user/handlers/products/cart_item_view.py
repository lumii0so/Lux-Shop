from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.paths import cart_menu_image_path
from app.user.states import EditCartItem
from app.user.keyboards.products_keyboards.cart_keyboard import return_to_cart_keyboard, cart_item_keyboard
from app.database.queries import get_user_id, get_cart_id, update_cart_item, get_cart_item_details

router = Router()

@router.callback_query(F.data.startswith('cart:item:'))
async def cart_item_view_handler(callback: CallbackQuery) -> None:
    item_id = int(callback.data.split(':')[-1])

    user_id = await get_user_id(callback.from_user.id)
    cart_id = await get_cart_id(user_id)

    item = await get_cart_item_details(cart_id=cart_id, item_id=item_id)
    if not item:
        await callback.answer("❌ This item is no longer in your cart.", show_alert=True)
        return

    text = (
             f'📋 <b>{item[1].capitalize()} (<i>№{item[0]}</i>)</b>\n\n'
             f'🏷️ <b>Category: {item[4]}</b>\n\n'
             f'💲 <b>Product price: ${item[2]}</b>\n'
             f'📦 <b>Product stock: {item[3]}</b>\n'
             f"🔢 <b>In your cart: {item[5]}x (${item[6]:.2f} total) </b>"
        )

    await callback.message.delete()

    await callback.message.answer_photo(
        photo=FSInputFile(cart_menu_image_path),
        caption=text,
        reply_markup=cart_item_keyboard(item_id, cart_id),
        parse_mode='HTML'
    )

    await callback.answer()

@router.callback_query(F.data.startswith('cart:edit:'))
async def cart_item_edit_handler(callback: CallbackQuery, state: FSMContext) -> None:
    item_id = int(callback.data.split(':')[-1])

    user_id = await get_user_id(callback.from_user.id)
    cart_id = await get_cart_id(user_id)

    item = await get_cart_item_details(cart_id=cart_id, item_id=item_id)
    if not item:
        await callback.answer('❌ Item is no longer in your cart.', show_alert=True)
        return

    stock = item[3]

    await state.update_data(
        item_id=item_id, 
        stock=stock,
        cart_id=cart_id
    )
    await state.set_state(EditCartItem.quantity)

    await callback.message.delete()

    await callback.message.answer(
        text=(
            f'✏️ Enter new quantity for {item[1]}'
            f'(Available stock: {stock}):\n'
            f'To cancel editing, type "cancel".'
        )
    )
    await callback.answer()

@router.message(StateFilter(EditCartItem), F.text.casefold() == "cancel")
async def cancel_edit_cart_item(
    message: Message,
    state: FSMContext
) -> None:
    data = await state.get_data()
    cart_id = data.get('cart_id')

    await state.clear()
    await message.answer(
            '❌ Cart item editing cancelled.',
            reply_markup=return_to_cart_keyboard(cart_id)
    )

@router.message(EditCartItem.quantity)
async def item_new_quantity_handler(
    message: Message, 
    state: FSMContext
) -> None:
    if not message.text or not message.text.isdigit():
        await message.answer('❌ Invalid input. Please enter a valid number.')
        return

    new_quantity = int(message.text)
    if new_quantity <= 0:
        await message.answer('❌ Quantity must be greater than 0.')
        return

    data = await state.get_data()
    cart_id = data.get('cart_id')
    item_id = data.get('item_id')
    stock = data.get('stock', 0)

    if new_quantity > stock:
        await message.answer(f'❌ Quantity exceeds available stock ({stock}). Please enter a smaller number.')
        return

    await update_cart_item(
        cart_id=cart_id, 
        item_id=item_id, 
        quantity=new_quantity
    )
    await state.clear()

    await message.answer(
        text=f'✅ Item quantity updated to {new_quantity}x.',
        reply_markup=return_to_cart_keyboard(cart_id)
    )

@router.callback_query(F.data.startswith('cart:delete:'))
async def delete_cart_item_handler(callback: CallbackQuery) -> None:
    item_id = int(callback.data.split(':')[-1])
    
    user_id = await get_user_id(callback.from_user.id)
    cart_id = await get_cart_id(user_id)

    await update_cart_item(cart_id=cart_id, item_id=item_id, quantity=0)

    await callback.message.delete()

    await callback.message.answer(
        text='🛒 Item removed.',
        reply_markup=return_to_cart_keyboard(cart_id)
    )