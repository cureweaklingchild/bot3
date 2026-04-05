from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db import Session
from models import Rating, Track, Genre
from datetime import datetime, timedelta

router = Router()

@router.message(Command("topweek"))
async def cmd_topweek(message: Message):
    session = Session()
    # Вычисляем дату 7 дней назад
    week_ago = datetime.utcnow() - timedelta(days=7)

    # Получаем оценки за последнюю неделю, группируем по треку
    results = (
        session.query(
            Track.title,
            Track.artist,
            Genre.name.label("genre_name"),
            Rating.track_id,
            Rating.rating
        )
        .join(Track, Rating.track_id == Track.id)
        .join(Genre, Track.genre_id == Genre.id)
        .filter(Rating.timestamp >= week_ago)
        .all()
    )

    if not results:
        await message.answer("За последнюю неделю ещё нет оценок.")
        session.close()
        return

    # Собираем статистику: для каждого track_id сумма оценок и количество
    stats = {}
    for row in results:
        track_id = row.track_id
        if track_id not in stats:
            stats[track_id] = {
                "title": row.title,
                "artist": row.artist,
                "genre": row.genre_name,
                "total": 0,
                "count": 0,
            }
        stats[track_id]["total"] += row.rating
        stats[track_id]["count"] += 1

    # Вычисляем средний рейтинг
    top_tracks = []
    for track_id, data in stats.items():
        avg = data["total"] / data["count"]
        top_tracks.append((data["title"], data["artist"], data["genre"], avg, data["count"]))

    # Сортируем по среднему рейтингу (убывание)
    top_tracks.sort(key=lambda x: x[3], reverse=True)
    top_tracks = top_tracks[:5]  # топ-5

    # Формируем текст
    text = "🏆 *Топ треков за неделю:*\n\n"
    for i, (title, artist, genre, avg, count) in enumerate(top_tracks, 1):
        text += f"{i}. *{title}* — {artist}\n"
        text += f"   Жанр: {genre}\n"
        text += f"   Рейтинг: {'⭐' * round(avg)} ({avg:.1f}/5) — {count} оценок\n\n"

    session.close()
    await message.answer(text, parse_mode="Markdown")