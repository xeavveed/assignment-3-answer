from typing import Annotated, Any

from fastapi import Depends
from wapang.app.items.exceptions import ItemNotFoundError, ItemNotEnoughStockError
from wapang.app.orders.exceptions import EmptyItemListError, OrderNotOwnedError, OrderNotFoundError, InvalidOrderStatusError
from wapang.app.items.repositories import ItemRepository
from wapang.app.items.models import Item
from wapang.app.users.models import User
from wapang.app.orders.models import Order, OrderItem
from wapang.app.orders.schemas import (
    OrderCreateRequest,
    OrderResponse,
    OrderDetailResponse,
    ItemResponse,
    OrderStatusUpdateRequest,
)
from wapang.app.orders.repositories import OrderRepository

class OrderService:
    def __init__(self, 
                 order_repository: Annotated[OrderRepository, Depends()],
                 item_repository: Annotated[ItemRepository, Depends()]
                 ) -> None:
        self.order_repository = order_repository
        self.item_repository = item_repository

    def create_order(self, user: User, request: OrderCreateRequest) -> OrderResponse:
        total_price = 0
        items_by_id: dict[str, Item] = {}
        seen_store_ids: set[str] = set()
        if request.items == []:
            raise EmptyItemListError()
        for req_item in request.items:
            item = self.item_repository.get_item_by_id(req_item.item_id)
            if item is None:
                raise ItemNotFoundError()
            if item.stock < req_item.quantity:
                raise ItemNotEnoughStockError()
            items_by_id[req_item.item_id] = item
            # add item subtotal
            total_price += item.price * req_item.quantity
            # add delivery fee once per store
            store_id = item.store.id
            if store_id not in seen_store_ids:
                seen_store_ids.add(store_id)
                total_price += item.store.delivery_fee
            

        order = Order(user_id=user.id, total_price=total_price)
        self.order_repository.create_order(order)

        new_order_items: list[OrderItem] = []
        for req_item in request.items:
            item = items_by_id[req_item.item_id]
            item.stock -= req_item.quantity
            new_order_items.append(
                OrderItem(
                    order_id=order.id,
                    item_id=req_item.item_id,
                    quantity=req_item.quantity,
                )
            )
        self.order_repository.create_order_items(new_order_items)

        return self._build_order_response(order)
    
    def get_order(self, user: User, order_id: str) -> OrderResponse:
        order = self.order_repository.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        if order.user_id != user.id:
            raise OrderNotOwnedError()

        return self._build_order_response(order)

    def update_order_status(self, user: User, order_id: str, request: OrderStatusUpdateRequest) -> str:
        order = self.order_repository.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()
        if order.user_id != user.id:
            raise OrderNotOwnedError()
        if order.status == request.status:
            raise InvalidOrderStatusError()
        
        order.status = request.status

        return order.status
    
    def get_orders_by_user(self, user_id: str) -> list[Order]:
        return self.order_repository.get_orders_by_user_id(user_id)
    
    def _build_order_response(self, order: Order) -> OrderResponse:
        lines: list[tuple[Item, int]] = [(oi.item, oi.quantity) for oi in order.order_items]
        details, total_price = self._compose_details_and_total(lines)
        return OrderResponse(
            order_id=order.id,
            details=details,
            total_price=total_price,
            status=order.status,
        )

    def _compose_details_and_total(self, lines: list[tuple[Item, int]]) -> tuple[list[OrderDetailResponse], int]:
            store_groups: dict[str, dict] = {}
            for item, qty in lines:
                store = item.store
                sid = store.id
                if sid not in store_groups:
                    store_groups[sid] = {
                        "store_id": sid,
                        "store_name": store.name,
                        "delivery_fee": store.delivery_fee,
                        "items": [],
                        "items_subtotal": 0,
                    }
                subtotal = item.price * qty
                store_groups[sid]["items"].append(
                    ItemResponse(
                        item_id=item.id,
                        item_name=item.name,
                        price=item.price,
                        quantity=qty,
                        subtotal=subtotal,
                    )
                )
                store_groups[sid]["items_subtotal"] += subtotal

            details: list[OrderDetailResponse] = []
            total_price = 0
            for g in store_groups.values():
                store_total_price = g["items_subtotal"] + g["delivery_fee"]
                total_price += store_total_price
                details.append(
                    OrderDetailResponse(
                        store_id=g["store_id"],
                        store_name=g["store_name"],
                        delivery_fee=g["delivery_fee"],
                        store_total_price=store_total_price,
                        items=g["items"],
                    )
                )

            return details, total_price