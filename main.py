import uvicorn
from fastapi import FastAPI
from routes.user import router
from fastapi.middleware.cors import CORSMiddleware

description = ''' **Here you have the movie info and user/panel info. With respect to the ratings , 
it will automatically changes the movie status.You can also filter and sort the movies.**'''

tags_metadata = [
    {
        "name": "Authorize",
        "description": "Login Here "
    },
    {
        "name": "Users",
        "description": "Operation done by users are here, Movie watching, give rating etc includes here"
    },
    {
        "name": "Movie info",
        "description": "You can upload or update movie info here"
    },
    {
        "name": "Filters",
        "description": "You can apply more than one filter at a time"
    },
    {
        "name": "Sort by rating",
        "description": " Here it show sort by average rating posted by all the reviewers"
    }
]

app = FastAPI(title='Movie Info App',
              description=description,
              version='0.0.1',
              contact={
                  'name': 'Nashith vp',
                  'email': 'nashith@anorasolutions.com'
              },
              openapi_tags=tags_metadata
              )

#origins = ["http://localhost", "http://localhost:8000", "http://localhost:9000", "64.227.130.120"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


@app.post('/hellow', tags=["Hello World"])
async def hellow():
    return {"msg": "HELLOW WORLD"}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app,
                host="127.0.0.1",
                port=9000,
                reload=False,
                )
