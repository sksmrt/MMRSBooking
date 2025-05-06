from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta


def build_calendar(year: int, month: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[], row_width=7)

    # Дни недели
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    markup.inline_keyboard.append(
        [InlineKeyboardButton(text=day, callback_data="ignore") for day in days]
    )

    # Дни месяца
    first_day = datetime(year, month, 1)
    start_weekday = (first_day.weekday()) % 7
    if month == 12:
        total_days = 31
    else:
        total_days = (datetime(year, month + 1, 1) - timedelta(days=1)).day

    row = [InlineKeyboardButton(text=" ", callback_data="ignore")] * start_weekday
    for day in range(1, total_days + 1):
        row.append(InlineKeyboardButton(
            text=str(day),
            callback_data=f"day:{day}.{month}.{year}"
        ))
        if len(row) == 7:
            markup.inline_keyboard.append(row)
            row = []
    if row:
        markup.inline_keyboard.append(row)

    # Навигация
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    markup.inline_keyboard.append([
        InlineKeyboardButton(text="<<", callback_data=f"prev:{prev_month}:{prev_year}"),
        InlineKeyboardButton(text=f"{get_month_name(month)} {year}", callback_data="ignore"),
        InlineKeyboardButton(text=">>", callback_data=f"next:{next_month}:{next_year}")
    ])

    return markup


def get_calendar_keyboard():
    today = datetime.today()
    return build_calendar(today.year, today.month)


def get_month_name(month: int) -> str:
    months_ru = [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    return months_ru[month - 1]
