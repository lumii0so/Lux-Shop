from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='📦 Manage products',
                callback_data='admin:products'
            )
        ],
        [
            InlineKeyboardButton(
                text='🛒 Manage orders 🚧',
                callback_data='admin:orders'
            )
        ],
        [
            InlineKeyboardButton(
                text='👥 Manage users 🚧',
                callback_data='admin:users'
            )
        ],
        [
            InlineKeyboardButton(
                text='💬 Support requests',
                callback_data='admin:support'
            )
        ],
        [
            InlineKeyboardButton(
                text='🗒️ View statistics 🚧',
                callback_data='admin:statistics'
            )
        ],
        [
            InlineKeyboardButton(
                text='◀️ Exit admin panel',
                callback_data='main_menu'
            )
        ]
    ]
)