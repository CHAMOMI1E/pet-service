from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import DB_TOKEN
from app.routers import users
import databases

# создаем объект database, который будет использоваться для выполнения запросов
database = databases.Database(DB_TOKEN)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(users.router)


@app.get("/start")
async def start():
    return {"hello": "world"}


# @app.on_event("startup")
# async def startup():
#     # когда приложение запускается устанавливаем соединение с БД
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     # когда приложение останавливается разрываем соединение с БД
#     await database.disconnect()
