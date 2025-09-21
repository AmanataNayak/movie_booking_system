from fastapi import FastAPI
from routes.movie import router as movie_router
from routes.genre import router as genre_router
from routes.showtime import router as showtime_router

app = FastAPI()

app.include_router(movie_router)
app.include_router(genre_router)
app.include_router(showtime_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
