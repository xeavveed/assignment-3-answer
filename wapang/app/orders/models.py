from enum import Enum
import uuid
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wapang.app.items.models import Item
from wapang.database.common import Base

from wapang.app.users.models import User


class StatusEnum(str, Enum):
    ORDERED = "ORDERED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class Order(Base):
    __tablename__ = "order"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    status: Mapped[StatusEnum] = mapped_column(String(10), default=StatusEnum.ORDERED)
    total_price: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User", back_populates="orders")

    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    quantity: Mapped[int] = mapped_column(Integer)
    order_id: Mapped[str] = mapped_column(ForeignKey("order.id"))
    item_id: Mapped[str] = mapped_column(ForeignKey("item.id"))
    order: Mapped[Order] = relationship(Order, back_populates="order_items")
    item: Mapped[Item] = relationship(Item, back_populates="order_items")