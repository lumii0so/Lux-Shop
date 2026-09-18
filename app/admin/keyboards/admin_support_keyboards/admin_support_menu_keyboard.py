from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_support_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📖 Open requests',
                    callback_data='admin:support:open'
                )
            ],
            [
                InlineKeyboardButton(
                    text='🗒️ All requests 🚧',
                    callback_data='admin:support:all'
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