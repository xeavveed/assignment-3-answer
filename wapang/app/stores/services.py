from typing import Annotated

from fastapi import Depends
from wapang.common.exceptions import InvalidFormatException
from wapang.app.stores.exceptions import StoreNotFoundError, StoreNotOwnedError, StoreUpdateForbiddenError
from wapang.app.stores.schemas import StoreCreateRequest, StoreUpdateRequest
from wapang.app.users.models import User
from wapang.app.stores.models import Store
from wapang.app.stores.repositories import StoreRepository
from wapang.app.stores.exceptions import StoreAlreadyExistsError, StoreInfoConflictError

class StoreService:
    def __init__(self, store_repository: Annotated[StoreRepository, Depends()]) -> None:
        self.store_repository = store_repository

    def create_store(self, user: User, request: StoreCreateRequest) -> Store:
        if self.store_repository.get_store_by_owner_id(user.id):
            raise StoreAlreadyExistsError()

        if self.store_repository.get_store_by_store_name(request.store_name) \
            or self.store_repository.get_store_by_email(request.email) \
            or self.store_repository.get_store_by_phone_number(request.phone_number):
            raise StoreInfoConflictError()

        store = Store(
            name=request.store_name,
            address=request.address,
            email=request.email,
            phone_number=request.phone_number,
            delivery_fee=request.delivery_fee,
            owner_id=user.id
        )

        self.store_repository.create_store(store)
        return store

    def update_store(self, user: User, store_id: str, request: StoreUpdateRequest) -> Store:
        store = self.store_repository.get_store_by_id(store_id)
        if not store:
            raise StoreNotFoundError()

        owner = self.store_repository.get_store_by_user_id(user.id)

        if owner and store.owner_id != user.id:
            raise StoreUpdateForbiddenError()

        if owner is None:
            raise StoreNotOwnedError()

        if not any([request.store_name, request.address, request.email, request.phone_number, request.delivery_fee]):
            raise InvalidFormatException()
        
        if (request.store_name and request.store_name != store.name and self.store_repository.get_store_by_store_name(request.store_name)):
            raise StoreInfoConflictError()
        if (request.email and request.email != store.email and self.store_repository.get_store_by_email(request.email)):
            raise StoreInfoConflictError()
        if (request.phone_number and request.phone_number != store.phone_number and self.store_repository.get_store_by_phone_number(request.phone_number)):
            raise StoreInfoConflictError()

        data = request.model_dump(exclude_none=True)
        if "store_name" in data:
            store.name = data.pop("store_name")
        for key, value in data.items():
            setattr(store, key, value)
        self.store_repository.update_store(store)
        return store
    
    def get_store_by_id(self, store_id: str) -> Store:
        store = self.store_repository.get_store_by_id(store_id)
        if not store:
            raise StoreNotFoundError()
        return store