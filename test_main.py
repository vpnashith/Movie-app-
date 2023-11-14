from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# To test the get from movies
def test_display_movies():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == [
  {
    "movie": "Lucifer",
    "director": "PrithivRaj",
    "genre": [
      "Action",
      "Drama",
      "Mass"
    ],
    "rating": 7.4
  },
  {
    "movie": "Leo",
    "director": "Lokesh",
    "genre": [
      "Action",
      "Thriller"
    ],
    "rating": 5.666666666666667
  },
  {
    "movie": "Nan pakal",
    "director": "LJP",
    "genre": [
      "Drama"
    ],
    "rating": 6
  },
  {
    "movie": "Leo2",
    "director": "Lokesh",
    "genre": [
      "Action",
      "comedy",
      "etc.."
    ],
    "rating": 6
  },
  {
    "movie": "Leo",
    "director": "Lokesh",
    "genre": [
      "Action",
      "comedy",
      "etc.."
    ],
    "rating": 0
  }
]


# def test_create_movie_info():
#     response = client.post('/movies/', json={
#         "cast": [
#             "vijay",
#             "Thrisha",
#             "etc.."
#         ],
#         "director": "Lokesh",
#         "genres": [
#             "Action",
#             "comedy",
#             "etc.."
#         ],
#         "languages": [
#             "English",
#             "Malayalam",
#             "etc.."
#         ],
#         "movie_name": "Leo",
#         "producer": "7 screen",
#         "release_date": "10-10-2023",
#         "resolution": [
#             "144p",
#             "240p",
#             "etc"
#         ],
#         "revenue_collection": 55,
#         "subtitles": [
#             "English",
#             "Malayalam",
#             "etc.."
#         ]
#     })
#     assert response.status_code == 200
#     assert response.json() == [
#   {
#     "movie": "Lucifer",
#     "director": "PrithivRaj",
#     "genre": [
#       "Action",
#       "Drama",
#       "Mass"
#     ],
#     "rating": 7.4
#   },
#   {
#     "movie": "Leo",
#     "director": "Lokesh",
#     "genre": [
#       "Action",
#       "Thriller"
#     ],
#     "rating": 5.666666666666667
#   },
#   {
#     "movie": "Nan pakal",
#     "director": "LJP",
#     "genre": [
#       "Drama"
#     ],
#     "rating": 6
#   },
#   {
#     "movie": "Leo2",
#     "director": "Lokesh",
#     "genre": [
#       "Action",
#       "comedy",
#       "etc.."
#     ],
#     "rating": 6
#   },
#   {
#     "movie": "Leo",
#     "director": "Lokesh",
#     "genre": [
#       "Action",
#       "comedy",
#       "etc.."
#     ],
#     "rating": 0
#   }
# ]
