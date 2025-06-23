import asyncio
from aiogram import Bot

TOKEN = "8152160829:AAGCBS4xyB9dhJjMf81LQM2uY9FlwlD4BYg"  # Your token in quotes

async def clear_webhook():
    bot = Bot(token=TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook cleared.")
    await bot.session.close()

asyncio.run(clear_webhook())
