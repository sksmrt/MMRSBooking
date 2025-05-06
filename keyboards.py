from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

def get_phone_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться номером", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_confirm_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отправить", callback_data="confirm_send")],
            [InlineKeyboardButton(text="Заполнить заново", callback_data="restart")]
        ]
    )

def get_admin_kb(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить", callback_data=f"admin_confirm:{user_id}")],
            [InlineKeyboardButton(text="Отклонить", callback_data=f"admin_reject:{user_id}")]
        ]
    )
