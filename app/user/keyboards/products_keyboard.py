from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def products_list_keyboard(products: list, page: int, has_next_page: bool) -> InlineKeyboardMarkup:
    buttons = []

    for product in products:
        product_id = product[0]
        product_name = product[1]
        product_price = product[3]
        product_category = product[2]

        buttons.append([
            InlineKeyboardButton(
                text=f"🛍 {product_name} - 💵 {product_price}$ - 🗒️ {product_category}",
                callback_data=f"product:{product_id}"
            )
        ])

    navigation_buttons =  []

    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Previous',
                callback_data=f'products:page:{page - 1}'
            )
        )

    if has_next_page:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Next ▶️',
                callback_data=f'products:page:{page + 1}'
            )
        )

    if navigation_buttons:
        buttons.append(navigation_buttons)

    buttons.append([
        InlineKeyboardButton(
            text='⬅️ Back',
            callback_data='main_menu'
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)