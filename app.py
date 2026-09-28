"""CineMatch: catálogo IMDb e avaliações criadas dentro da aplicação."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import csv
import json
import math
import sqlite3

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / 'data' / 'ml-100k' / 'world_imdb_movies_top_movies_per_year.csv'
DB = ROOT / 'feedback.sqlite3'


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def load_catalog():
    if not CATALOG.exists():
        raise FileNotFoundError(f'Dataset não encontrado: {CATALOG}')
    catalog = {}
    with CATALOG.open(encoding='utf-8', newline='') as file:
        for row in csv.DictReader(file):
            movie_id, title = row['id'].strip(), row['title'].strip()
            if movie_id and title:
                catalog[movie_id] = {'id': movie_id, 'title': title, 'year': row['year'].strip(),
                                     'genres': [genre.strip() for genre in row['genre'].split(',') if genre.strip()],
                                     'imdb_rating': number(row['rating_imdb']), 'votes': int(number(row['vote']))}
    return catalog


movies = load_catalog()
GENRES = sorted({genre for movie in movies.values() for genre in movie['genres']})


def database():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute('CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, genres TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
    con.execute('CREATE TABLE IF NOT EXISTS user_ratings (profile_id INTEGER NOT NULL, movie_id TEXT NOT NULL, rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5), created_at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(profile_id, movie_id), FOREIGN KEY(profile_id) REFERENCES profiles(id))')
    con.execute('CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, user_id INTEGER, usefulness INTEGER CHECK(usefulness BETWEEN 1 AND 5), comment TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
    return con


def get_profile(profile_id):
    with database() as con:
        row = con.execute('SELECT id, name, genres FROM profiles WHERE id = ?', (profile_id,)).fetchone()
    if not row:
        raise ValueError('Perfil não encontrado.')
    return {'id': row['id'], 'name': row['name'], 'genres': json.loads(row['genres'])}


def profile_ratings(profile_id):
    with database() as con:
        rows = con.execute('SELECT movie_id, rating FROM user_ratings WHERE profile_id = ?', (profile_id,)).fetchall()
    return {row['movie_id']: row['rating'] for row in rows if row['movie_id'] in movies}


def profile_history(profile_id):
    values = profile_ratings(profile_id)
    return sorted([{**movies[movie_id], 'rating': rating} for movie_id, rating in values.items()], key=lambda movie: (-movie['rating'], movie['title']))


def all_profiles_ratings(except_profile):
    grouped = {}
    with database() as con:
        rows = con.execute('SELECT profile_id, movie_id, rating FROM user_ratings WHERE profile_id != ?', (except_profile,)).fetchall()
    for row in rows:
        if row['movie_id'] in movies:
            grouped.setdefault(row['profile_id'], {})[row['movie_id']] = row['rating']
    return grouped


def preference_weight(rating):
    """Dá mais influência a avaliações altas: 3★=0,33; 4★=0,67; 5★=1."""
    return max(rating - 2, 0) / 3


def weighted_mean(ratings):
    total_weight = sum(preference_weight(rating) for rating in ratings.values())
    if not total_weight:
        return 3.0
    return sum(rating * preference_weight(rating) for rating in ratings.values()) / total_weight


def neighbor_similarity(target, other):
    common = {movie for movie in set(target).intersection(other) if preference_weight(target[movie]) and preference_weight(other[movie])}
    if len(common) < 2:
        return 0.0, common
    target_mean, other_mean = weighted_mean(target), weighted_mean(other)
    numerator = sum(preference_weight(target[movie]) * preference_weight(other[movie]) * (target[movie] - target_mean) * (other[movie] - other_mean) for movie in common)
    left = math.sqrt(sum(preference_weight(target[movie]) * (target[movie] - target_mean) ** 2 for movie in common))
    right = math.sqrt(sum(preference_weight(other[movie]) * (other[movie] - other_mean) ** 2 for movie in common))
    if not left or not right:
        return 0.0, common
    # Reduz confiança quando o par compartilha poucos filmes.
    return (numerator / (left * right)) * (len(common) / (len(common) + 5)), common


def recommendations(profile_id, n=24):
    profile, target = get_profile(profile_id), profile_ratings(profile_id)
    favorites = set(profile['genres'])
    neighbors = []
    for ratings in all_profiles_ratings(profile_id).values():
        similarity, _ = neighbor_similarity(target, ratings)
        if similarity > 0:
            neighbors.append((similarity, ratings, weighted_mean(ratings)))
    neighbors.sort(key=lambda item: item[0], reverse=True)
    neighbors = neighbors[:40]
    target_mean = weighted_mean(target)
    liked_genres = {}
    for movie_id, rating in target.items():
        if rating >= 4:
            for genre in movies[movie_id]['genres']:
                liked_genres[genre] = liked_genres.get(genre, 0) + (rating - 3)
    liked_total = sum(liked_genres.values()) or 1
    scored = []
    for movie_id, movie in movies.items():
        if movie_id in target:
            continue
        declared_genres = len(favorites.intersection(movie['genres'])) / max(len(favorites), 1)
        learned_genres = sum(liked_genres.get(genre, 0) for genre in movie['genres']) / liked_total
        genre_score = .55 * declared_genres + .45 * min(learned_genres, 1)
        base = movie['imdb_rating'] / 2 if movie['imdb_rating'] else 2.5
        weighted, total, support = 0.0, 0.0, 0
        for similarity, ratings, mean in neighbors:
            if movie_id in ratings:
                weighted += similarity * preference_weight(ratings[movie_id]) * (ratings[movie_id] - mean)
                total += similarity
                support += 1
        collaborative = target_mean + weighted / total if total else base
        # Gêneros e nota de catálogo resolvem início frio; avaliações de usuários entram pelo score colaborativo.
        score = .55 * collaborative + .30 * base + .65 * genre_score
        scored.append((score, movie['votes'], movie_id, support))
    scored.sort(reverse=True)
    method = 'filtragem colaborativa entre perfis criados e preferências de gênero' if neighbors else 'gêneros favoritos e dados do catálogo IMDb (início frio)'
    return [{**movies[movie_id], 'score': round(score, 2), 'support': support,
             'method': 'collaborative' if support else 'catalog',
             'genre_match': bool(favorites.intersection(movies[movie_id]['genres']))} for score, _, movie_id, support in scored[:n]], method


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'web'), **kwargs)

    def json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status); self.send_header('Content-Type', 'application/json; charset=utf-8'); self.send_header('Content-Length', len(body)); self.end_headers(); self.wfile.write(body)

    def read_body(self):
        return json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')

    def do_GET(self):
        url, query = urlparse(self.path), parse_qs(urlparse(self.path).query)
        try:
            if url.path == '/api/summary':
                with database() as con: rating_count = con.execute('SELECT COUNT(*) FROM user_ratings').fetchone()[0]
                return self.json({'movies': len(movies), 'ratings': rating_count, 'users': len(profiles())})
            if url.path == '/api/genres': return self.json(GENRES)
            if url.path == '/api/profiles': return self.json(profiles())
            if url.path == '/api/movies':
                term = query.get('q', [''])[0].casefold()
                found = [movie for movie in movies.values() if term in movie['title'].casefold()]
                return self.json(sorted(found, key=lambda movie: (-movie['votes'], movie['title']))[:12])
            if url.path == '/api/profile':
                profile_id = int(query['id'][0]); return self.json({**get_profile(profile_id), 'history': profile_history(profile_id)})
            if url.path == '/api/recommendations':
                recs, method = recommendations(int(query['profile'][0])); return self.json({'recommendations': recs, 'method': method})
        except (ValueError, KeyError, IndexError) as error:
            return self.json({'error': str(error)}, 400)
        return super().do_GET()

    def do_POST(self):
        try:
            body = self.read_body()
            if self.path == '/api/profiles':
                name, genres, initial = str(body.get('name', '')).strip()[:60], sorted(set(body.get('genres', []))), body.get('ratings', [])
                if not name: raise ValueError('Informe seu nome.')
                if not genres or not set(genres).issubset(GENRES): raise ValueError('Selecione pelo menos um gênero válido.')
                values = {str(row['movie']): int(row['rating']) for row in initial}
                if any(movie not in movies or rating not in range(1, 6) for movie, rating in values.items()): raise ValueError('Filme ou nota inválida.')
                with database() as con:
                    profile_id = con.execute('INSERT INTO profiles(name, genres) VALUES (?, ?)', (name, json.dumps(genres))).lastrowid
                    con.executemany('INSERT INTO user_ratings(profile_id, movie_id, rating) VALUES (?, ?, ?)', [(profile_id, movie, rating) for movie, rating in values.items()])
                return self.json({'id': profile_id}, 201)
            if self.path == '/api/rating':
                profile_id, movie, rating = int(body['profile']), str(body['movie']), int(body['rating']); get_profile(profile_id)
                if movie not in movies or rating not in range(1, 6): raise ValueError('Dados de avaliação inválidos.')
                with database() as con: con.execute('INSERT OR REPLACE INTO user_ratings(profile_id, movie_id, rating) VALUES (?, ?, ?)', (profile_id, movie, rating))
                return self.json({'ok': True})
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            return self.json({'error': str(error)}, 400)
        self.json({'error': 'Rota inexistente'}, 404)


def profiles():
    with database() as con:
        rows = con.execute('SELECT p.id, p.name, p.genres FROM profiles p WHERE EXISTS (SELECT 1 FROM user_ratings r WHERE r.profile_id = p.id) ORDER BY p.id DESC').fetchall()
    return [{'id': row['id'], 'name': row['name'], 'genres': json.loads(row['genres'])} for row in rows]


if __name__ == '__main__':
    database().close(); print('CineMatch em http://localhost:8000')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
