import logging
from aiogram import Bot
from data import data_config


async def on_startup_notify(bot: Bot):
    for admin in data_config.ADMINS:
        try:
            await bot.send_message(admin, "✅ Bot turned #on")
        except Exception as err:
            logging.warning(err, exc_info=True)


async def on_shutdown_notify(bot: Bot):
    for admin in data_config.ADMINS:
        try:
            await bot.send_message(admin, "⛔️ Bot turned #off")
        except Exception as err:
            logging.warning(err, exc_info=True)