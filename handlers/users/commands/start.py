from aiogram import types, Router
from aiogram.filters.command import CommandStart
from aiogram import types
from db.base import existe_in_db, add_user_in_data_base, update_send_start


router = Router()


@router.message(CommandStart())
async def bot_start(message: types.Message):
    update_send_start(message.chat.id, 0)
    if not existe_in_db("user", message.chat.id):
        add_user_in_data_base(message.chat.id, message.from_user.username, message.from_user.full_name)

    msg = f"Привет <b>{message.from_user.full_name}</b>!"
    await message.answer(msg)