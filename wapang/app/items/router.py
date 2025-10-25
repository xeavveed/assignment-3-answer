from typing import Annotated
from fastapi import APIRouter, Depends, Query

from wapang.app.auth.utils import login_with_header, login_with_header_optional
from wapang.app.reviews.schemas import ReviewCreateRequest, ReviewResponse
from wapang.app.reviews.services import ReviewService
from wapang.app.users.models import User
from wapang.app.items.schemas import ItemCreateRequest, ItemResponse, ItemUpdateRequest, ItemQueryParams
from wapang.app.items.services import ItemService

item_router = APIRouter()

@item_router.post("/", status_code=201)
def create_item(
    user: Annotated[User, Depends(login_with_header)],
    request: ItemCreateRequest,
    item_service: Annotated[ItemService, Depends()],
) -> ItemResponse:
    item = item_service.create_item(user, request)
    return ItemResponse(
        id=item.id,
        item_name=item.name,
        price=item.price,
        stock=item.stock
    )

@item_router.patch("/{item_id}", status_code=200)
def update_item(
    user: Annotated[User, Depends(login_with_header)],
    item_id: str,
    request: ItemUpdateRequest,
    item_service: Annotated[ItemService, Depends()],
):
    updated_item = item_service.update_item(user, item_id, request)
    return ItemResponse(
        id=updated_item.id,
        item_name=updated_item.name,
        price=updated_item.price,
        stock=updated_item.stock
    )

@item_router.get("/", status_code=200)
def get_items(
    query_params: Annotated[ItemQueryParams, Query()],
    item_service: Annotated[ItemService, Depends()],
):
    items = item_service.get_items(query_params)
    return [ItemResponse(
        id=item.id,
        item_name=item.name,
        price=item.price,
        stock=item.stock
    ) for item in items]

@item_router.delete("/{item_id}", status_code=204)
def delete_item(
    user: Annotated[User, Depends(login_with_header)],
    item_id: str,
    item_service: Annotated[ItemService, Depends()],
):
    item_service.delete_item(user, item_id)

@item_router.post("/{item_id}/reviews", status_code=201)
def create_review(
    user: Annotated[User, Depends(login_with_header)],
    item_id: str,
    request: ReviewCreateRequest,
    review_service: Annotated[ReviewService, Depends()],
):
    review = review_service.create_review(user, item_id, request)
    return ReviewResponse(
        review_id=review.id,
        item_id=review.item_id,
        writer_nickname=review.user.nickname or "",
        is_writer=True,
        rating=review.rating,
        comment=review.comment,
    )

@item_router.get(
    "/{item_id}/reviews",
    status_code=200,
    response_model=list[ReviewResponse],
    response_model_exclude_none=True,
)
def get_item_reviews(
    item_id: str,
    user: Annotated[User | None, Depends(login_with_header_optional)],
    review_service: Annotated[ReviewService, Depends()],
):
    reviews = review_service.get_reviews_by_item(item_id)
    return [ReviewResponse(
        review_id=review.id,
        item_id=review.item_id,
        writer_nickname=review.user.nickname or "",
        is_writer=(review.user_id == user.id) if user is not None else None,
        rating=review.rating,
        comment=review.comment,
    ) for review in reviews]
