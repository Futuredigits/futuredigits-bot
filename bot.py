import os
import logging
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

from db import redis
from localization import load_locales
from notifications import init_notifications, _scheduler as NOTIF_SCHED

load_dotenv()
load_locales()

app = FastAPI()

from dotenv import load_dotenv

bot: Bot | None = None
dp: Dispatcher | None = None


TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
storage = RedisStorage(redis)
dp = Dispatcher(storage=storage)


from handlers.common import register_common_handlers, hydrate_premium_cache
register_common_handlers(dp)

from handlers.life_path import router as life_path_router
from handlers.soul_urge import router as soul_urge_router
from handlers.personality import router as personality_router
from handlers.birthday import router as birthday_router
from handlers.expression import router as expression_router
from handlers.destiny import router as destiny_router
from handlers.passion_number import router as passion_router
from handlers.premium_karmic_debt import router as karmic_router
from handlers.premium_compatibility import router as compatibility_router
from handlers.premium_love_vibes import router as love_vibes_router
from handlers.premium_personal_year import router as personal_year_router
from handlers.premium_moon_energy import router as moon_energy_router
from handlers.premium_daily_vibe import router as daily_vibe_router
from handlers.premium_angel_number import router as angel_number_router
from handlers.premium_name_vibration import router as name_vibration_router
from handlers.admin import admin_router
from handlers.notify import notify_router

dp.include_router(life_path_router)
dp.include_router(soul_urge_router)
dp.include_router(personality_router)
dp.include_router(birthday_router)
dp.include_router(expression_router)
dp.include_router(destiny_router)
dp.include_router(passion_router)
dp.include_router(karmic_router)
dp.include_router(compatibility_router)
dp.include_router(love_vibes_router)
dp.include_router(personal_year_router)
dp.include_router(moon_energy_router)
dp.include_router(daily_vibe_router)
dp.include_router(angel_number_router)
dp.include_router(name_vibration_router)
dp.include_router(admin_router)
dp.include_router(notify_router)



@app.on_event("startup")
async def on_startup():
    logging.info("🚀 Bot is starting...")
    await hydrate_premium_cache()
    try:
        result = await bot.set_webhook(url=os.getenv("WEBHOOK_URL"))
        logging.info(f"📡 Webhook set: {result}")
    except Exception:
        logging.exception("❌ Failed to set webhook")

    try:
        sched = init_notifications(bot)
        logging.info(f"[notif] init returned: {sched}")
        if sched:
            for j in sched.get_jobs():
                logging.info(f"[notif] job={j.id} next={j.next_run_time}")
    except Exception:
        logging.exception("[notif] init failed")


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


async def choose_storage():
    try:
        storage = RedisStorage(redis=redis)
        logging.info("[redis] using RedisStorage")
    except Exception as e:
        logging.warning("[redis] not available (%s) -> MemoryStorage", e)
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)







