import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import token

from keep_live import keep_live

from handlers.user import router

# keep_live()

async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Error')