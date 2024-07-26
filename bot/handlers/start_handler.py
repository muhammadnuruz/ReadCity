import json
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from bot.buttons.inline_buttons import language_buttons
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back_main_menu, back_main_menu_ru, choice_language, choice_language_ru
from bot.dispatcher import dp, bot
from main import admins

audio_file_id_1 = 'CQACAgIAAxkBAAIBc2ZsQDWviJTcl5mRWTiTU6-RpChdAAIXSQACX3v5SkChV37J5Z5lNQQ'
audio_file_id_2 = 'CQACAgIAAxkBAAIBdWZsQF8oeYEoa_Zs3hvoqmK61pSdAAIjSQACX3v5StkZXQN_HfsKNQQ'
audio_file_id_3 = 'CQACAgIAAxkBAAIBd2ZsQHY55n3Wo1cRMNEuSz5mA2CHAAIlSQACX3v5Sn0mFW4xzobTNQQ'
audio_file_id_4_1 = 'CQACAgIAAxkBAAICdWaI26u3YbbTNaxGAsSUoaGD7cdPAAIdSQACX3v5SuFCZV8zAeBFNQQ'
audio_file_id_4_2 = 'CQACAgIAAxkBAAICdmaI26t8s8qLwy7mbXQchsNWsvOzAAIfSQACX3v5Srg_JBASx1HKNQQ'
audio_file_id_5 = 'CQACAgIAAxkBAAICeWaI2-JKKLL24wVCjcNZx9lIkY6fAALlSgAC58dASA46Z_BaUqXrNQQ'


@dp.message_handler(content_types=types.ContentType.AUDIO)
async def handle_audio(msg: types.Message):
    audio = msg.audio
    file_id = audio.file_id
    print(file_id)
    await msg.reply(file_id)


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru]))
async def back_main_menu_function_1(msg: types.Message):
    await msg.answer(text=f"""
/start buyrug'ini yuboring ❗

----------------------------

Отправьте команду /start ❗""", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals=[back_main_menu, back_main_menu_ru]),
                    state=['test_performance_1', 'test_performance_2'])
async def back_main_menu_function_1(msg: types.Message, state: FSMContext):
    if msg.text == back_main_menu:
        await msg.answer(text=f"Asosiy menu🏠", reply_markup=await main_menu_buttons(msg.from_user.id))
    else:
        await msg.answer(text=f"Главное меню🏠", reply_markup=await main_menu_buttons(msg.from_user.id))
    await state.finish()


