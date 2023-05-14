import asyncio
from create_bot import bot, dp
from handlers import commands, inline


async def main():
    print('Bot online')

    # Инициализация роутеров
    dp.include_router(commands.router)
    dp.include_router(inline.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
