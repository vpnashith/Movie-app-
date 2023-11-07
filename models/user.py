from pydantic import BaseModel, Field
from typing import Annotated


class Movie_Base(BaseModel):
    cast: list | None = None
    subtitles: list | None = None
    languages: list | None = None
    genres: list | None = None
    rating: list[int] | None = []
    resolution: list | None = None
    release_date: str | None = None
    revenue_collection: int | None = None
    overall_status: str | None = None
    average_rating: float | None = 0


class Movie(Movie_Base):
    movie_name: str
    director: str
    producer: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'movie_name': 'Leo',
                    'director': 'Lokesh',
                    'producer': '7 screen',
                    'cast': ["vijay", "Thrisha", "etc.."],
                    'subtitles': ['English', "Malayalam", "etc.."],
                    'languages': ['English', "Malayalam", "etc.."],
                    'genres': ["Action", "comedy", "etc.."],
                    'resolution': ["144p", "240p", "etc"],
                    'release_date': '10-10-2023',
                    'revenue_collection': 55.0

                }
            ]
        }
    }


class MovieUpdate(Movie_Base):
    movie_name: str | None = None
    director: str | None = None
    producer: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'movie_name': 'Leo',
                    'director': 'Lokesh',
                    'producer': '7 screen',
                    'cast': ["vijay", "Thrisha", "etc.."],
                    'subtitles': ['English', "Malayalam", "etc.."],
                    'languages': ['English', "Malayalam", "etc.."],
                    'genres': ["Action", "comedy", "etc.."],
                    'resolution': ["144p", "240p", "etc"],
                    'release_date': '10-10-2023',
                    'revenue_collection': 55.0

                }
            ]
        }
    }


class User(BaseModel):  # to create user
    name: str
    age: Annotated[int, Field(ge=18)]


class UserInDB(User):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    age: Annotated[int | None, Field(ge=18)] = None
    password: str | None = None


class Rating(BaseModel):  # to give the rating
    movie_name: str
    rating: Annotated[int | None, Field(ge=0, le=10)] = None


class dir_prod(BaseModel):
    director: str | None = None
    producer: str | None = None


class Filter(BaseModel):
    genre: str | None = None
    minimum_rating: float | None = None
    languages_or_subtitle: str | None = None
    director_and_producer: dir_prod | None = None
    release_date: str | None = None
    cast: list | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "genre": "Action",
                    "minimum_rating": 5.0,
                    "languages_or_subtitle": 'English',
                    "director_and_producer": {'director': 'director_name', 'producer': 'producer_name'},
                    "release_date": '10-10-23',
                    "cast": ['actor1', 'actor2', 'etc...']
                }
            ]
        }
     }


class Tags:
    movie = 'Movie info'
    user = 'Users'
    filters = 'Filters'
    sort = 'Sort by rating'

