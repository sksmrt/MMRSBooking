from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import get_phone_kb, get_confirm_kb, get_admin_kb
from utils.inline_calendar import get_calendar_keyboard, build_calendar
from config import ADMIN_CHAT_ID

router = Router()

class Booking(StatesGroup):
    date = State()
    time = State()
    people = State()
    phone = State()
    name = State()
    confirm = State()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer("Привет! Чтобы забронировать столик, отправь команду /reserve")

@router.message(F.text == "/reserve")
async def cmd_reserve(message: Message, state: FSMContext):
    await message.answer("Выберите дату бронирования столика:", reply_markup=get_calendar_keyboard())
    await state.set_state(Booking.date)

@router.callback_query(F.data.startswith("day:"))
async def set_date(call: CallbackQuery, state: FSMContext):
    _, raw = call.data.split(":", 1)
    day, month, year = map(int, raw.split("."))
    formatted_date = f"{day:02d}.{month:02d}.{year}"
    await state.update_data(date=formatted_date)
    await call.message.answer("Отправьте время брони.\nФормат — ЧЧ:ММ\n❗️Мы работаем с 17:00, бронь на раннее время недоступна.")
    await state.set_state(Booking.time)

@router.callback_query(F.data.startswith("prev:") | F.data.startswith("next:"))
async def switch_month(call: CallbackQuery):
    _, month, year = call.data.split(":")
    markup = build_calendar(int(year), int(month))
    await call.message.edit_reply_markup(reply_markup=markup)
    await call.answer()

@router.message(Booking.time)
async def set_time(message: Message, state: FSMContext):
    time = message.text.strip()
    if not time or len(time) != 5 or ":" not in time:
        await message.answer("Неверный формат. Введите время в формате ЧЧ:ММ")
        return
    hour = int(time.split(":")[0])
    if hour < 17:
        await message.answer("Мы работаем с 17:00. Выберите более позднее время.")
        return
    await state.update_data(time=time)
    await message.answer("Сколько будет человек? Отправьте числом.")
    await state.set_state(Booking.people)

@router.message(Booking.people)
async def set_people(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, отправьте число.")
        return
    await state.update_data(people=int(message.text))
    await message.answer("Поделитесь номером телефона:", reply_markup=get_phone_kb())
    await state.set_state(Booking.phone)

@router.message(Booking.phone, F.contact)
async def set_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Введите ваше имя:")
    await state.set_state(Booking.name)

@router.message(Booking.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    text = (
        f"Информация о брони:\n\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}\n"
        f"Кол-во персон: {data['people']}\n\n"
        f"Имя: {data['name']}\n"
        f"Номер для связи: {data['phone']}"
    )
    await message.answer(text, reply_markup=get_confirm_kb())
    await state.set_state(Booking.confirm)

@router.callback_query(F.data == "confirm_send")
async def send_booking(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = (
        f"Информация о брони:\n\n"
        f"Дата: {data['date']}\n"
        f"Время: {data['time']}\n"
        f"Кол-во персон: {data['people']}\n\n"
        f"Имя: {data['name']}\n"
        f"Номер для связи: {data['phone']}"
    )
    await call.bot.send_message(ADMIN_CHAT_ID, text, reply_markup=get_admin_kb(call.from_user.id))
    await call.message.answer("Заявка отправлена! Ожидайте подтверждения.")
    await state.clear()

@router.callback_query(F.data == "restart")
async def restart_booking(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("Бронирование сброшено. Введите команду /reserve заново.")
