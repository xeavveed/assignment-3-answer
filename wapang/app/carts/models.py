from sqlalchemy import String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from wapang.app.users.models import User
from wapang.database.common import Base

from wapang.app.items.models import Item

class CartItem(Base):
    __tablename__ = "cart_item"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, index=True)
    item_id: Mapped[str] = mapped_column(String(36), ForeignKey("item.id", ondelete="CASCADE"), primary_key=True, index=True)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    user: Mapped[User] = relationship("User")
    item: Mapped[Item] = relationship("Item")