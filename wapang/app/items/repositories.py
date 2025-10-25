from typing import Annotated, Sequence
import uuid

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from wapang.app.items.models import Item
from wapang.database.connection import get_db_session

class ItemRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def create_item(self, item: Item) -> None:
        self.session.add(item)
        self.session.flush()

    def update_item(self, item: Item) -> None:
        self.session.merge(item)
        self.session.flush()

    def delete_item(self, item: Item) -> None:
        self.session.delete(item)

    def get_item_by_id(self, item_id: str) -> Item | None:
        return self.session.scalar(select(Item).where(Item.id == item_id))
    
    def get_items(
            self, 
            store_id: str | None = None, 
            min_price: int | None = None, 
            max_price: int | None = None, 
            in_stock: bool = False
        ) -> Sequence[Item]:
        query = select(Item)
        if store_id:
            query = query.where(Item.store_id == store_id)
        if min_price is not None:
            query = query.where(Item.price >= min_price)
        if max_price is not None:
            query = query.where(Item.price <= max_price)
        if in_stock:
            query = query.where(Item.stock > 0)
        
        return self.session.scalars(query).all()