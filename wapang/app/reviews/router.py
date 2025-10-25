from typing import Annotated
from fastapi import APIRouter, Depends, Query

from wapang.app.auth.utils import login_with_header, login_with_header_optional
from wapang.app.reviews.schemas import ReviewUpdateRequest, ReviewResponse
from wapang.app.reviews.services import ReviewService
from wapang.app.users.models import User


review_router = APIRouter()

@review_router.get("/{review_id}", status_code=200, 
                     response_model=ReviewResponse,
                   response_model_exclude_none=True)
def get_review(
    review_id: str,
    user: Annotated[User | None, Depends(login_with_header_optional)],
    review_service: Annotated[ReviewService, Depends()],
) -> ReviewResponse:
    review = review_service.get_review(review_id)
    return ReviewResponse(
        review_id=review.id,
        item_id=review.item_id,
        writer_nickname=review.user.nickname or "",
        is_writer=(review.user_id == user.id) if user is not None else None,
        rating=review.rating,
        comment=review.comment,
    )

@review_router.patch("/{review_id}", status_code=200)
def update_review(
    review_id: str,
    user: Annotated[User, Depends(login_with_header)],
    request: ReviewUpdateRequest,
    review_service: Annotated[ReviewService, Depends()],
):
    updated_review = review_service.update_review(review_id, user, request)
    return ReviewResponse(
        review_id=updated_review.id,
        item_id=updated_review.item_id,
        writer_nickname=updated_review.user.nickname or "",
        is_writer=(updated_review.user_id == user.id),
        rating=updated_review.rating,
        comment=updated_review.comment,
    )

@review_router.delete("/{review_id}", status_code=204)
def delete_review(
    review_id: str,
    user: Annotated[User, Depends(login_with_header)],
    review_service: Annotated[ReviewService, Depends()],
):
    review_service.delete_review(review_id, user)
