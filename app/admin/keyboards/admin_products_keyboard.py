from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_products_list_keyboard(products: list, page: int, has_next_page: bool) -> InlineKeyboardMarkup:
    buttons = []

    for product in products:
        product_id = product[0]
        product_name = product[1]
        product_price = product[3]
        product_category = product[2]

        buttons.append([
            InlineKeyboardButton(
                text=f"🛍 {product_name} - 💵 {product_price}$ - 🗒️ {product_category}",
                callback_data=f"admin:product_info:{product_id}"
            )
        ])

    navigation_buttons =  []

    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Previous',
                callback_data=f'admin:products:page:{page - 1}'
            )
        )

    if has_next_page:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Next ▶️',
                callback_data=f'admin:products:page:{page + 1}'
            )
        )

    if navigation_buttons:
        buttons.append(navigation_buttons)

    buttons.append([
        InlineKeyboardButton(
            text='⬅️ Back',
            callback_data='admin:products'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_product_keyboard(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🛠️ Edit product',
                        callback_data=f'admin:product:edit:{product_id}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='❌ Delete product',
                        callback_data=f'admin:product:delete:{product_id}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='🗒️ View product statistics 🚧',
                        callback_data=f'admin:product:statistics:{product_id}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='◀️ Back',
                        callback_data='admin:products:view'
                    )
                ]
            ]
    )

def admin_product_operation_confirmation_keyboard(product_id: int, operation_name: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='✅ Confirm',
                        callback_data=f'admin:product:{operation_name}_confirmed:{product_id}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='❌ Cancel',
                        callback_data=f'admin:product:{product_id}'
                    )
                ]
            ]
    )