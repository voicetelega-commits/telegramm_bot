import os
import asyncio
from aiogram import Bot, Dispatcher
import logging
from dotenv import load_dotenv


from handlers.start import router as start_router
from handlers.pars_menu import router as pars_router
from handlers.search_chat import router as search_chat_router


load_dotenv()
logging.basicConfig(level=logging.INFO)


async def main():
    bot_token = os.getenv('BOT_TOKEN')


    try:
        print("🚀 Запускаю бота...")
        bot = Bot(token=bot_token)
        dp = Dispatcher()

        dp.include_router(start_router)
        dp.include_router(pars_router)
        dp.include_router(search_chat_router)

        print("✅ Бот инициализирован")
        print("🔄 Запуск поллинг...")
        await bot.delete_webhook(drop_pending_updates=True)

        print("✅ Бот запущен и готов к работе!")
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Ошибка запуска: {e}')


if __name__ == "__main__":
    try:
        print("🤖 TELEGRAM BOT")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("STOP WORK BOT")
