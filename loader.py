from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from data.data_config import BOT_TOKEN
from handlers.users.commands import start, admin, help, statistics
from handlers.users.statistics import statistic
from handlers.users import nothing
from handlers.errors import error
from inline_mode import inline_generate_data
from middlewares.check_subscribe import CheckingSubscribeOnChannel, CheckingSubscribeOnChannelInlineMode
from middlewares.throttling import ThrottlingMessageMiddleware
from middlewares.add_last_message import AddLastMessageMiddleware
from middlewares.send_start import SendStartMessageMiddleware, SendStartCallbackQueryMiddleware
from utils.notify_admins import on_startup_notify, on_shutdown_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(bot: Bot):
    await on_startup_notify(bot)


async def on_shutdown(bot: Bot):
    await on_shutdown_notify(bot)


async def start_bot():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    await set_default_commands(bot)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.inline_query.middleware.register(CheckingSubscribeOnChannelInlineMode())
    dp.message.middleware.register(SendStartMessageMiddleware())
    dp.callback_query.middleware.register(SendStartCallbackQueryMiddleware())
    dp.message.middleware.register(ThrottlingMessageMiddleware())
    dp.message.middleware.register(AddLastMessageMiddleware())
    dp.message.middleware.register(CheckingSubscribeOnChannel())

    dp.include_router(error.router)
    dp.include_router(inline_generate_data.router)
    dp.include_routers(
        start.router,
        admin.router,
        help.router,
        statistics.router,
    )
    dp.include_router(statistic.router)
    dp.include_router(nothing.router)
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()