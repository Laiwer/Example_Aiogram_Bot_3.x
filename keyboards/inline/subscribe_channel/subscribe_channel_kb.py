from aiogram.utils.keyboard import InlineKeyboardBuilder


def channel_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="📢 Топовый канал", url="https://t.me/bots_rooms")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
