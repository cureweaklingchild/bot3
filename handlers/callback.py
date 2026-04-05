from datetime import datetime, timedelta

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session

from db import Session
from keyboards import track_buttons, menu_buttons
from models import User, Rating, Track, Genre
from music_provider import MusicProvider
from recommendation import RecommendationEngine

router = Router()


@router.callback_query(lambda c: c.data.startswith("rate_"))
async def callback_rate(callback: CallbackQuery):
    rating_value = int(callback.data.split("_")[1])
    user_tg_id = callback.from_user.id

    session = Session()
    user = session.query(User).filter(User.tg_id == user_tg_id).first()
    if not user or not user.last_track_id:
        await callback.answer("Сначала получите трек через /random или кнопку", show_alert=True)
        session.close()
        return

    track = session.query(Track).filter(Track.id == user.last_track_id).first()
    if not track:
        await callback.answer("Трек не найден", show_alert=True)
        session.close()
        return

    existing = session.query(Rating).filter(
        Rating.user_id == user.id,
        Rating.track_id == track.id
    ).first()

    if existing:
        existing.rating = rating_value
        await callback.answer(f"Обновлена оценка для «{track.title}» → {rating_value}")
    else:
        rating = Rating(
            user_id=user.id,
            track_id=track.id,
            genre_id=track.genre_id,
            rating=rating_value
        )
        session.add(rating)
        await callback.answer(f"Оценка {rating_value} для «{track.title}» сохранена")

    session.commit()
    session.close()

    # Убираем кнопки с оценками, чтобы нельзя было оценить повторно
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(lambda c: c.data == "skip")
async def callback_skip(callback: CallbackQuery):
    session = Session()
    user = session.query(User).filter(User.tg_id == callback.from_user.id).first()
    if not user:
        user = User(tg_id=callback.from_user.id, username=callback.from_user.username)
        session.add(user)
        session.commit()

    genre, track = RecommendationEngine.get_random_recommendation()
    if not track:
        await callback.message.answer("Пока нет треков в базе")
        session.close()
        return

    user.last_track_id = track.id
    session.commit()

    text = (f"🎵 *{track.title}*\n🎤 {track.artist}\n🎸 Жанр: *{genre.name}*\n"
            f"📖 {genre.description or ''}\n"
            f"🔗 [Ссылка]({track.url})" if track.url else f"🎵 *{track.title}*\n🎤 {track.artist}\n🎸 Жанр: *{genre.name}*")
    session.close()

    # Редактируем текущее сообщение, показываем новый трек
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=track_buttons())
    await callback.answer()


@router.callback_query(lambda c: c.data == "fact")
async def callback_fact(callback: CallbackQuery):
    fact = MusicProvider.get_random_fact()
    if not fact:
        await callback.message.answer("Факты временно недоступны")
        return
    text = f"🎵 *Музыкальный факт:*\n\n{fact.text}"
    if fact.source:
        text += f"\n\n📖 Источник: {fact.source}"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=menu_buttons())
    await callback.answer()


@router.callback_query(lambda c: c.data == "producer")
async def callback_producer(callback: CallbackQuery):
    producer = MusicProvider.get_random_producer()
    if not producer:
        await callback.message.answer("Статьи о продюсерах временно недоступны")
        return
    text = f"🎛 *{producer.name}*\n\n{producer.bio or ''}"
    if producer.wiki_url:
        text += f"\n\n🔗 [Подробнее]({producer.wiki_url})"
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=menu_buttons())
    await callback.answer()


@router.callback_query(lambda c: c.data == "history")
async def callback_history(callback: CallbackQuery):
    user_tg_id = callback.from_user.id
    session = Session()
    user = session.query(User).filter(User.tg_id == user_tg_id).first()
    if not user:
        await callback.message.edit_text("У вас пока нет оценок. Оцените трек, чтобы они появились.",
                                         reply_markup=menu_buttons())
        session.close()
        await callback.answer()
        return

    ratings = session.query(Rating).filter(Rating.user_id == user.id) \
        .order_by(Rating.timestamp.desc()).limit(10).all()
    if not ratings:
        await callback.message.edit_text("Вы ещё не оценили ни одного трека.", reply_markup=menu_buttons())
        session.close()
        await callback.answer()
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
    await callback.message.edit_text(history_text, parse_mode="Markdown", reply_markup=menu_buttons())
    await callback.answer()


@router.callback_query(lambda c: c.data == "random")
async def callback_random(callback: CallbackQuery):
    session = Session()
    user = session.query(User).filter(User.tg_id == callback.from_user.id).first()
    if not user:
        user = User(tg_id=callback.from_user.id, username=callback.from_user.username)
        session.add(user)
        session.commit()

    genre, track = RecommendationEngine.get_random_recommendation()
    if not track:
        await callback.message.answer("Пока нет треков в базе")
        session.close()
        return

    user.last_track_id = track.id
    session.commit()

    text = (f"🎵 *{track.title}*\n🎤 {track.artist}\n🎸 Жанр: *{genre.name}*\n"
            f"📖 {genre.description or ''}\n"
            f"🔗 [Ссылка]({track.url})" if track.url else f"🎵 *{track.title}*\n🎤 {track.artist}\n🎸 Жанр: *{genre.name}*")
    session.close()

    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=track_buttons())
    await callback.answer()


@router.callback_query(lambda c: c.data == "share")
async def callback_share(callback: CallbackQuery):
    # Получаем последний трек пользователя (можно взять из БД)
    session = Session()
    user = session.query(User).filter(User.tg_id == callback.from_user.id).first()
    if not user or not user.last_track_id:
        await callback.answer("Сначала получите трек через /random или кнопку", show_alert=True)
        session.close()
        return
    track = session.query(Track).filter(Track.id == user.last_track_id).first()
    if not track:
        await callback.answer("Трек не найден", show_alert=True)
        session.close()
        return

    # Формируем текст для отправки
    share_text = (
        f"🎵 *{track.title}* — {track.artist}\n"
        f"🎸 Жанр: {track.genre.name if track.genre else '?'}\n"
        f"🔗 [Слушать]({track.url})" if track.url else f"🎵 *{track.title}* — {track.artist}"
    )
    # Отправляем пользователю сообщение, которое он может переслать
    await callback.message.answer(
        f"Вот информация о треке, которую можно отправить другу:\n\n{share_text}",
        parse_mode="Markdown"
    )
    await callback.answer("Готово! Теперь вы можете переслать это сообщение другу.")
    session.close()


@router.callback_query(lambda c: c.data == "topweek")
async def callback_topweek(callback: CallbackQuery):
    session = Session()
    week_ago = datetime.utcnow() - timedelta(days=7)

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
        await callback.message.edit_text("За последнюю неделю ещё нет оценок.", reply_markup=menu_buttons())
        session.close()
        await callback.answer()
        return

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

    top_tracks = []
    for track_id, data in stats.items():
        avg = data["total"] / data["count"]
        top_tracks.append((data["title"], data["artist"], data["genre"], avg, data["count"]))
    top_tracks.sort(key=lambda x: x[3], reverse=True)
    top_tracks = top_tracks[:5]

    text = "🏆 *Топ треков за неделю:*\n\n"
    for i, (title, artist, genre, avg, count) in enumerate(top_tracks, 1):
        text += f"{i}. *{title}* — {artist}\n"
        text += f"   Жанр: {genre}\n"
        text += f"   Рейтинг: {'⭐' * round(avg)} ({avg:.1f}/5) — {count} оценок\n\n"

    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=menu_buttons())
    session.close()
    await callback.answer()
