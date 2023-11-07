from pymongo import MongoClient

connection = MongoClient()

db = connection.movie_app
movie_list = db.movies
users = db.users
