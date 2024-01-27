from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.filters.command import Command
from data.data_config import ADMINS, ADMIN_PASSWORD
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from db.base import count_recently_bot_users, count_active_bot_users, get_all_user_id, get_data_from_user


class AdminStates(StatesGroup):
    m_all = State()
    m_id = State()
    s_user = State()


router = Router()


@router.message(Command("admin"), F.from_user.id == int(ADMINS[0]), F.text.split(" ")[1] == ADMIN_PASSWORD)
async def admin_main(message: Message):
    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💬 ВСЕМ", callback_data="admin_message_all_" + ADMIN_PASSWORD)],
            [InlineKeyboardButton(text="💬 По ID", callback_data="admin_message_id_" + ADMIN_PASSWORD)],
            [InlineKeyboardButton(text="📊 Бота", callback_data="admin_stats_bot_" + ADMIN_PASSWORD)],
            [InlineKeyboardButton(text="🪪 По ID", callback_data="admin_stats_user_" + ADMIN_PASSWORD)],
            [InlineKeyboardButton(text="📁 Log", callback_data="admin_info_file_" + ADMIN_PASSWORD)],
        ]
    )
    await message.delete()
    await message.answer("1010100101010101", reply_markup=admin_kb)


@router.callback_query(F.data.contains(ADMIN_PASSWORD), F.from_user.id == int(ADMINS[0]))
async def admin_commands(call: CallbackQuery, state: FSMContext):
    await call.answer()
    msg = ""
    if call.data == "admin_message_all_" + ADMIN_PASSWORD:
        await state.set_state(AdminStates.m_all)
        await call.message.delete()
        msg = "Введити сообщение:"
    elif call.data == "admin_message_id_" + ADMIN_PASSWORD:
        await state.set_state(AdminStates.m_id)
        await call.message.delete()
        msg = "Введити ID(&)сообщение:"
    elif call.data == "admin_stats_bot_" + ADMIN_PASSWORD:
        await admin_stats_bot_for_admin(call.message)
        return
    elif call.data == "admin_stats_user_" + ADMIN_PASSWORD:
        await state.set_state(AdminStates.s_user)
        await call.message.delete()
        msg = "Введити ID:"
    elif call.data == "admin_info_file_" + ADMIN_PASSWORD:
        await admin_info_file_for_admin(call.message)
        return
    await call.message.answer(msg)


def admin_text_stats_bot_for_admin():
    text = f"⏳ <b><i>Пользователи бота за последний час:</i>\n\t\t\t\t\t\t{count_recently_bot_users('l'):,} чел.</b>"
    text += f"\n\n👋 <b><i>Новые пользователи бота за последний час:</i>\n\t\t\t\t\t\t{count_recently_bot_users('j'):,} чел.</b>"
    text += f"\n\n✅ <b><i>Новые пользователи бота за последние сутки:</i>\n\t\t\t\t\t\t{count_active_bot_users('j'):,} чел.</b>"
    return text


async def admin_stats_bot_for_admin(message: Message):
    msg = admin_text_stats_bot_for_admin()
    await message.delete()
    await message.answer(msg, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Обновить", callback_data="admin_update_stats_bot")]]))


@router.callback_query(F.data == "admin_update_stats_bot")
async def admin_update_stats_bot_for_admin(call: CallbackQuery):
    await call.answer()
    msg = admin_text_stats_bot_for_admin()
    try:
        await call.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Обновить", callback_data="admin_update_stats_bot")]]))
    except TelegramBadRequest:
        pass


async def admin_info_file_for_admin(message: Message):
    info = FSInputFile(path="utils\\misc\\bot.log", filename="info.log")
    await message.delete()
    await message.answer_document(info)


@router.message(AdminStates.m_all)
async def admin_message_all_for_admin(message: Message, state: FSMContext, bot: Bot):
    user_ids = get_all_user_id()
    for i in user_ids:
        bot.parse_mode = None
        await bot.send_message(i[0], text=message.text, entities=message.entities, link_preview_options=message.link_preview_options, reply_markup=message.reply_markup)
        bot.parse_mode = "HTML"
    await state.clear()


@router.message(AdminStates.m_id)
async def admin_message_id_for_admin(message: Message, state: FSMContext, bot: Bot):
    texts = message.text.split("&")
    await bot.send_message(texts[0], texts[1])
    await message.answer("Отправлено")
    await state.clear()


@router.message(AdminStates.s_user)
async def admin_stats_user_for_admin(message: Message, state: FSMContext):
    try:
        data = get_data_from_user(int(message.text))[:-1]
        msg = f"Инфа по юзеру @{data[2]}:"
        for i in data:
            msg += f"\n{i}"
        await message.answer(msg)
        await state.clear()
    except TypeError:
        await message.answer("Нет такого юзера!")
        await state.clear()