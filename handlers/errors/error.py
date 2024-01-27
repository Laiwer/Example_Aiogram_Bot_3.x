from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramNotFound
import logging


router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    # if isinstance(event.exception, TelegramNotFound):
    #     logging.warning(msg=event.exception)
    # else:
    logging.error(msg=event.exception, exc_info=True)