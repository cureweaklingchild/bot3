from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from music_provider import MusicProvider

router = Router()

@router.message(Command("fact"))
async def cmd_fact(message: Message):
    fact = MusicProvider.get_random_fact()
    if not fact:
        await message.answer("Пока нет музыкальных фактов. Попробуйте позже.")
        return

    text = f"🎵 *Музыкальный факт:*\n\n{fact.text}"
    if fact.source:
        text += f"\n\n📖 Источник: {fact.source}"
    await message.answer(text, parse_mode="Markdown")