from aiogram import types, Router
from aiogram.filters.command import Command
from data.list_answer_bot import ANSWER_HELP


router = Router()


@router.message(Command("help"))
async def command_help_mes(message: types.Message):
    await message.answer(ANSWER_HELP)