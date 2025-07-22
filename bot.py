import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import from_url
from fastapi import FastAPI, Request
from aiogram.types import Update
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import asyncio


load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode="Markdown")
redis = from_url("rediss://default:ATl7AAIjcDEwYjdkZjhmYTczNjk0YzZmOWY4Zjg0ODE4NmU1YTcwN3AxMA@ideal-pegasus-14715.upstash.io:6379")
storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)


from handlers.common import register_common_handlers
from handlers.life_path import router as life_path_router
from handlers.soul_urge import router as soul_urge_router
from handlers.personality import router as personality_router
from handlers.birthday import router as birthday_router
from handlers.expression import router as expression_router
from handlers.destiny import router as destiny_router


register_common_handlers(dp)
dp.include_router(life_path_router)
dp.include_router(soul_urge_router)
dp.include_router(personality_router)
dp.include_router(birthday_router)
dp.include_router(expression_router)
dp.include_router(destiny_router)


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    logging.info("🚀 Bot is starting...")
    print("📡 Setting webhook to:", os.getenv("WEBHOOK_URL"))
    try:
        result = await bot.set_webhook(url=os.getenv("WEBHOOK_URL"))
        print("✅ Webhook set result:", result)
    except Exception as e:
        print("❌ Failed to set webhook")
        import traceback
        traceback.print_exc()

    # 🛡 Safety: keep the event loop alive
    asyncio.create_task(idle_loop())


async def idle_loop():
    while True:
        await asyncio.sleep(3600)


@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Bot is shutting down...")
    await bot.delete_webhook()
    await bot.session.close()


@app.get("/")
async def root():
    return {"status": "Futuredigits bot is running"}


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        import traceback
        print("🔥 UNHANDLED ERROR:")
        traceback.print_exc()
    return JSONResponse(content={"ok": True})






