from typing import Annotated
import uuid

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from wapang.app.stores.models import Store
from wapang.database.connection import get_db_session

class StoreRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]) -> None:
        self.session = session

    def create_store(self, store: Store) -> None:
        self.session.add(store)
        self.session.flush()

    def update_store(self, store: Store) -> None:
        self.session.merge(store)
        self.session.flush()

    def get_store_by_id(self, store_id: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.id == store_id))

    def get_store_by_owner_id(self, owner_id: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.owner_id == owner_id))

    def get_store_by_store_name(self, store_name: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.name == store_name))
    
    def get_store_by_email(self, email: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.email == email))
    
    def get_store_by_phone_number(self, phone_number: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.phone_number == phone_number))
    
    def get_store_by_user_id(self, user_id: str) -> Store | None:
        return self.session.scalar(select(Store).where(Store.owner_id == user_id))