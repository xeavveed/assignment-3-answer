import uuid
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wapang.database.common import Base

from wapang.app.users.models import User


class Store(Base):
    __tablename__ = "store"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True)
    address: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone_number: Mapped[str] = mapped_column(String(20))
    delivery_fee: Mapped[int] = mapped_column(Integer)

    owner_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    owner: Mapped[User] = relationship("User", back_populates="stores")
    
    items = relationship("Item", back_populates="store", cascade="all, delete-orphan")