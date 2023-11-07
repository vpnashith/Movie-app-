import pymongo
from fastapi import APIRouter, HTTPException, status, Depends
from config.database import movie_list, users
from models.user import Movie, User, Rating, Filter, UserInDB, MovieUpdate, UserUpdate, Tags
from schemas.user import serialize_movie, serialize_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Literal

router = APIRouter()

# AUTHORIZATION

oauth2schema = OAuth2PasswordBearer(tokenUrl='token')


def password_encode(password):
    return '<' + password + '>'


@router.post('/token', tags=['Authorize'])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not users.find_one({'name': form_data.username}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user exists')
    if not users.find_one({'password': password_encode(form_data.password)}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Password')
    return {'access_token': form_data.username, 'token_type': 'bearer'}


# MOVIE DETAILS

@router.get('/', tags=[Tags.movie], description='Display all the movies information')
async def display_movies():
    return serialize_movie(movie_list.find())


@router.post('/movies/', tags=[Tags.movie], description='Add a new movie info')
async def create_movie_info(movie: Movie):
    movie_list.insert_one(dict(movie))
    return serialize_movie(movie_list.find())


@router.put('/movies/{movie_name}', tags=[Tags.movie],
            description='Edit the movie info, we have to give the name of the movie',
            dependencies=[Depends(oauth2schema)])
async def edit_the_movie_info(movie_name_to_update: str, updated_info: MovieUpdate):
    d = dict()
    if updated_info.movie_name:
        d['movie_name'] = updated_info.movie_name
    if updated_info.director:
        d['director'] = updated_info.director
    if updated_info.producer:
        d['producer'] = updated_info.producer
    if updated_info.cast:
        d['cast'] = updated_info.cast
    if updated_info.subtitles:
        d['subtitle'] = updated_info.director
    if updated_info.languages:
        d['languages'] = updated_info.languages
    if updated_info.genres:
        d['genres'] = updated_info.genres
    if updated_info.rating:
        d['rating'] = updated_info.rating
        d['overall_status'] = 'HIT' if sum(updated_info.rating) / (len(updated_info.rating) * 10) > 0.6 else 'FLOP'
        d['average_rating'] = sum(updated_info.rating) / len(updated_info.rating)
    if updated_info.resolution:
        d['resolution'] = updated_info.resolution
    if updated_info.release_date:
        d['release_date'] = updated_info.release_date
    if updated_info.revenue_collection:
        d['revenue_collection'] = updated_info.revenue_collection

    movie_list.find_one_and_update({'movie_name': movie_name_to_update}, {'$set': d})

    return serialize_movie(movie_list.find())


@router.delete('/movies/{movie_name}', tags=[Tags.movie],
               description='delete the movie info, we have to give the name of the movie',
               dependencies=[Depends(oauth2schema)])
async def delete_the_movie_info(movie_name: str):
    return movie_list.find_one_and_delete({'movie_name': movie_name})


# USER


@router.post('/user/', tags=[Tags.user], description='Add a new user / Register a new user')
async def create_user(user: UserInDB):
    user.password = password_encode(user.password)
    users.insert_one(dict(user))
    return serialize_user(users.find())


@router.put('/user/watch/', tags=[Tags.user], description='Watch movie')
async def watch_movie(name_of_user: Annotated[str, Depends(oauth2schema)], movie_watching: str):
    if not movie_list.find_one({'movie_name': movie_watching}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Not present such a movie. Please check the name')
    # Now we are adding a field movie_watched by the user into Users database
    if users.find_one({'name': name_of_user, 'movie_watched': {'$exists': False}}):
        users.find_one_and_update({'name': name_of_user}, {'$set': {'movie_watched': [movie_watching]}})
    elif users.find_one({'name': name_of_user, 'movie_watched': {'$elemMatch': {'$eq': movie_watching}}}):
        return {'status': f'user {name_of_user} is {movie_watching} is already watched'}
    else:
        users.find_one_and_update({'name': name_of_user}, {'$push': {'movie_watched': movie_watching}})

    return {'status': f'user {name_of_user} is finished watching movie {movie_watching} , Updated the DB'}


#
# @router.post('/user/rating/', tags=['users'], description='Add a rating')#, dependencies=[Depends(oauth2schema)])
# async def post_rating(user_rating: Rating):
#     if user_rating.rating:
#         rating = movie_list.find_one({'movie_name': user_rating.movie_name}, {'rating': True, '_id': False})['rating']
#         updated_rating = rating + user_rating.rating
#         movie_list.find_one_and_update({'movie_name': user_rating.movie_name}, {'$set': {'rating': updated_rating}})
#         print(rating)


@router.post('/user/rating/', tags=[Tags.user],
             description='Add a rating. You can add rating if you are watched the movie.Otherwise you cannot')
async def post_rating(user_rating: Rating, user_name: Annotated[str, Depends(oauth2schema)]):
    if not users.find_one(
            {'name': user_name, 'movie_watched': {'$elemMatch': {'$eq': user_rating.movie_name}}}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User {user_name} does not watched this movie {user_rating.movie_name}, Please '
                                   f'watch and then only you can rate the movie')
    if user_rating.rating:
        rating = movie_list.find_one({'movie_name': user_rating.movie_name}, {'rating': True, '_id': False}).get(
            'rating')
        rating.append(user_rating.rating)
        average = sum(rating) / len(rating)
        movie_list.find_one_and_update({'movie_name': user_rating.movie_name},
                                       {'$set': {'rating': rating, 'average_rating': average}})

        if sum(rating) / ((len(rating)) * 10) > 0.6:
            movie_list.find_one_and_update({'movie_name': user_rating.movie_name}, {'$set': {'overall_status': 'HIT'}})
        else:
            movie_list.find_one_and_update({'movie_name': user_rating.movie_name}, {'$set': {'overall_status': 'FLOP'}})

    return {'Message': f'Rating Added Successfully for the movie {user_rating.movie_name}'}


@router.get('/user/{name}/', tags=[Tags.user], description='Search for a particular user by name')
async def find_user(name: str):
    return serialize_user(users.find({'name': name}))


@router.put('/user/{name}/', tags=[Tags.user], description='update the user info, we have to give the name of the user')
async def update_user(name: Annotated[str, Depends(oauth2schema)], user: UserUpdate):
    d = dict()
    if user.name:
        d['name'] = user.name
    if user.age:
        d['age']: user.age
    if user.password:
        d['password'] = password_encode(user.password)

    users.update_one({'name': name}, {'$set': d})

    return serialize_user(users.find({'name': user.name}))


@router.delete('/user/{name}/', tags=[Tags.user], description='delete the user info, we have to give the name of the '
                                                              'user, We are only deleting one user-movie compo at a time'
                                                              'input hte movie name that you watched')
async def delete_user(name: Annotated[str, Depends(oauth2schema)], movie_name: str):
    return users.find_one_and_delete({'name': name, 'movie_name': movie_name})


# FILTERS

# @router.get('/movie/filter/{genre_search}', tags=['filters'])
# async def filter_movies(genre_search: str):
#     # movie_list.find({'genres': {'$elemMatch': {'$eq': genre_search}}})
#     print(serialize_movie((movie_list.find({'genres': {'$elemMatch': {'$eq': genre_search}}}))))


@router.post('/movie/filter/', tags=[Tags.filters])
async def filter_the_movies(item: Filter):
    d = dict()
    if item.genre:  # OK
        d['genres'] = {'$elemMatch': {'$eq': item.genre}}
    if item.cast:  # OK
        d['cast'] = {'$all': item.cast}
    if item.minimum_rating:  # OK
        d['average_rating'] = {'$gt': item.minimum_rating}  # Added a new field in the DB (average_rating)
    if item.languages_or_subtitle:  # OK
        d['$or'] = [{'subtitles': {'$elemMatch': {'$eq': item.languages_or_subtitle}}},
                    {'languages': {'$elemMatch': {'$eq': item.languages_or_subtitle}}}]
    if item.director_and_producer:  # OK
        d['$and'] = [{'director': item.director_and_producer.director},
                     {'producer': item.director_and_producer.producer}]
    if item.release_date:  # OK
        d['release_date'] = item.release_date

    # print("d is : ", d)

    return serialize_movie(movie_list.find(d))


# SORT

@router.post('/movie/sort/', tags=[Tags.sort])
async def order(asc_or_desc: Literal['Ascending', 'Descending']):
    if asc_or_desc == 'Ascending':
        return serialize_movie(
            movie_list.find().sort('average_rating', pymongo.ASCENDING))  # We can do 1 instead of pymongo.ASCENDING
    else:
        return serialize_movie(
            movie_list.find().sort('average_rating', pymongo.DESCENDING))  # We can do -1 instead of pymongo.DESCENDING
