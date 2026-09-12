import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv("BOT_API")
admin_ids = [int(admin_id) for admin_id in os.getenv('ADMIN_IDS').split(',')]
bot_version = '0.1.1'

if not bot_key:
    raise ValueError('Bot API key not found. Check the .env file.')