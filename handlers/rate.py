from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db import Session
from models import User, Rating, Track

router = Router()


@router.message(Command("rate"))
async def cmd_rate(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите оценку от 1 до 5.\nПример: /rate 4")
        return
    try:
        rating_value = int(args[1])
    except ValueError:
        await message.answer("Оценка должна быть числом от 1 до 5.")
        return
    if rating_value < 1 or rating_value > 5:
        await message.answer("Оценка должна быть от 1 до 5.")
        return

    user_tg_id = message.from_user.id
    session = Session()

    user = session.query(User).filter(User.tg_id == user_tg_id).first()
    if not user or not user.last_track_id:
        await message.answer("Вы ещё не получили ни одного трека. Используйте /random, чтобы начать.")
        session.close()
        return

    track_id = user.last_track_id
    track = session.query(Track).filter(Track.id == track_id).first()
    if not track:
        await message.answer("Ошибка: трек не найден. Попробуйте ещё раз /random.")
        session.close()
        return

    # Проверяем, есть ли уже оценка
    existing = session.query(Rating).filter(
        Rating.user_id == user.id,
        Rating.track_id == track_id
    ).first()

    if existing:
        existing.rating = rating_value
        await message.answer(f"Обновил вашу оценку для трека «{track.title}» на {rating_value}.")
    else:
        rating = Rating(
            user_id=user.id,
            track_id=track_id,
            genre_id=track.genre_id,
            rating=rating_value
        )
        session.add(rating)
        await message.answer(f"Оценка {rating_value} сохранена для трека «{track.title}».")

    session.commit()
    session.close()
