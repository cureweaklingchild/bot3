import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Genre, Track, Rating, Producer, MusicFact

engine = create_engine('sqlite:///music_bot.db')
Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
    session = Session()
    if session.query(Genre).count() == 0:
        with open('data/genres.json', 'r', encoding='utf-8') as f:
            genres = json.load(f)
        for g in genres:
            genre = Genre(id=g['id'], name=g['name'], description=g['description'])
            session.add(genre)
        session.commit()
    if session.query(Track).count() == 0:
        with open('data/tracks.json', 'r', encoding='utf-8') as f:
            tracks = json.load(f)
        for t in tracks:
            track = Track(
                title=t['title'],
                artist=t['artist'],
                genre_id=t['genre_id'],
                url=t.get('url'),
                source=t.get('source')
            )
            session.add(track)
        session.commit()
    session.close()

def init_db():
    Base.metadata.create_all(engine)
    session = Session()
    if session.query(Genre).count() == 0:
        print("Loading genres from data/genres.json")
        with open('data/genres.json', 'r', encoding='utf-8') as f:
            genres = json.load(f)
        for g in genres:
            genre = Genre(id=g['id'], name=g['name'], description=g['description'])
            session.add(genre)
        session.commit()
        print(f"Loaded {len(genres)} genres")
    else:
        print("Genres already exist in DB")
    if session.query(Track).count() == 0:
        print("Loading tracks from data/tracks.json")
        try:
            with open('data/tracks.json', 'r', encoding='utf-8') as f:
                tracks = json.load(f)
            for t in tracks:
                track = Track(
                    title=t['title'],
                    artist=t['artist'],
                    genre_id=t['genre_id'],
                    url=t.get('url'),
                    source=t.get('source')
                )
                session.add(track)
            session.commit()
            print(f"Loaded {len(tracks)} tracks")
        except Exception as e:
            print(f"Error loading tracks: {e}")
    else:
        print("Tracks already exist in DB")
    tracks_count = session.query(Track).count()
    print(f"Total tracks in DB: {tracks_count}")

    if session.query(Producer).count() == 0:
        print("Loading producers from data/producers.json")
        try:
            with open('data/producers.json', 'r', encoding='utf-8') as f:
                producers = json.load(f)
            for p in producers:
                producer = Producer(
                    name=p['name'],
                    bio=p.get('bio'),
                    wiki_url=p.get('wiki_url'),
                    image_url=p.get('image_url'),
                    source=p.get('source')
                )
                session.add(producer)
            session.commit()
            print(f"Loaded {len(producers)} producers")
        except Exception as e:
            print(f"Error loading producers: {e}")

    if session.query(MusicFact).count() == 0:
        print("Loading music facts from data/facts.json")
        try:
            with open('data/facts.json', 'r', encoding='utf-8') as f:
                facts = json.load(f)
            for fact_data in facts:
                fact = MusicFact(text=fact_data['text'], source=fact_data.get('source'))
                session.add(fact)
            session.commit()
            print(f"Loaded {len(facts)} music facts")
        except Exception as e:
            print(f"Error loading music facts: {e}")

    session.close()
