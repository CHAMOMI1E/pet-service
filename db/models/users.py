from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import true

from datetime import datetime

from db.models.base import Base


class Users(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(server_default=true(), nullable=False)


class Tokens(Base):
    __tablename__ = 'tokens'

    token: Mapped[UUID] = mapped_column(UUID(as_uuid=False),
                                        server_default=text("uuid_generate_v4()"),
                                        unique=True,
                                        nullable=False,
                                        index=True)
    expires: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
