import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db import init_db
from handlers import start, random, rate, history, producer, fact, callback, subscribe, top  # добавляем импорты
from scheduler import setup_scheduler

async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(random.router)
    dp.include_router(rate.router)
    dp.include_router(history.router)
    dp.include_router(producer.router)
    dp.include_router(fact.router)
    dp.include_router(callback.router)
    dp.include_router(subscribe.router)
    dp.include_router(top.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    setup_scheduler(bot)

if __name__ == "__main__":
    asyncio.run(main())
