from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from music_provider import MusicProvider

router = Router()


@router.message(Command("producer"))
async def cmd_producer(message: Message):
    producer = MusicProvider.get_random_producer()
    if not producer:
        await message.answer("Пока нет статей о продюсерах. Попробуйте позже.")
        return

    text = f"🎛 *{producer.name}*\n\n"
    if producer.bio:
        text += f"{producer.bio}\n\n"
    if producer.wiki_url:
        text += f"🔗 [Подробнее]({producer.wiki_url})"
    await message.answer(text, parse_mode="Markdown")
