from typing import Annotated
from fastapi import APIRouter, Depends

from wapang.app.items.services import ItemService
from wapang.app.stores.models import Store
from wapang.app.users.models import User
from wapang.app.stores.services import StoreService
from wapang.app.stores.schemas import StoreCreateRequest, StoreUpdateRequest, StoreResponse
from wapang.app.items.schemas import ItemResponse
from wapang.app.auth.utils import login_with_header

store_router = APIRouter()

@store_router.post("/", status_code=201)
def create_store(
    user: Annotated[User, Depends(login_with_header)],
    request: StoreCreateRequest,
    store_service: Annotated[StoreService, Depends()]
) -> StoreResponse:
    store =  store_service.create_store(user, request)
    return StoreResponse(
        id=store.id,
        store_name=store.name,
        address=store.address,
        email=store.email,
        phone_number=store.phone_number,
        delivery_fee=store.delivery_fee,
    )

@store_router.patch("/{store_id}", status_code=200)
def update_store(
    store_id: str,
    user: Annotated[User, Depends(login_with_header)],
    request: StoreUpdateRequest,
    store_service: Annotated[StoreService, Depends()]
) -> StoreResponse:
    updated_store = store_service.update_store(user=user, store_id=store_id, request=request)
    return StoreResponse(
        id=updated_store.id,
        store_name=updated_store.name,
        address=updated_store.address,
        email=updated_store.email,
        phone_number=updated_store.phone_number,
        delivery_fee=updated_store.delivery_fee,
    )


@store_router.get("/{store_id}", status_code=200)
def get_store(
    store_id: str,
    store_service: Annotated[StoreService, Depends()]
) -> StoreResponse:
    store = store_service.get_store_by_id(store_id=store_id)
    return StoreResponse(
        id=store.id,
        store_name=store.name,
        address=store.address,
        email=store.email,
        phone_number=store.phone_number,
        delivery_fee=store.delivery_fee,
    )

@store_router.get("/{store_id}/items", status_code=200)
def get_store_items(
    store_id: str,
    item_service: Annotated[ItemService, Depends()]
) -> list[ItemResponse]:
    items = item_service.get_store_items(store_id=store_id)
    return [ItemResponse(
        id=item.id,
        item_name=item.name,
        price=item.price,
        stock=item.stock
    ) for item in items]