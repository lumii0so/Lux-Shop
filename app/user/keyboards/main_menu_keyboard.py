from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👕 Products', callback_data='products')
        ],
        [
            InlineKeyboardButton(text='📦 My orders 🚧', callback_data='orders')
        ],
        [
            InlineKeyboardButton(text='💬 Support', callback_data='support')
        ],
        [
            InlineKeyboardButton(text='ℹ️ About', callback_data='about')
        ]
    ]
)