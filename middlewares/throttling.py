from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any, List
import datetime


class ThrottlingMessageMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.number_time_block = 30
        self.time_updates: dict[List[int, int, bool], datetime.datetime] = {}
        self.timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=3)
        self.time_block: datetime.timedelta = datetime.timedelta(seconds=self.number_time_block) # время в секундах, на которое будет заблокирован пользователь
        self.number_message: int = 4

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if user_id not in self.time_updates.keys():
            self.time_updates[user_id] = [1, datetime.datetime.now(), False]
            return await handler(event, data)
        elif self.time_updates[user_id][2] and (datetime.datetime.now() - self.time_updates[user_id][1]) <= self.time_block:
            return
        elif user_id in self.time_updates.keys():
            self.time_updates[user_id][0] += 1
            if self.time_updates[user_id][0] >= self.number_message and (datetime.datetime.now() - self.time_updates[user_id][1]) < self.timedelta_limiter:
                await event.answer(f"🚫 Ты заблокирован на {self.number_time_block} секунд за <b>спам</b>! В течении этого времени, бот тебя игнорирует!")
                self.time_updates[user_id] = [1, datetime.datetime.now(), True]
            elif self.time_updates[user_id][2] == True or self.time_updates[user_id][0] >= self.number_message:
                del self.time_updates[user_id]
                return await handler(event, data)
            else:
                return await handler(event, data)