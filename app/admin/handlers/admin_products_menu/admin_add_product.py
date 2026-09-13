from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.config import admin_ids
from app.admin.keyboards.admin_products_keyboard import admin_products_keyboard
from app.admin.filters import IsAdmin
from app.user.states import AddProduct
from app.database.queries import add_product

from decimal import Decimal, InvalidOperation

router = Router()

# Add product

@router.callback_query(F.data == 'admin:products:add', IsAdmin(admin_ids))
async def add_product_handler(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(AddProduct.name)

    await callback.message.delete()

    await callback.message.answer(
        "(Type 'cancel' at any point to cancel adding)\nEnter the product name:"
    )

    await callback.answer()

@router.message(StateFilter(AddProduct), IsAdmin(admin_ids), F.text.casefold() == "cancel")
async def cancel_add_product(
    message: Message,
    state: FSMContext
) -> None:
    await state.clear()

    await message.answer(
        "❌ Product adding cancelled.",
        reply_markup=admin_products_keyboard
    )

@router.message(AddProduct.name, IsAdmin(admin_ids))
async def product_name_handler(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text:
        await message.answer('❌ Please send a text message.')
        return
    
    await state.update_data(name=message.text)

    await state.set_state(AddProduct.category)

    await message.answer(
        "Enter the product category:"
    )

@router.message(AddProduct.category, IsAdmin(admin_ids))
async def product_category_handler(
    message: Message,
    state: FSMContext
) -> None:
    if not message.text:
            await message.answer('❌ Please send a text message.')
            return

    await state.update_data(category=message.text)

    await state.set_state(AddProduct.price)

    await message.answer(
        "Enter the product price:"
    )

@router.message(AddProduct.price, IsAdmin(admin_ids))
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

    await state.set_state(AddProduct.stock)

    await message.answer(
        "Enter the product stock:"
    )

@router.message(AddProduct.stock, IsAdmin(admin_ids))
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

    await add_product(
        name=data["name"],
        category=data["category"],
        price=data["price"],
        stock=data["stock"]
    )

    await state.clear()

    await message.answer(
        "✅ Product information collected.",
        reply_markup=admin_products_keyboard
    )