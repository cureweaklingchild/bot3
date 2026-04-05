import random
from music_provider import MusicProvider

class RecommendationEngine:
    @staticmethod
    def get_random_recommendation():
        genres = MusicProvider.get_genres_with_tracks()
        if not genres:
            print("[DEBUG] No genres with tracks")
            return None, None
        genre = random.choice(genres)
        print(f"[DEBUG] Chosen genre: {genre.id} - {genre.name}")
        track = MusicProvider.get_track_by_genre(genre.id)
        if track:
            print(f"[DEBUG] Found track: {track.title}")
        else:
            print("[DEBUG] No track found for genre")
        return genre, track