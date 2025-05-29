from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from handlers import router_command
import asyncio

load_dotenv()

bot = os.environ.get('BOT_TOKEN')
bot = Bot(token=bot)

dp = Dispatcher()
dp.include_router(router_command)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot is running...")
    asyncio.run(main())
    print("Bot stopped.")