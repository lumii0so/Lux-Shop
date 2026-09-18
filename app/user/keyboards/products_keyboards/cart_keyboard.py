from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cart_keyboard(items: list, page: int, has_next_page: bool, cart_id: int) -> InlineKeyboardMarkup:
    buttons = []

    for item in items:
        item_id = item[0]
        item_name = item[1]
        item_price = item[2]
        item_quantity = item[3]

        buttons.append([
            InlineKeyboardButton(
                text=f"🛒 {item_name} - 💵 ${item_price} - 📦 {item_quantity}x",
                callback_data=f"cart:item:{item_id}"
            )
        ])

    navigation_buttons =  []

    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Previous',
                callback_data=f'cart:page:{page - 1}'
            )
        )

    if has_next_page:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Next ▶️',
                callback_data=f'cart:page:{page + 1}'
            )
        )

    if navigation_buttons:
        buttons.append(navigation_buttons)

    if items:
        buttons.append([
            InlineKeyboardButton(
                text='💲 Buy all',
                callback_data=f'cart:buy_confirmation:{cart_id}'
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text='⬅️ Back',
            callback_data='products'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def cart_item_keyboard(item_id: int, cart_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🛠️ Edit quantity',
                    callback_data=f'cart:edit:{item_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='🗑️ Remove from a cart',
                    callback_data=f'cart:delete:{item_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='◀️ Back',
                    callback_data=f'products:cart:{cart_id}'
                )
            ]  
        ]
    )

def cart_buy_confirmation_keyboard(cart_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅ Confirm',
                    callback_data=f'cart:buy_all:{cart_id}'
                )
            ],
            [
                InlineKeyboardButton(
                    text='◀️ Back',
                    callback_data=f'products:cart:{cart_id}'
                )
            ]  
        ]
    )

def return_to_cart_keyboard(cart_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='◀️ Back',
                        callback_data=f'products:cart:{cart_id}'
                    )
                ]  
            ]
        )