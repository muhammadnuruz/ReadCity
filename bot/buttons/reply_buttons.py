import json

import requests
from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import back_main_menu, adverts, none_advert, forward_advert, back_admin_menu, back_main_menu_ru, \
    choice_language, choice_language_ru


async def main_menu_buttons(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8001/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [
            [choice_language]
        ]
    else:
        design = [
            [choice_language_ru]
        ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_button(chat_id: int):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8001/telegram-users/chat_id/{chat_id}/").content)
    if tg_user['language'] == 'uz':
        design = [[back_main_menu]]
    else:
        design = [[back_main_menu_ru]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_admin_menu_button():
    design = [[back_admin_menu]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_menu_buttons():
    design = [
        [adverts],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def advert_menu_buttons():
    design = [
        [none_advert, forward_advert],
        [back_admin_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
