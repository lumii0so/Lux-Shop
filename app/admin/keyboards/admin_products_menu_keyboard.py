from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_products_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='➕ Add product',
                    callback_data='admin:products:add'
                )
            ],
            [
                InlineKeyboardButton(
                    text='📖 View products',
                    callback_data='admin:products:view'
                )
            ],
            [
                InlineKeyboardButton(
                    text='◀️ Back',
                    callback_data='admin:menu'
                )
            ]
        ]
)