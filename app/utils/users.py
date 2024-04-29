import hashlib
import random
import string
from datetime import datetime, timedelta
from sqlalchemy import select

from db.models.base import async_session
from db.models.users import Tokens, Users
from app.schemas import users as user_schema


def get_random_string(length=12):
    """ Генерирует случайную строку, использующуюся как соль """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """ Хеширует пароль с солью """
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


async def get_user_by_email(email: str):
    """ Возвращает информацию о пользователе """
    async with async_session() as session:
        query = await session.execute(select(Users).where(Users.email == email))
        return query.scalars().first()


async def get_user_by_token(token: str):
    """ Возвращает информацию о владельце указанного токена """
    async with async_session() as session:
        try:
            query = await session.execute(
                select(Users).
                join(Tokens).
                where(Tokens.expires > datetime.now(),
                      Tokens.token == token))
            return query.scalars().first()
        except Exception as e:
            print(e)


async def create_user_token(user_id: int) -> Tokens:
    """ Создает токен для пользователя с указанным user_id """
    async with async_session() as session:
        try:
            new_user_token = Tokens(
                expires=datetime.now() + timedelta(weeks=2),
                user_id=user_id,
            )
            session.add(new_user_token)
            await session.commit()
            return new_user_token

        except Exception as e:
            print(e)


async def create_user(user: user_schema.UserCreate):
    """ Создает нового пользователя в БД """
    async with async_session() as session:
        try:
            salt = get_random_string()
            hashed_password = hash_password(user.password, salt)
            user_id = Users(
                email=user.email,
                name=user.name,
                hashed_password=f"{salt}${hashed_password}"
            )
            session.add(user_id)
            await session.commit()
            token = await create_user_token(user_id.id)
            print(token.token)
            token_dict = {"access_token": f"{token.token}",
                          "expires": f"{token.expires}"}  # Fix here: Use "access_token" instead of "token"
        except Exception as e:
            print(e)
    return {**user.dict(), "id": user_id.id, "is_active": True,
            "token": token_dict}  # Fix here: Use user_id.id instead of user_id
