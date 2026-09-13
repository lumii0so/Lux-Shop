from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def user_requests_keyboard(requests: list, page: int, has_next_page: bool) -> InlineKeyboardMarkup:
    buttons = []
    
    for request in requests:
        request_id = request[0]
        created_at = request[1]
        request_status = request[2]
        
        buttons.append([
            InlineKeyboardButton(
                text=f"💬 №{request_id} - ⌚ {created_at} - Status: {request_status} 📁",
                callback_data=f"requestid:{request_id}"
            )
        ])
    
    navigation_buttons =  []
    
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Previous',
                callback_data=f'user_requests:page:{page - 1}'
            )
        )
    
    if has_next_page:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Next ▶️',
                callback_data=f'user_requests:page:{page + 1}'
            )
        )
    
    if navigation_buttons:
        buttons.append(navigation_buttons)
    
    buttons.append([
        InlineKeyboardButton(
            text='⬅️ Back',
            callback_data='support'
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)