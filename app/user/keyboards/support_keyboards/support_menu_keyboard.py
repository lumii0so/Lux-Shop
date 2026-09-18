from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

support_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✍️ Make a support request', callback_data='support:create')
        ],
        [
            InlineKeyboardButton(text='📂 My requests', callback_data='support:my_requests')
        ],
        [
            InlineKeyboardButton(text='◀️ Back', callback_data='main_menu')
        ]
    ]
)

support_request_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Back", callback_data="support")
        ]
    ]
)