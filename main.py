import logging
import asyncio
from aiogram import executor
from bot.handlers import *

admins = [1974800905, 93979910]


async def on_startup(dp):
    print("Bot is online!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup(dp))
    executor.start_polling(dp, skip_updates=True)