@dp.message_handler(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8001/telegram-users/chat_id/{msg.from_user.id}/").content)
    deep_user = msg.get_args()
    if deep_user != "":
        await state.set_state('language_1')
        await msg.answer(text="""
Tilni tanlang

-------------

Выберите язык""", reply_markup=await language_buttons())
        async with state.proxy() as data:
            data["qr_code"] = deep_user
        try:
            if tg_user['detail']:
                for admin in admins:
                    await bot.send_message(chat_id=admin, text=f"""
Yangi user🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism-Familiya: {msg.from_user.full_name}
Username: @{msg.from_user.username}\n""", parse_mode='HTML')
                data = {
                    "chat_id": str(msg.from_user.id),
                    "username": msg.from_user.username,
                    "full_name": msg.from_user.full_name,
                    "language": 'uz'
                }
                requests.post(url=f"http://127.0.0.1:8001/telegram-users/create/", data=data)
        except KeyError:
            pass


@dp.callback_query_handler(Text(startswith='language_'), state='language_1')
async def language_function(call: types.CallbackQuery, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8001/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    requests.put(url=f"http://127.0.0.1:8001/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    await state.set_state('register_1')
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text=f"Ism-Familiyangizni kiriting ✍️:")
    else:
        await call.message.answer(text=f"Введите свое имя и фамилию ✍️:")


@dp.message_handler(state='register_1')
async def register_function(msg: types.Message, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8001/telegram-users/chat_id/{msg.from_user.id}/").content)
    async with state.proxy() as data:
        data['full_name'] = msg.text
    k = KeyboardButton(text="MY NUMBER📲", request_contact=True)
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb_client.add(k)
    await state.set_state("register_2")
    if tg_user.get('language') == 'uz':
        await msg.answer(text="«MY NUMBER📲» - tugmasini bosish orqali telefon raqamingizni yuboring 👇",
                         reply_markup=kb_client)
    else:
        await msg.answer(text="Укажите свой номер телефона, нажав кнопку «MY NUMBER📲» 👇", reply_markup=kb_client)


@dp.message_handler(state='register_2', content_types='contact')
async def phone_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = msg.contact.phone_number
    data = {
        "full_name": data['full_name'],
        "phone_number": data['phone_number']
    }
    tg_user = json.loads(
        requests.get(url=f"http://127.0.0.1:8001/telegram-users/chat_id/{msg.from_user.id}/").content)
    requests.patch(url=f"http://127.0.0.1:8001/telegram-users/update/{tg_user['id']}/", data=data)
    async with state.proxy() as data:
        if 'qr_code' in data and data['qr_code'].startswith("listening"):
            key, key2, key3, key4 = data['qr_code'].split("_")
            audio_file_id = ''
            if int(key3) == 1:
                audio_file_id = audio_file_id_1
            elif int(key3) == 2:
                audio_file_id = audio_file_id_2
            elif int(key3) == 3:
                audio_file_id = audio_file_id_3
            elif int(key3) == 4:
                audio_file_id = audio_file_id_4_2
                await bot.send_audio(chat_id=msg.from_user.id, audio=audio_file_id_4_1, protect_content=True)
            elif int(key3) == 5:
                audio_file_id = audio_file_id_5
            await bot.send_audio(chat_id=msg.from_user.id, audio=audio_file_id, protect_content=True)
            message = await msg.answer(text="Audio",
                                       reply_markup=await main_menu_buttons(msg.from_user.id))
            await message.delete()
        else:
            key, key2, key3 = data['qr_code'].split("_")
            book = ""
            if int(key2) == 1:
                book = 'Beauty and the Beast'
            elif int(key2) == 2:
                book = 'Poor Millionaire'
            elif int(key2) == 3:
                book = 'Titanic'
            elif int(key2) == 4:
                book = 'Jack and Beanstalk & Green eyes'
            elif int(key2) == 5:
                book = 'Japan'
            if tg_user.get('language') == 'uz':
                await msg.answer(text="Tez orada siz bilan aloqaga chiqamiz 😊",
                                 reply_markup=ReplyKeyboardRemove())
            else:
                await msg.answer(text="Мы скоро свяжемся с вами 😊",
                                 reply_markup=ReplyKeyboardRemove())
            for admin in admins:
                await bot.send_message(chat_id=admin, text=f"""
{book} - kitobi uchun yangi haridor 🆕

Ism-Familiya: {data['full_name']}
Telefon raqam: {data['phone_number']}""")
    await state.finish()


@dp.message_handler(Text(equals=[choice_language, choice_language_ru]))
async def change_language_function_1(msg: types.Message, state: FSMContext):
    await state.set_state('language_2')
    if msg.text == choice_language:
        await msg.answer(text="Tilni tanlang", reply_markup=await language_buttons())
    else:
        await msg.answer(text="Выберите язык", reply_markup=await language_buttons())


@dp.callback_query_handler(Text(startswith='language_'), state='language_2')
async def language_function_1(call: types.CallbackQuery, state: FSMContext):
    tg_user = json.loads(requests.get(url=f"http://127.0.0.1:8001/telegram-users/chat_id/{call.from_user.id}/").content)
    data = {
        "chat_id": str(call.from_user.id),
        "username": call.from_user.username,
        "full_name": call.from_user.full_name,
        "language": call.data.split("_")[-1]
    }
    requests.put(url=f"http://127.0.0.1:8001/telegram-users/update/{tg_user['id']}/", data=data)
    await call.message.delete()
    if call.data.split("_")[-1] == 'uz':
        await call.message.answer(text="Til o'zgartirildi 🇺🇿", reply_markup=await main_menu_buttons(call.from_user.id))
    else:
        await call.message.answer(text="Язык изменен 🇷🇺", reply_markup=await main_menu_buttons(call.from_user.id))
    await state.finish()
