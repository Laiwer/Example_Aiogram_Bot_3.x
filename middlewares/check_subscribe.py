from aiogram import BaseMiddleware
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from keyboards.inline.subscribe_channel.subscribe_channel_kb import channel_inline_keyboard
from typing import Callable, Dict, Any, Awaitable
import uuid


CHANNEL_ID = "" # int or @username
CHANNEL_NAME = ""


class CheckingSubscribeOnChannel(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        chat_member = await data["bot"].get_chat_member(chat_id=CHANNEL_ID, user_id=event.chat.id)
        if chat_member.status != "left":
            return await handler(event, data)
        else:
            await event.answer(f"⬇ Для продолжения подпишись на <b><i>{CHANNEL_NAME}</i></b> и снова отправь /start", reply_markup=channel_inline_keyboard())


class CheckingSubscribeOnChannelInlineMode(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[InlineQuery, Dict[str, Any]], Awaitable[Any]],
        event: InlineQuery,
        data: Dict[str, Any]
    ) -> Any:
        chat_member = await data["bot"].get_chat_member(chat_id=CHANNEL_ID, user_id=event.from_user.id)
        if chat_member.status != "left":
            return await handler(event, data)
        else:
            result = [
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="⬆️ Перейди в бота по кнопке выше",
                    description=f'Отправь боту /start и подпишись на канал {CHANNEL_NAME}, чтобы пользоваться ботом',
                    input_message_content=InputTextMessageContent(message_text=f"Отправь боту /start и подпишись на канал {CHANNEL_NAME}, чтобы пользоваться ботом"),
                    thumbnail_url="https://em-content.zobj.net/source/apple/354/loudspeaker_1f4e2.png",
                    thumbnail_height=160,
                    thumbnail_width=160
            )
            ]
            await event.answer(result, cache_time=1, is_personal=True, switch_pm_text="Перейти в бота", switch_pm_parameter="i")