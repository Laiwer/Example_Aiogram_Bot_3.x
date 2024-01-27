from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.callbacks.statistics.statistics import Statistics


def statistics_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="🔄 Обновить статистику", callback_data=Statistics(process="update_statistics"))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
