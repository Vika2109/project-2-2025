import asyncio
import logging
from aiogram import Bot, Dispatcher

from config.settings import TELEGRAM_TOKEN
from routers import commands, callbacks
from utils.logger import setup_logger


async def main():
    # Настройка логгера
    setup_logger()
    
    # Инициализация бота и диспетчера
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    
    # Подключение роутеров
    dp.include_router(commands.router) 
    dp.include_router(callbacks.router)

    
    
    # Запуск поллинга
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())