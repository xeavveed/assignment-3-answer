from typing import Annotated
from fastapi import APIRouter, Depends

from wapang.app.auth.utils import login_with_header
from wapang.app.users.models import User
from wapang.app.users.schemas import UserSignupRequest, UserUpdateRequest, UserResponse
from wapang.app.users.services import UserService
from wapang.app.orders.services import OrderService
from wapang.app.orders.schemas import OrderUserResponse
from wapang.app.reviews.services import ReviewService
from wapang.app.reviews.schemas import ReviewUserResponse

user_router = APIRouter()


@user_router.post("/", status_code=201)
def signup(
    signup_request: UserSignupRequest, user_service: Annotated[UserService, Depends()]
) -> UserResponse:
    user = user_service.create_user(
        signup_request.email, signup_request.password,
    )
    return UserResponse(
        id=user.id,
        email=user.email,
        nickname=user.nickname,
        address=user.address,
        phone_number=user.phone_number,
    )

@user_router.get("/me", status_code=200)
def get_me(
    user: Annotated[User, Depends(login_with_header)],
    ) -> UserResponse:
    return UserResponse.model_validate(user)

@user_router.patch("/me", status_code=200)
def update_me(
    user: Annotated[User, Depends(login_with_header)],
    request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends()]) -> UserResponse:
    updated_user = user_service.update_user(request=request, user=user)
    return UserResponse.model_validate(updated_user)

@user_router.get("/me/orders", status_code=200)
def get_my_orders(
    user: Annotated[User, Depends(login_with_header)],
    order_service: Annotated[OrderService, Depends()]
) -> list[OrderUserResponse]:
    orders = order_service.get_orders_by_user(user.id)
    return [OrderUserResponse(
        order_id=order.id,
        total_price=order.total_price,
        status=order.status,
    ) for order in orders]

@user_router.get("/me/reviews", status_code=200)
def get_my_reviews(
    user: Annotated[User, Depends(login_with_header)],
    review_service: Annotated[ReviewService, Depends()]
) -> list[ReviewUserResponse]:
    reviews = review_service.get_reviews_by_user(user.id)
    return [ReviewUserResponse(
        review_id=review.id,
        item_id=review.item_id,
        item_name=review.item.name,
        rating=review.rating,
        comment=review.comment,
    ) for review in reviews]