import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wapang.app.stores.models import Store
from wapang.database.common import Base


class Item(Base):
    __tablename__ = "item"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    stock: Mapped[int] = mapped_column(Integer)

    store_id: Mapped[str] = mapped_column(ForeignKey("store.id"))
    store: Mapped[Store] = relationship(back_populates="items")

    order_items = relationship("OrderItem", back_populates="item")
    reviews = relationship("Review", back_populates="item")