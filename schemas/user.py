def single_serializer_movie(movie) -> dict:
    return {
        'movie': movie['movie_name'],
        'director': movie['director'],
        'genre': movie['genres'],
        'rating': movie['average_rating']
    }


def serialize_movie(items) -> list:
    return [single_serializer_movie(item) for item in items]


def single_serializer_user(item) -> dict:
    return {
        'name': item['name'],
        'age': item['age']
    }


def serialize_user(items):
    return [single_serializer_user(item) for item in items]


######################################################################
# ALTERNATE WAY
def single_serializer_movie_short(movie) -> dict:
    return {**{i: str(movie[i]) for i in movie if i == '_id'}, **{i: movie[i] for i in movie if i != '_id'}}
#
#
# def serialize_movie(items) -> list:
#     return [single_serializer_movie_short(item) for item in items]

#######################################################################
