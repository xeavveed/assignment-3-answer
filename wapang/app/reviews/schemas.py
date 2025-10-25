from pydantic import BaseModel
from typing import Annotated
from pydantic.functional_validators import AfterValidator
from wapang.app.users.schemas import skip_none
from wapang.common.exceptions import InvalidFormatException

def validate_rating(v: int) -> int:
    if v < 1 or v > 5:
        raise InvalidFormatException()
    return v

def validate_comment(v: str) -> str:
    if not v or len(v) > 500:
        raise InvalidFormatException()
    return v

class ReviewCreateRequest(BaseModel):
    rating: Annotated[int, AfterValidator(validate_rating)]
    comment: Annotated[str, AfterValidator(validate_comment)]

class ReviewUpdateRequest(BaseModel):
    rating: Annotated[int | None, AfterValidator(skip_none(validate_rating))] = None
    comment: Annotated[str | None, AfterValidator(skip_none(validate_comment))] = None

class ReviewUserResponse(BaseModel):
    review_id: str
    item_id: str
    item_name: str
    rating: int
    comment: str

class ReviewResponse(BaseModel):
    review_id: str
    item_id: str
    writer_nickname: str
    is_writer: bool | None
    rating: int
    comment: str