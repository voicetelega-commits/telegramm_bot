import os
import asyncio
from aiogram import Bot, Dispatcher
import logging
from dotenv import load_dotenv



load_dotenv()

logging.basicConfig(level=logging.INFO)

async def main():
    bot_token = os.getenv('BOT_TOKEN')


    try:
        print("🚀 Запускаю бота...")
        bot = Bot(token=bot_token)
        dp = Dispatcher()

        print("✅ Бот инициализирован")
        print("🔄 Запуск поллинг...")
        await bot.delete_webhook(drop_pending_updates=True)

        print("✅ Бот запущен и готов к работе!")
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Ошибка запуска: {e}')


if __name__ == "__main__":
    try:
        print("🤖 TELEGRAM BOT Работает!")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("STOP WORK BOT")
