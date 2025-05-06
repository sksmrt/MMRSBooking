import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties

from config import API_TOKEN
from handlers import booking, admin

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

dp.include_routers(booking.router, admin.router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/reserve", description="Забронировать столик"),
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
