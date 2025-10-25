from typing import Annotated

from fastapi import Depends
from wapang.app.users.models import User
from wapang.app.carts.models import CartItem
from wapang.app.carts.schemas import CartItemRequest
from wapang.app.carts.exceptions import EmptyItemListError
from wapang.app.carts.repositories import CartRepository
from wapang.app.items.repositories import ItemRepository
from wapang.app.items.exceptions import ItemNotFoundError
from wapang.app.orders.schemas import OrderCreateRequest, ItemRequest
from wapang.app.orders.services import OrderService

class CartService:
    def __init__(self, 
                 cart_repository: Annotated[CartRepository, Depends()],
                 item_repository: Annotated[ItemRepository, Depends()],
                 ) -> None:
        self.cart_repository = cart_repository
        self.item_repository = item_repository
    
    def add_or_update_cart(
            self,
            user: User, 
            request: CartItemRequest,
            order_service: OrderService
        ) -> tuple[list, int]:
        item = self.item_repository.get_item_by_id(request.item_id)
        if not item:
            raise ItemNotFoundError()
        cartitem = self.cart_repository.get_cart_item_by_user_and_item(user.id, request.item_id)
        if request.quantity == 0 and cartitem:
            self.cart_repository.delete_cart_item(cartitem)
        elif cartitem:
            cartitem.quantity = request.quantity
            self.cart_repository.update_cart_item(cartitem)
        else:
            cartitem = CartItem(user_id=user.id, item_id=request.item_id, quantity=request.quantity)
            self.cart_repository.add_cart_item(cartitem)

        all_cart_items = self.cart_repository.get_cart_items_by_user_id(user.id)

        return order_service._compose_details_and_total([(ci.item, ci.quantity) for ci in all_cart_items])

    def get_cart_items(self, user: User, order_service: OrderService) -> tuple[list, int]:
        all_cart_items = self.cart_repository.get_cart_items_by_user_id(user.id)
        return order_service._compose_details_and_total([(ci.item, ci.quantity) for ci in all_cart_items])
    
    def clear_cart(self, user: User) -> None:
        all_cart_items = self.cart_repository.get_cart_items_by_user_id(user.id)
        for ci in all_cart_items:
            self.cart_repository.delete_cart_item(ci)

    def checkout(self, user: User, order_service: OrderService) -> list[CartItem]:
        cart_items = self.cart_repository.get_cart_items_by_user_id(user.id)
        if not cart_items:
            raise EmptyItemListError()
        
        req = OrderCreateRequest(
            items=[ItemRequest(item_id=ci.item_id, quantity=ci.quantity) for ci in cart_items]
        )
        order = order_service.create_order(user, req)
        self.clear_cart(user)

        return order