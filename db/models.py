from sqlalchemy import text, ForeignKey, String, Boolean, Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import true

from datetime import datetime

from config import DB_TOKEN

engine = create_async_engine(DB_TOKEN,
                             echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Users(Base,IdMixin):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(server_default=true(), nullable=False)


class Tokens(Base, IdMixin):
    __tablename__ = 'tokens'

    token: Mapped[UUID] = mapped_column(UUID(as_uuid=False),
                                        server_default=text("uuid_generate_v4()"),
                                        unique=True,
                                        nullable=False,
                                        index=True)
    expires: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
