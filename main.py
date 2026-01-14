from fastapi import FastAPI
from app.controller.UserController import router as UserRouter
from app.controller.BookController import router as BookRouter
from app.controller.BookingController import router as BookingRouter

app = FastAPI()
app.include_router(UserRouter)
app.include_router(BookRouter)
app.include_router(BookingRouter)


@app.get("/")
def WeGood() -> dict:
    return {"status": "ok"}
