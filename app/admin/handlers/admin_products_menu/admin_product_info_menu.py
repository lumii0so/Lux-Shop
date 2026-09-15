from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from decimal import Decimal, InvalidOperation

from app.config import admin_ids
from app.admin.filters import IsAdmin
from app.admin.keyboards.admin_products_keyboard import admin_product_keyboard, admin_product_operation_confirmation_keyboard
from app.admin.keyboards.admin_products_menu_keyboard import admin_products_keyboard
from app.database.queries import get_product, get_product_name, edit_product, delete_product
from app.user.states import EditProduct

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
         f'📋 <b>{product_name.capitalize()} (<i>№{product_id}</i>) (<i>{product_category}</i>)</b> 📋\n\n'
         f'💲 <b>Product price: ${product_price}</b>\n'
         f'📦 <b>Product stock: {product_stock}</b>\n\n'
         f'🔽 <b>Choose an action from below </b>🔽'
    )

    await message.answer(
        text=text,
        reply_markup=admin_product_keyboard(product_id),
        parse_mode='HTML'
    )


@router.callback_query(F.data.startswith('admin:product_info:'), IsAdmin(admin_ids))
async def admin_product_info_handler(callback: CallbackQuery) -> None:
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

# Confirming product operations

@router.callback_query(F.data.startswith('admin:product:edit:'), IsAdmin(admin_ids))
async def admin_product_edit_confirmation_handler(callback: CallbackQuery) -> None:
    product_id = int(callback.data.split(':')[-1])

    product_name = await get_product_name(product_id=product_id)

    await callback.message.delete()
    
    await callback.message.answer(
        text=f'Edit product {product_name.capitalize()} (№{product_id})?',
        reply_markup=admin_product_operation_confirmation_keyboard(product_id=product_id, operation_name='edit')
    )
    
    await callback.answer()

@router.callback_query(F.data.startswith('admin:product:delete:'), IsAdmin(admin_ids))
async def admin_product_delete_confirmation_handler(callback: CallbackQuery) -> None:
    product_id = int(callback.data.split(':')[-1])
    
    product_name = await get_product_name(product_id=product_id)
    
    await callback.message.delete()
        
    await callback.message.answer(
        text=f'Delete product {product_name.capitalize()} (№{product_id})?',
        reply_markup=admin_product_operation_confirmation_keyboard(product_id=product_id, operation_name='delete')
    )
        
    await callback.answer()

# Executing product operations

# Editing
@router.callback_query(F.data.startswith('admin:product:edit_confirmed:'), IsAdmin(admin_ids))
async def admin_product_edit_handler(callback: CallbackQuery, state: FSMContext) -> None:
    product_id = int(callback.data.split(':')[-1])
    await state.update_data(product_id=product_id)

    await state.set_state(EditProduct.name)

    await callback.message.delete()

    await callback.message.answer(
        "(Type 'cancel' at any point to cancel editing)\nEnter the product name:"
    )

    await callback.answer()

@router.message(StateFilter(EditProduct), IsAdmin(admin_ids), F.text.casefold() == "cancel")
async def cancel_add_product(
    message: Message,
    state: FSMContext
) -> None:
    await state.clear()

    await message.answer(
        "❌ Product editing cancelled.",
        reply_markup=admin_products_keyboard
    )

@router.message(EditProduct.name, IsAdmin(admin_ids))
async def product_name_handler(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text:
        await message.answer('❌ Please send a text message.')
        return
    
    await state.update_data(name=message.text)

    await state.set_state(EditProduct.category)

    await message.answer(
        "Enter the product category:"
    )

@router.message(EditProduct.category, IsAdmin(admin_ids))
async def product_category_handler(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text:
            await message.answer('❌ Please send a text message.')
            return

    await state.update_data(category=message.text)

    await state.set_state(EditProduct.price)

    await message.answer(
        "Enter the product price:"
    )

@router.message(EditProduct.price, IsAdmin(admin_ids))
async def product_price_handler(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text:
            await message.answer('❌ Please send a text message.')
            return
    
    try:
        price = Decimal(message.text)

        if price < 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        await message.answer(
            "Please enter a valid price:"
        )
        return

    await state.update_data(price=price)

    await state.set_state(EditProduct.stock)

    await message.answer(
        "Enter the product stock:"
    )

@router.message(EditProduct.stock, IsAdmin(admin_ids))
async def product_stock_handler(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text:
        await message.answer('❌ Please send a text message.')
        return
    
    if not message.text.isdigit():
        await message.answer("Please enter a valid stock amount:")
        return

    await state.update_data(stock=int(message.text))

    data = await state.get_data()

    await edit_product(
        product_id=data['product_id'],
        name=data["name"],
        category=data["category"],
        price=data["price"],
        stock=data["stock"]
    )

    await state.clear()

    await message.answer(
        "✅ Product edited.",
        reply_markup=admin_products_keyboard
    )

# Deleting
@router.callback_query(F.data.startswith('admin:product:delete_confirmed:'), IsAdmin(admin_ids))
async def admin_product_delete_handler(callback: CallbackQuery) -> None:
    product_id = int(callback.data.split(':')[-1])
    
    product_name = await get_product_name(product_id=product_id)

    await delete_product(product_id=product_id)
    
    await callback.message.delete()
        
    await callback.message.answer(
        text=f'Product {product_name.capitalize()} №{product_id} deleted',
        reply_markup=admin_products_keyboard
    )

    await callback.answer()