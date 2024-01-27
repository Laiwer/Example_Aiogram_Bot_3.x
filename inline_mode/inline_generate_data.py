from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import uuid


router = Router()


@router.inline_query()
async def inline_mode_handler(inline_query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Title",
            description='description',
            input_message_content=InputTextMessageContent(message_text="message_text"),
            thumbnail_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Telegram_2019_Logo.svg/1200px-Telegram_2019_Logo.svg.png",
            thumbnail_height=1,
            thumbnail_width=1
        )
    ]
    await inline_query.answer(results, cache_time=1, is_personal=True, switch_pm_text="Перейти в бота", switch_pm_parameter="-")