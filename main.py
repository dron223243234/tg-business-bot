import asyncio
from aiogram import Bot, Dispatcher
from config import token
from db import init_db
from handlers import router
from aiogram.client.session.aiohttp import AiohttpSession


async def main():
    await init_db()
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


