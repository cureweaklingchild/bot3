from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db import Session
from models import User, Rating, Track

router = Router()


@router.message(Command("history"))
async def cmd_history(message: Message):
    user_tg_id = message.from_user.id
    session = Session()

    user = session.query(User).filter(User.tg_id == user_tg_id).first()
    if not user:
        await message.answer("У вас пока нет оценок. Используйте /random и /rate, чтобы начать.")
        session.close()
        return


    ratings = session.query(Rating).filter(Rating.user_id == user.id) \
        .order_by(Rating.timestamp.desc()).limit(10).all()

    if not ratings:
        await message.answer("Вы ещё не оценили ни одного трека.")
        session.close()
        return

    history_text = "📊 *Ваши последние оценки:*\n\n"
    for r in ratings:
        track = session.query(Track).filter(Track.id == r.track_id).first()
        if track:
            date_str = r.timestamp.strftime("%d.%m.%Y %H:%M")
            history_text += f"🎵 {track.title} — {track.artist}\n"
            history_text += f"   Жанр: {track.genre.name if track.genre else '?'}\n"
            history_text += f"   Оценка: {'⭐' * r.rating} ({r.rating}/5)\n"
            history_text += f"   {date_str}\n\n"

    session.close()
    await message.answer(history_text, parse_mode="Markdown")
