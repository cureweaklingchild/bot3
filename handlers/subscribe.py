from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db import Session
from models import User

router = Router()

@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message):
    session = Session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    if not user:
        user = User(tg_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
    user.is_subscribed = 1
    session.commit()
    session.close()
    await message.answer("✅ Вы подписались на ежедневную музыкальную подборку! Каждый день в 10:00 я буду присылать вам случайный трек.")

@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message):
    session = Session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    if user:
        user.is_subscribed = 0
        session.commit()
        await message.answer("❌ Вы отписались от ежедневной подборки.")
    else:
        await message.answer("Вы ещё не были подписаны.")
    session.close()