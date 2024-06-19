import json

import requests
from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.text import account, account_ru
from bot.dispatcher import dp


@dp.message_handler(Text(equals=[account, account_ru]))
async def cabinet_menu_function_1(msg: types.Message):
    user = json.loads(requests.get(url=f"http://127.0.0.1:8000/students/chat_id/{msg.from_user.id}/").content)
    if msg.text == account:
        await msg.answer(text=f"""
""")
    else:
        await msg.answer(text=f"""
""")
