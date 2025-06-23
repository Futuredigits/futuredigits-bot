import asyncio
from aiogram import Bot

TOKEN = "8152160829:AAGCBS4xyB9dhJjMf81LQM2uY9FlwlD4BYg"

async def force_reset():
    bot = Bot(token=TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.get_updates(offset=-1)  # ⛔ Force-terminate old polling queue
    print("✅ Telegram session reset.")
    await bot.session.close()

asyncio.run(force_reset())
