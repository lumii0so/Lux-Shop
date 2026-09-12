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
                    text='🛠️ Edit product 🚧',
                    callback_data='admin:products:edit'
                )
            ],
            [
                InlineKeyboardButton(
                    text='❌ Delete product 🚧',
                    callback_data='admin:products:delete'
                )
            ],
            [
                InlineKeyboardButton(
                    text='🗒️ View product statistics 🚧',
                    callback_data='admin:products:statistics'
                )
            ],
            [
                InlineKeyboardButton(
                    text='◀️ Back',
                    callback_data='admin:back'
                )
            ]
        ]
)