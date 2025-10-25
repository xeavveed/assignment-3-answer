from typing import Annotated

from fastapi import Depends
from wapang.app.users.models import User
from wapang.app.items.schemas import ItemCreateRequest, ItemQueryParams, ItemUpdateRequest
from wapang.app.items.repositories import ItemRepository
from wapang.app.stores.repositories import StoreRepository
from wapang.app.stores.exceptions import StoreNotFoundError, StoreNotOwnedError
from wapang.app.items.exceptions import ItemNotFoundError, ItemNotOwnedError
from wapang.app.items.models import Item
from wapang.common.exceptions import InvalidFormatException

class ItemService:
    def __init__(self, 
                 item_repository: Annotated[ItemRepository, Depends()],
                 store_repository: Annotated[StoreRepository, Depends()]
                 ) -> None:
        self.item_repository = item_repository
        self.store_repository = store_repository

    def create_item(self, user: User, request: ItemCreateRequest) -> Item:
        store = self.store_repository.get_store_by_owner_id(user.id)
        if not store:
            raise StoreNotOwnedError()

        item = Item(name=request.item_name, price=request.price, stock=request.stock, store_id=store.id)
        self.item_repository.create_item(item)
        return item
    

    def update_item(self, user: User, item_id: str, request: ItemUpdateRequest) -> Item:
        store = self.store_repository.get_store_by_owner_id(user.id)
        if not store:
            raise StoreNotOwnedError()

        item = self.item_repository.get_item_by_id(item_id)
        if not item:
            raise ItemNotFoundError()
        if item.store_id != store.id:
            raise ItemNotOwnedError()

        if not any([request.item_name, request.price, request.stock]):
            raise InvalidFormatException()
        
        update_data = request.model_dump(exclude_none=True)
        for key, value in update_data.items():
            if key == "item_name":
                setattr(item, "name", value)
            else:
                setattr(item, key, value)

        self.item_repository.update_item(item)
        return item
    
    def get_items(self, query_params: ItemQueryParams) -> list[Item]:
        if query_params.store_id and self.store_repository.get_store_by_id(query_params.store_id) is None:
            raise StoreNotFoundError()
        items = self.item_repository.get_items(store_id=query_params.store_id,
                                       min_price=query_params.min_price,
                                       max_price=query_params.max_price,
                                       in_stock=query_params.in_stock)
        return items
    
    def delete_item(self, user: User, item_id: str) -> None:
        store = self.store_repository.get_store_by_owner_id(user.id)
        if not store:
            raise StoreNotOwnedError()

        item = self.item_repository.get_item_by_id(item_id)
        if not item:
            raise ItemNotFoundError()
        if item.store_id != store.id:
            raise ItemNotOwnedError()

        self.item_repository.delete_item(item)

    def get_store_items(self, store_id: str) -> list[Item]:
        if self.store_repository.get_store_by_id(store_id) is None:
            raise StoreNotFoundError()
        return self.item_repository.get_items(store_id=store_id)