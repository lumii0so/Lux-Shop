import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import logging

# Config variables
from app.config import bot_key

# DB connection
from app.database.connection import init_db, close_db

# User handlers
from app.user.handlers.main_menu import router as main_menu_router
from app.user.handlers.products.view_catalog import router as catalog_router
from app.user.handlers.products.product_view import router as product_view_router
from app.user.handlers.products.user_cart import router as user_cart_router
from app.user.handlers.products.cart_item_view import router as cart_item_router


from app.user.handlers.orders import router as orders_router


from app.user.handlers.support.support_menu import router as support_menu_router
from app.user.handlers.support.write_support_request import router as write_request_router
from app.user.handlers.support.user_requests_menu import router as user_requests_router
from app.user.handlers.support.request_menu import router as user_request_menu_router


from app.user.handlers.about import router as about_router

# Admin handlers
from app.admin.handlers.admin_menu import router as admin_menu_router


from app.admin.handlers.admin_products.admin_products_menu import router as admin_products_menu_router
from app.admin.handlers.admin_products.admin_add_product import router as admin_add_product_router
from app.admin.handlers.admin_products.admin_view_catalog import router as admin_catalog_router
from app.admin.handlers.admin_products.admin_product_view import router as admin_product_view_router

from app.admin.handlers.admin_orders.admin_orders_menu import router as admin_orders_menu_router


from app.admin.handlers.admin_users.admin_users_menu import router as admin_users_menu_router


from app.admin.handlers.admin_support.admin_support_menu import router as admin_support_menu_router
from app.admin.handlers.admin_support.admin_open_requests import router as admin_open_requests_menu_router
from app.admin.handlers.admin_support.admin_request_view import router as admin_request_menu_router


from app.admin.handlers.admin_statistics.admin_statistics_menu import router as admin_statistics_menu_router

# ================================================================

# Logging info
logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=bot_key)

# Initialize dispatcher
dp = Dispatcher()

# Bot commands
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🛒 Start the bot 🛒")
    ]
    await bot.set_my_commands(commands)

# 1. User interface handler
dp.include_router(main_menu_router)

# 1.1 User products panel handlers
dp.include_router(catalog_router)
dp.include_router(product_view_router)
dp.include_router(user_cart_router)
dp.include_router(cart_item_router)

# 1.2 User orders panel handlers
dp.include_router(orders_router)

# 1.3 User support panel handlers
dp.include_router(support_menu_router)
dp.include_router(write_request_router)
dp.include_router(user_requests_router)
dp.include_router(user_request_menu_router)

# 1.4 About panel handler
dp.include_router(about_router)

# ================================================================

# 2. Admin panel handler
dp.include_router(admin_menu_router)

# 2.1 Admin products panel handlers
dp.include_router(admin_products_menu_router)
dp.include_router(admin_add_product_router)
dp.include_router(admin_catalog_router)
dp.include_router(admin_product_view_router)

# 2.2 Admin orders panel handlers
dp.include_router(admin_orders_menu_router)


# 2.3 Admin users panel handlers
dp.include_router(admin_users_menu_router)


# 2.4 Admin support panel handlers
dp.include_router(admin_support_menu_router)
dp.include_router(admin_open_requests_menu_router)
dp.include_router(admin_request_menu_router)


# 2.5 Admin statistics panel handlers
dp.include_router(admin_statistics_menu_router)

# ================================================================

async def main() -> None:
    await init_db()

    logging.info('BOT started.')
    await set_commands(bot)
    await dp.start_polling(bot)

    await close_db()

asyncio.run(main())
