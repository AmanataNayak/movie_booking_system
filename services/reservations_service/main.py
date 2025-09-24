from fastapi import FastAPI
from router.reservation import router as reservation_router

app = FastAPI(title="Reservation Service")

app.include_router(reservation_router)
