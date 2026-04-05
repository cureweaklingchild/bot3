from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def track_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(1, 6):
        builder.button(text=str(i), callback_data=f"rate_{i}")
    builder.button(text="⏭ Пропустить", callback_data="skip")
    builder.button(text="📤 Поделиться", callback_data="share")
    builder.button(text="🎲 Случайный факт", callback_data="fact")
    builder.button(text="🎛 Случайный продюсер", callback_data="producer")
    builder.button(text="📊 Мои оценки", callback_data="history")
    builder.button(text="🏆 Топ недели", callback_data="topweek")
    builder.adjust(5, 1, 3, 1)
    return builder.as_markup()

def menu_buttons() -> InlineKeyboardMarkup:
    """Кнопки для фактов, продюсеров и истории"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🎵 Случайный трек", callback_data="random")
    builder.button(text="⏭ Пропустить", callback_data="skip")
    builder.button(text="🎲 Случайный факт", callback_data="fact")
    builder.button(text="🎛 Случайный продюсер", callback_data="producer")
    builder.button(text="📊 Мои оценки", callback_data="history")
    builder.adjust(2, 1, 2)
    return builder.as_markup()