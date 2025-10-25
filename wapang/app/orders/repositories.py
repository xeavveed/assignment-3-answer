from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from wapang.app.orders.models import Order, OrderItem
from wapang.database.connection import get_db_session

class OrderRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def create_order(self, order: Order) -> None:
        self.session.add(order)
        self.session.flush()

    def create_order_items(self, order_items: list[OrderItem]) -> None:
        self.session.add_all(order_items)
        self.session.flush()

    def get_order_by_id(self, order_id: str) -> Order | None:
        return self.session.scalar(select(Order).where(Order.id == order_id))

    def get_orders_by_user_id(self, user_id: str) -> Sequence[Order]:
        query = select(Order).where(Order.user_id == user_id)
        return self.session.scalars(query).all()