from schemas.movie import MovieCreate, MovieUpdate

movies: dict[int, dict] = {}
next_id = 1


def get_all_movies() -> list[dict]:
    return list(movies.values())


def get_movie(movie_id: int) -> dict:
    movie = movies.get(movie_id)
    if movie is None:
        raise KeyError("Film tidak ditemukan")
    return movie


def create_movie(data: MovieCreate) -> dict:
    global next_id

    movie = data.model_dump()
    movie["id"] = next_id
    movies[next_id] = movie
    next_id += 1

    return movie


def update_movie(movie_id: int, data: MovieUpdate) -> dict:
    if movie_id not in movies:
        raise KeyError("Film tidak ditemukan")

    movie = data.model_dump()
    movie["id"] = movie_id
    movies[movie_id] = movie

    return movie


def delete_movie(movie_id: int) -> None:
    if movie_id not in movies:
        raise KeyError("Film tidak ditemukan")

    del movies[movie_id]
