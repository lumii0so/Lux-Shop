from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_request_menu_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='✍️ Reply',
                        callback_data=f'admin:request:reply:{request_id}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='✅ Close',
                        callback_data=f'admin:request:close:{request_id}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='◀️ Back',
                        callback_data='admin:support:open'
                    )
                ]
        ]
    )

def admin_request_reply_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='◀️ Back',
                    callback_data=f'admin:requestid:{request_id}'
                )
            ]
        ]
    )

def admin_request_notification_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📂 Check request',
                    callback_data=f'admin:requestid:{request_id}'
                )
            ]
        ]
    )

def admin_notification_reply_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='◀️ Back',
                    callback_data=f'admin:requestid:{request_id}'
                )
            ]
        ]
    )

admin_support_request_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Back", callback_data="admin:support")
        ]
    ]
)