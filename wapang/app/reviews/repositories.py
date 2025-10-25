from typing import Annotated
import uuid

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from wapang.app.reviews.models import Review
from wapang.database.connection import get_db_session

class ReviewRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def create_review(self, review: Review) -> None:
        self.session.add(review)
        self.session.flush()

    def get_review_by_id(self, review_id: str) -> Review | None:
        return self.session.scalar(select(Review).where(Review.id == review_id))
    
    def update_review(self, review: Review) -> None:
        self.session.merge(review)
        self.session.flush()
    
    def delete_review(self, review: Review) -> None:
        self.session.delete(review)

    def get_reviews_by_user_id(self, user_id: str) -> list[Review]:
        return list(self.session.scalars(select(Review).where(Review.user_id == user_id)).all())
    
    def get_review_by_user_and_item(self, user_id: str, item_id: str) -> Review | None:
        return self.session.scalar(select(Review).where(Review.user_id == user_id, Review.item_id == item_id))
    
    def get_reviews_by_item_id(self, item_id: str) -> list[Review]:
        return list(self.session.scalars(select(Review).where(Review.item_id == item_id)).all())