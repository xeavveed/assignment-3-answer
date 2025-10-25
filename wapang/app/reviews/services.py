from typing import Annotated

from fastapi import Depends
from wapang.app.items.exceptions import ItemNotFoundError
from wapang.app.items.repositories import ItemRepository
from wapang.app.reviews.schemas import ReviewCreateRequest, ReviewUpdateRequest
from wapang.app.users.models import User
from wapang.app.reviews.models import Review
from wapang.app.reviews.repositories import ReviewRepository
from wapang.app.reviews.exceptions import ReviewNotFoundError, ReviewNotOwnedError, ReviewAlreadyExistsError
from wapang.app.users.exceptions import NicknameNotSetError
from wapang.common.exceptions import InvalidFormatException

class ReviewService:
    def __init__(self, 
                 review_repository: Annotated[ReviewRepository, Depends()],
                 item_repository: Annotated[ItemRepository, Depends()],
                 ) -> None:
        self.review_repository = review_repository
        self.item_repository = item_repository

    def create_review(self, user: User, item_id: str, request: ReviewCreateRequest) -> Review:
        item = self.item_repository.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        if user.nickname is None:
            raise NicknameNotSetError()
        
        if self.review_repository.get_review_by_user_and_item(user.id, item_id) is not None:
            raise ReviewAlreadyExistsError()
        
        review = Review(user_id=user.id, item_id=item_id, rating=request.rating, comment=request.comment)
        self.review_repository.create_review(review)
        return review

    def get_review(self, review_id: str) -> Review:
        review = self.review_repository.get_review_by_id(review_id)
        
        if review is None:
            raise ReviewNotFoundError()
        
        return review

    def update_review(self, review_id: str, user: User, request: ReviewUpdateRequest) -> Review:
        review = self.review_repository.get_review_by_id(review_id)

        if review is None:
            raise ReviewNotFoundError()

        if review.user_id != user.id:
            raise ReviewNotOwnedError()

        if not any([request.rating, request.comment]):
            raise InvalidFormatException()
        
        for key, value in request.model_dump(exclude_none=True).items():
            setattr(review, key, value)

        self.review_repository.update_review(review)
        return review
    
    def delete_review(self, review_id: str, user: User) -> None:
        review = self.review_repository.get_review_by_id(review_id)

        if review is None:
            raise ReviewNotFoundError()

        if review.user_id != user.id:
            raise ReviewNotOwnedError()

        self.review_repository.delete_review(review)

    def get_reviews_by_user(self, user_id: str) -> list[Review]:
        return self.review_repository.get_reviews_by_user_id(user_id)
    
    def get_reviews_by_item(self, item_id: str) -> list[Review]:
        if self.item_repository.get_item_by_id(item_id) is None:
            raise ItemNotFoundError()
        return self.review_repository.get_reviews_by_item_id(item_id)