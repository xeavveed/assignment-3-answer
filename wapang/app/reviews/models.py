import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wapang.database.common import Base

from wapang.app.users.models import User
from wapang.app.items.models import Item


class Review(Base):
    __tablename__ = "review"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(String(500), nullable=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="reviews")

    item_id: Mapped[str] = mapped_column(ForeignKey("item.id"))
    item: Mapped["Item"] = relationship("Item", back_populates="reviews")