from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    last_track_id = Column(Integer, ForeignKey('tracks.id'), nullable=True)  # добавлено

    ratings = relationship('Rating', back_populates='user')
    # связь с последним треком (не обязательна)
    last_track = relationship('Track', foreign_keys=[last_track_id])
    is_subscribed = Column(Integer, default=0)


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    tracks = relationship('Track', back_populates='genre')
    ratings = relationship('Rating', back_populates='genre')


class Track(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    url = Column(String, nullable=True)
    source = Column(String, nullable=True)

    genre = relationship('Genre', back_populates='tracks')
    ratings = relationship('Rating', back_populates='track')


class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    track_id = Column(Integer, ForeignKey('tracks.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    rating = Column(Integer, nullable=False)  # 1-5
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='ratings')
    track = relationship('Track', back_populates='ratings')
    genre = relationship('Genre', back_populates='ratings')


class Producer(Base):
    __tablename__ = 'producers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=True)  # краткая биография
    wiki_url = Column(String, nullable=True)  # ссылка на Википедию или другую статью
    image_url = Column(String, nullable=True)  # опционально фото
    source = Column(String, nullable=True)  # источник (например, "wikipedia")


class MusicFact(Base):
    __tablename__ = 'music_facts'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    source = Column(String, nullable=True)  # опционально: откуда факт

