from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import admin
from db import add_user, add_order

router = Router()


class OrderState(StatesGroup):
    name = State()
    phone = State()
    description = State()


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Услуги и цены"), KeyboardButton(text="📝 Оформить заявку")],
        [KeyboardButton(text="ℹ️ О нас")]
    ],
    resize_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Поделиться контактом", request_contact=True)],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )
    await message.answer("Добро пожаловать! Выберите действие из меню:", reply_markup=main_kb)


@router.message(F.text == "❌ Отмена")
@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=main_kb)


@router.message(F.text == "📝 Оформить заявку")
async def start_order(message: types.Message, state: FSMContext):
    await state.set_state(OrderState.name)
    await message.answer("Как к вам обращаться?", reply_markup=ReplyKeyboardRemove())


@router.message(OrderState.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderState.phone)
    await message.answer("Отправьте ваш номер телефона (или нажмите кнопку ниже):", reply_markup=phone_kb)


@router.message(OrderState.phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone_number)

    await state.set_state(OrderState.description)
    await message.answer("Опишите вашу задачу или требуемую услугу:", reply_markup=ReplyKeyboardRemove())


@router.message(OrderState.description)
async def process_description(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    order_id = await add_order(
        user_id=message.from_user.id,
        name=user_data['name'],
        phone=user_data['phone'],
        description=message.text
    )
    await state.clear()
    await message.answer(f"Спасибо! Заявка #{order_id} принята. Менеджер свяжется с вами.", reply_markup=main_kb)
    if admin:
        admin_text = (
            f"🔔 **Новая заявка #{order_id}!**\n\n"
            f"👤 **Имя:** {user_data['name']}\n"
            f"📞 **Телефон:** {user_data['phone']}\n"
            f"📝 **Задача:** {message.text}"
        )
        await message.bot.send_message(chat_id=admin, text=admin_text, parse_mode="Markdown")
