import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wapang.database.common import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str | None] = mapped_column(String(150))
    phone_number: Mapped[str | None] = mapped_column(String(20))

    stores = relationship("Store", back_populates="owner")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")