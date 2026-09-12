import os, asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import logging

# Config variables
from app.config import bot_key

# DB connection
from app.database.connection import init_db, close_db

# User handlers
from app.user.handlers.main_menu import router as main_menu_router
from app.user.handlers.products import router as products_router
from app.user.handlers.orders import router as orders_router
from app.user.handlers.support import router as support_router
from app.user.handlers.about import router as about_router

# Admin handlers
from app.admin.handlers.admin_menu import router as admin_menu_router

from app.admin.handlers.admin_products_menu.admin_products_menu import router as admin_products_menu_router
from app.admin.handlers.admin_products_menu.admin_add_product import router as admin_add_product_router
from app.admin.handlers.admin_products_menu.admin_edit_product import router as admin_edit_product_router
from app.admin.handlers.admin_products_menu.admin_delete_product import router as admin_delete_product_router
from app.admin.handlers.admin_products_menu.admin_product_statistics import router as admin_product_statistics_router

from app.admin.handlers.admin_orders_menu.admin_orders_menu import router as admin_orders_menu_router


from app.admin.handlers.admin_users_menu.admin_users_menu import router as admin_users_menu_router


from app.admin.handlers.admin_support_menu.admin_support_menu import router as admin_support_menu_router


from app.admin.handlers.admin_statistics_menu.admin_statistics_menu import router as admin_statistics_menu_router



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

# 1. User interface handlers
dp.include_router(main_menu_router)
dp.include_router(products_router)
dp.include_router(orders_router)
dp.include_router(support_router)
dp.include_router(about_router)

# 2. Admin panel handlers
dp.include_router(admin_menu_router)

# 2.1 Admin products panel handlers
dp.include_router(admin_products_menu_router)
dp.include_router(admin_add_product_router)
dp.include_router(admin_edit_product_router)
dp.include_router(admin_delete_product_router)
dp.include_router(admin_product_statistics_router)

# 2.2 Admin orders panel handlers
dp.include_router(admin_orders_menu_router)


# 2.3 Admin users panel handlers
dp.include_router(admin_users_menu_router)


# 2.4 Admin support panel handlers
dp.include_router(admin_support_menu_router)


# 2.5 Admin statistics panel handlers
dp.include_router(admin_statistics_menu_router)


async def main() -> None:
    await init_db()

    logging.info('BOT started.')
    await set_commands(bot)
    await dp.start_polling(bot)

    await close_db()

asyncio.run(main())
