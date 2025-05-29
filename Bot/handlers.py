from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardMarkup
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiohttp
import re

router_command = Router()

# Language-specific messages
LANGUAGES = {
    "uz": {
        "welcome": "Assalomu alaykum! 🤗 Botimizga xush kelibsiz! 🎉",
        "select_language": "Kerakli tilni tanlang 🌐",
        "enter_username": "Iltimos, foydalanuvchi nomingizni kiriting (3-30 belgi): 👤",
        "enter_last_name": "Iltimos, familiyangizni kiriting (2-50 belgi): 📝",
        "enter_age": "Iltimos, yoshingizni kiriting (raqamda, 13-150): 🎂",
        "enter_gender": "Iltimos, jinsingizni tanlang: 🚻",
        "enter_phone": "Iltimos, telefon raqamingizni ulashing: 📱",
        "enter_password": "Iltimos, parolingizni kiriting (kamida 6 belgi): 🔒\nParol bu siz va AI bilan suhbatlaringiz havfsiz va saqlanib borishi uchun kerak bo'ladi!",
        "registration_complete": "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi! 🎉 Sizning ma'lumotlaringiz:\n👤 Ism: {username}\n📝 Familiya: {last_name}\n🎂 Yosh: {age}\n🚻 Jins: {gender}\n📱 Telefon: {phone}",
        "error": "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring. 😔",
        "invalid_input": "Iltimos, to'g'ri ma'lumot kiriting. 😔",
        "invalid_phone_input": "Iltimos, 'Telefon raqamimni ulashish' tugmasini bosing va telefon raqamingizni ulashing. 😔",
        "server_error": "Serverda xatolik yuz berdi. Iltimos, ro'yxatdan o'tishni qaytadan boshlang. 😔"
    },
    "ru": {
        "welcome": "Здравствуйте! 🤗 Добро пожаловать в наш бот! 🎉",
        "select_language": "Выберите язык 🌐",
        "enter_username": "Пожалуйста, введите имя пользователя (3-30 символов): 👤",
        "enter_last_name": "Пожалуйста, введите вашу фамилию (2-50 символов): 📝",
        "enter_age": "Пожалуйста, введите ваш возраст (число, 13-150): 🎂",
        "enter_gender": "Пожалуйста, выберите пол: 🚻",
        "enter_phone": "Пожалуйста, поделитесь номером телефона: 📱",
        "enter_password": "Пожалуйста, введите пароль (минимум 6 символов): 🔒\nПароль необходим для безопасного хранения ваших разговоров с ИИ!",
        "registration_complete": "Регистрация успешно завершена! 🎉 Ваши данные:\n👤 Имя: {username}\n📝 Фамилия: {last_name}\n🎂 Возраст: {age}\n🚻 Пол: {gender}\n📱 Телефон: {phone}",
        "error": "Произошла ошибка. Пожалуйста, попробуйте снова. 😔",
        "invalid_input": "Пожалуйста, введите корректные данные. 😔",
        "invalid_phone_input": "Пожалуйста, нажмите кнопку 'Поделиться номером телефона' и отправьте ваш номер. 😔",
        "server_error": "Произошла ошибка на сервере. Пожалуйста, начните регистрацию заново. 😔"
    },
    "en": {
        "welcome": "Hello! 🤗 Welcome to our bot! 🎉",
        "select_language": "Please select a language 🌐",
        "enter_username": "Please enter your username (3-30 characters): 👤",
        "enter_last_name": "Please enter your last name (2-50 characters): 📝",
        "enter_age": "Please enter your age (number, 13-150): 🎂",
        "enter_gender": "Please select your gender: 🚻",
        "enter_phone": "Please share your phone number: 📱",
        "enter_password": "Please enter your password (minimum 6 characters): 🔒\nPassword is required to keep your conversations with AI secure and saved!",
        "registration_complete": "Registration completed successfully! 🎉 Your information:\n👤 Username: {username}\n📝 Last Name: {last_name}\n🎂 Age: {age}\n🚻 Gender: {gender}\n📱 Phone: {phone}",
        "error": "An error occurred. Please try again. 😔",
        "invalid_input": "Please enter valid information. 😔",
        "invalid_phone_input": "Please press the 'Share my phone number' button and share your phone number. 😔",
        "server_error": "A server error occurred. Please start the registration again. 😔"
    }
}

# Gender options for each language
VALID_GENDERS = {
    "uz": {"erkak": "Erkak", "ayol": "Ayol"},
    "ru": {"мужской": "Мужской", "женский": "Женский"},
    "en": {"male": "Male", "female": "Female"}
}

# Phone share button text for each language
PHONE_BUTTON_TEXT = {
    "uz": "Telefon raqamimni ulashish",
    "ru": "Поделиться номером телефона",
    "en": "Share my phone number"
}

# Chat button text for each language
CHAT_BUTTON_TEXT = {
    "uz": "Chatni boshlash",
    "ru": "Начать чат",
    "en": "Start chat"
}


class RegistrationStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_username = State()
    waiting_for_last_name = State()
    waiting_for_age = State()
    waiting_for_gender = State()
    waiting_for_phone = State()
    waiting_for_password = State()


async def send_message(message: Message, state: FSMContext, key: str, reply_markup=None, **kwargs):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")
    text = LANGUAGES[language][key].format(**kwargs)
    return await message.answer(text, reply_markup=reply_markup)


def create_gender_keyboard(language: str) -> InlineKeyboardMarkup:
    gender_options = VALID_GENDERS.get(language, VALID_GENDERS["uz"])
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=display_name, callback_data=gender_key)
                for gender_key, display_name in gender_options.items()
            ]
        ]
    )


