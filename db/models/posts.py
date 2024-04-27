from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped

from db.models.base import Base


class Posts(Base):
    __tablename__ = "posts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime]
    title: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
