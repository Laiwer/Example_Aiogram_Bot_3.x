from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Awaitable, Dict, Any
from db.base import existe_in_db, get_data_from_user


class SendStartMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if event.chat.type == "private":
            if (not existe_in_db("user", event.chat.id) or get_data_from_user(event.chat.id)[6] == 1) and event.text != "/start":
                await event.answer("ℹ Отправьте боту /start")
            else:
                return await handler(event, data)
        else:
            return


class SendStartCallbackQueryMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        if event.message.chat.type == "private":
            if (not existe_in_db("user", event.message.chat.id) or get_data_from_user(event.message.chat.id)[6] == 1):
                await event.answer("ℹ Отправьте боту /start", show_alert=True)
            else:
                return await handler(event, data)
        else:
            return