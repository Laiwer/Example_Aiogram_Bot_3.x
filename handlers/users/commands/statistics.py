from aiogram import types, Router
from keyboards.inline.statistics.statistics_kb import statistics_inline_keyboard
from handlers.users.statistics.statistic import statistics_text
from aiogram.filters.command import Command


router = Router()


@router.message(Command("statistics"))
async def statistics(message: types.Message):
    msg = await statistics_text()
    await message.answer(msg, reply_markup=statistics_inline_keyboard())
