from typing import Annotated, Sequence
import uuid

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from wapang.app.carts.models import CartItem
from wapang.database.connection import get_db_session

class CartRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def add_cart_item(self, cart_item: CartItem) -> None:
        self.session.add(cart_item)
        self.session.flush()

    def update_cart_item(self, cart_item: CartItem) -> None:
        self.session.merge(cart_item)
        self.session.flush()

    def get_cart_item_by_user_and_item(self, user_id: str, item_id: str) -> CartItem | None:
        return self.session.scalar(
            select(CartItem).where(CartItem.user_id == user_id, CartItem.item_id == item_id)
        )

    def delete_cart_item(self, cart_item: CartItem) -> None:
        self.session.delete(cart_item)
        self.session.flush()

    def get_cart_items_by_user_id(self, user_id: str) -> Sequence[CartItem]:
        return self.session.scalars(
            select(CartItem).where(CartItem.user_id == user_id)
        ).all()