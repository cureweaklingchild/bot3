from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from db import Session
from models import User
from recommendation import RecommendationEngine
from keyboards import track_buttons
import logging

scheduler = AsyncIOScheduler()

async def send_daily_picks(bot):
    """Отправляет случайный трек всем подписанным пользователям"""
    session = Session()
    subscribers = session.query(User).filter(User.is_subscribed == 1).all()
    session.close()

    if not subscribers:
        logging.info("Нет подписанных пользователей")
        return

    for user in subscribers:
        try:
            genre, track = RecommendationEngine.get_random_recommendation()
            if not track:
                logging.warning(f"Нет трека для пользователя {user.tg_id}")
                continue

            # Сохраняем трек как последний для пользователя (чтобы можно было оценить)
            session = Session()
            db_user = session.query(User).filter(User.id == user.id).first()
            if db_user:
                db_user.last_track_id = track.id
                session.commit()
            session.close()

            text = (f"🎵 *{track.title}*\n"
                    f"🎤 {track.artist}\n"
                    f"🎸 Жанр: *{genre.name}*\n"
                    f"📖 {genre.description or ''}\n"
                    f"🔗 [Ссылка]({track.url})" if track.url else f"🎵 *{track.title}*\n🎤 {track.artist}\n🎸 Жанр: *{genre.name}*")
            await bot.send_message(chat_id=user.tg_id, text=text, parse_mode="Markdown", reply_markup=track_buttons())
        except Exception as e:
            logging.error(f"Ошибка отправки подборки пользователю {user.tg_id}: {e}")

def setup_scheduler(bot):
    scheduler.add_job(
        send_daily_picks,
        CronTrigger(hour=10, minute=0),   # каждый день в 10:00
        args=[bot],
        id="daily_picks",
        replace_existing=True
    )
    scheduler.start()
    logging.info("Планировщик ежедневной подборки запущен")