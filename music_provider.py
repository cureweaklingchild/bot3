import random

from db import Session
from models import Track, Genre, Producer, MusicFact


class MusicProvider:
    @staticmethod
    def get_genres_with_tracks():
        session = Session()
        # Получаем все жанры, у которых есть хотя бы один трек
        genres = session.query(Genre).join(Track).distinct().all()
        # Для каждого жанра проверим количество треков
        result = []
        for g in genres:
            count = session.query(Track).filter(Track.genre_id == g.id).count()
            if count > 0:
                result.append(g)
            else:
                print(f"[DEBUG] Genre {g.id} {g.name} has no tracks, removing from list")
        session.close()
        print(f"[DEBUG] get_genres_with_tracks returning {len(result)} genres: {[g.id for g in result]}")
        return result

    @staticmethod
    def get_track_by_genre(genre_id):
        session = Session()
        tracks = session.query(Track).filter(Track.genre_id == genre_id).all()
        print(f"[DEBUG] get_track_by_genre: genre_id={genre_id}, tracks_found={len(tracks)}")
        session.close()
        if not tracks:
            return None
        return random.choice(tracks)

    @staticmethod
    def get_random_producer():
        session = Session()
        producers = session.query(Producer).all()
        if not producers:
            session.close()
            return None
        producer = random.choice(producers)
        session.close()
        return producer

    @staticmethod
    def get_random_fact():
        session = Session()
        facts = session.query(MusicFact).all()
        if not facts:
            session.close()
            return None
        fact = random.choice(facts)
        session.close()
        return fact
