from aiogram.filters.callback_data import CallbackData


class Statistics(CallbackData, prefix="statistics"):
    process: str