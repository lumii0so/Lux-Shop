from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

about_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💻 GitHub', url='https://github.com/lumii0so')
        ],
        [
            InlineKeyboardButton(text='◀️ Back', callback_data='main_menu')
        ]
    ]
)