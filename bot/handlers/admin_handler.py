from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import admin_menu_buttons
from bot.buttons.text import back_admin_menu
from bot.dispatcher import dp
from main import admins


@dp.message_handler(Text(back_admin_menu), state=['advert', 'send_forward'])
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    await msg.answer(text=f"Admin menu 👤", reply_markup=await admin_menu_buttons())
    await state.finish()


@dp.message_handler(commands='admin')
async def admin_handler_1(msg: types.Message):
    if msg.from_user.id in admins:
        await msg.answer(text="Admin menuga hush kelibsiz 😊", reply_markup=await admin_menu_buttons())
