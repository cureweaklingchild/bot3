from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from recommendation import RecommendationEngine
from db import Session
from models import User
from keyboards import track_buttons   # убедись, что импорт есть

router = Router()

@router.message(Command("random"))
async def cmd_random(message: Message):
    session = Session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    if not user:
        user = User(tg_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()

    genre, track = RecommendationEngine.get_random_recommendation()
    if not track:
        await message.answer("Извините, пока нет треков в базе. Попробуйте позже.")
        session.close()
        return

    user.last_track_id = track.id
    session.commit()

    # Формируем текст. Убедись, что переменная text объявлена до ответа
    if track.url:
        text = (f"🎵 *{track.title}*\n"
                f"🎤 {track.artist}\n"
                f"🎸 Жанр: *{genre.name}*\n"
                f"📖 {genre.description or ''}\n"
                f"🔗 [Ссылка]({track.url})")
    else:
        text = (f"🎵 *{track.title}*\n"
                f"🎤 {track.artist}\n"
                f"🎸 Жанр: *{genre.name}*")

    await message.answer(text, parse_mode="Markdown", reply_markup=track_buttons())
    session.close()