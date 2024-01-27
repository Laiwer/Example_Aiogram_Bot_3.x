from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def nothing_message_handler(message: Message):
    await message.answer("🤷 <b>Я тебя не понял.</b> 🤷\nИспользуй команду /start,\nчтобы пользоваться ботом.")