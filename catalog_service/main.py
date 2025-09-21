from fastapi import FastAPI
from routers.auditorium import router as auditorium_router
from routers.seat import router as seat_router
from routers.showtime import router as showtime_router

app = FastAPI()

app.include_router(auditorium_router)
app.include_router(seat_router)
app.include_router(showtime_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
