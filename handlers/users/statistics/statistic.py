from aiogram import types, Router, F
from db.base import count_all_bot_users, count_active_bot_users, count_time_work_bot 
from keyboards.inline.statistics.statistics_kb import statistics_inline_keyboard
from keyboards.callbacks.statistics.statistics import Statistics
from aiogram.exceptions import TelegramBadRequest


router = Router()


async def statistics_text() -> str:
    time = ""
    timee = count_time_work_bot()
    if timee[0] == 0:
        if timee[1] == 0:
            time += f"{timee[2]} ч. {0 if timee[3] < 0 else timee[3]} мин."
        else:
            time += f"{timee[1]} дн. {timee[2]} ч."
    else:
        time += f"{timee[0]} мес. {timee[1]} дн."
    text = f"👥 <b><i>Всего пользователей бота:</i>\n\t\t\t\t\t\t{count_all_bot_users():,} чел.</b>"
    text += f"\n\n📆 <b><i>Пользователи бота за последние сутки:</i>\n\t\t\t\t\t\t{count_active_bot_users('l'):,} чел.</b>"
    text += f"\n\n⏰ <b><i>Бот работает:</i>\n\t\t\t\t\t\t{time}</b>"
    return text


@router.callback_query(Statistics.filter(F.process == "update_statistics"))
async def statistics_category(call: types.CallbackQuery):
    await call.answer()
    msg = await statistics_text()
    try:
        await call.message.edit_text(msg, reply_markup=statistics_inline_keyboard())
    except TelegramBadRequest:
        pass
