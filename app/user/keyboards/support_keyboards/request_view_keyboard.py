from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def opened_request_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='✍️ Send message',
                        callback_data=f'request:reply:{request_id}'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text='◀️ Back',
                        callback_data='support:my_requests'
                    )
                ]
        ]
    )

closed_request_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='📕 This request has been closed by an admin',
                callback_data='request:closed_request'
            )
        ],
        [
            InlineKeyboardButton(
                text='◀️ Back',
                callback_data='support:requests'
            )
        ]
    ]
)

def reply_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='◀️ Back',
                    callback_data=f'requestid:{request_id}'
                )
            ]
        ]
    )

def request_notification_keyboard(request_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='📂 Check request',
                    callback_data=f'requestid:{request_id}'
                )
            ]
        ]
    )

user_support_request_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Back", callback_data="support")
        ]
    ]
)