import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
from aiogram.types import Update
from fastapi.responses import JSONResponse
from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode="Markdown")
dp = Dispatcher(storage=MemoryStorage())

from handlers.common import register_common_handlers
register_common_handlers(dp)


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    logging.info("Bot is starting...")
    await bot.set_webhook(url=os.getenv("WEBHOOK_URL"))

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Bot is shutting down...")
    await bot.delete_webhook()
    await bot.session.close()


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.exception("Error processing update")
    return JSONResponse(content={"ok": True})


from handlers.common import register_common_handlers
register_common_handlers(dp)



