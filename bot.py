import asyncio
from aiogram import Bot, Dispatcher
from config import Config, load_config
from handlers import other_handlers, user_handlers
# from aiogram.fsm.storage.redis import RedisStorage, Redis

# redis: Redis = Redis(host='localhost')
# storage: RedisStorage = RedisStorage(redis=redis)


async def main() -> None:
    config: Config = load_config()
    bot: Bot = Bot(token=config.bot_token.token)
    dp: Dispatcher = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