def create_phone_keyboard(language: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=PHONE_BUTTON_TEXT[language], request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


@router_command.message(Command("start"))
async def bot_start(message: Message, state: FSMContext):
    await message.answer(
        LANGUAGES["uz"]["welcome"] + "\n" + LANGUAGES["uz"]["select_language"],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="uz"),
                    InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru"),
                    InlineKeyboardButton(text="🇬🇧 English", callback_data="en")
                ]
            ]
        )
    )
    await state.set_state(RegistrationStates.waiting_for_language)


@router_command.callback_query(F.data.in_(["uz", "ru", "en"]))
async def process_language(callback_query: CallbackQuery, state: FSMContext):
    language = callback_query.data
    await state.update_data(language=language)
    await send_message(callback_query.message, state, "enter_username")
    await state.set_state(RegistrationStates.waiting_for_username)
    await callback_query.answer()


@router_command.message(RegistrationStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()
    if not (3 <= len(username) <= 30 and username.isalnum()):
        await send_message(message, state, "invalid_input")
        return
    await state.update_data(username=username)
    await send_message(message, state, "enter_last_name")
    await state.set_state(RegistrationStates.waiting_for_last_name)


@router_command.message(RegistrationStates.waiting_for_last_name)
async def process_last_name(message: Message, state: FSMContext):
    last_name = message.text.strip()
    if not (2 <= len(last_name) <= 50 and all(c.isalpha() or c.isspace() for c in last_name)):
        await send_message(message, state, "invalid_input")
        return
    await state.update_data(last_name=last_name)
    await send_message(message, state, "enter_age")
    await state.set_state(RegistrationStates.waiting_for_age)


@router_command.message(RegistrationStates.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        if not (13 <= age <= 150):
            await send_message(message, state, "invalid_input")
            return
        await state.update_data(age=age)
        user_data = await state.get_data()
        language = user_data.get("language", "uz")
        await send_message(
            message,
            state,
            "enter_gender",
            reply_markup=create_gender_keyboard(language)
        )
        await state.set_state(RegistrationStates.waiting_for_gender)
    except ValueError:
        await send_message(message, state, "invalid_input")


@router_command.callback_query(F.data.in_(["erkak", "ayol", "мужской", "женский", "male", "female"]))
async def process_gender(callback_query: CallbackQuery, state: FSMContext):
    gender = callback_query.data
    user_data = await state.get_data()
    language = user_data.get("language", "uz")
    if gender not in VALID_GENDERS.get(language, VALID_GENDERS["uz"]):
        await send_message(callback_query.message, state, "invalid_input")
        return
    await state.update_data(gender=VALID_GENDERS[language][gender])
    await send_message(
        callback_query.message,
        state,
        "enter_phone",
        reply_markup=create_phone_keyboard(language)
    )
    await state.set_state(RegistrationStates.waiting_for_phone)
    await callback_query.answer()


@router_command.message(RegistrationStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")
    if not message.contact:
        await send_message(
            message,
            state,
            "invalid_phone_input",
            reply_markup=create_phone_keyboard(language)
        )
        return
    phone = message.contact.phone_number
    if not re.match(r"^\+998\d{9}$", phone):
        await send_message(
            message,
            state,
            "invalid_input",
            reply_markup=create_phone_keyboard(language)
        )
        return
    await state.update_data(phone=phone)
    await send_message(message, state, "enter_password")
    await state.set_state(RegistrationStates.waiting_for_password)


@router_command.message(RegistrationStates.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()
    if len(password) < 6:
        await send_message(message, state, "invalid_input")
        return
    await state.update_data(password=password)
    user_data = await state.get_data()
    language = user_data.get("language", "uz")

    # Prepare data for POST request
    payload = {
        "username": user_data["username"],
        "last_name": user_data["last_name"],
        "age": user_data["age"],
        "gender": user_data["gender"],
        "phone": user_data["phone"],
        "password": password
    }

    # Send POST request to the server
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:8000/users/", json=payload) as response:
                if response.status == 200:
                    # Successful registration
                    await send_message(
                        message,
                        state,
                        "registration_complete",
                        username=user_data["username"],
                        last_name=user_data["last_name"],
                        age=user_data["age"],
                        gender=user_data["gender"],
                        phone=user_data["phone"],
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text=CHAT_BUTTON_TEXT[language],
                                        callback_data="chat_symptoms"
                                    )
                                ]
                            ]
                        )
                    )
                    await state.clear()
                else:
                    # Server error, restart registration
                    await send_message(
                        message,
                        state,
                        "server_error",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="uz"),
                                    InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru"),
                                    InlineKeyboardButton(text="🇬🇧 English", callback_data="en")
                                ]
                            ]
                        )
                    )
                    await state.set_state(RegistrationStates.waiting_for_language)
    except aiohttp.ClientError:
        # Network or connection error, restart registration
        await send_message(
            message,
            state,
            "server_error",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="uz"),
                        InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru"),
                        InlineKeyboardButton(text="🇬🇧 English", callback_data="en")
                    ]
                ]
            )
        )
        await state.set_state(RegistrationStates.waiting_for_language)


@router_command.callback_query(F.data == "chat_symptoms")
async def chat(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    language = user_data.get("language", "uz")
    messages = {
        "uz": "Hurmatli bemor, menga🏣 o'z simptomlaringizni yuboring,\n Marhamat qilib 🧐!.............",
        "ru": "Уважаемый пациент, пожалуйста, отправьте мне свои симптомы!",
        "en": "Dear patient, please send me your symptoms!"
    }
    await callback_query.message.answer(messages[language])
    await callback_query.answer()


@router_command.message(RegistrationStates.waiting_for_language)
async def process_language(message: Message, state: FSMContext):
    ...
