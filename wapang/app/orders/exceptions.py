from wapang.common.exceptions import WapangException

class OrderNotFoundError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=404, error_code="ERR_019", error_msg="ORDER NOT FOUND")

class OrderNotOwnedError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=403, error_code="ERR_020", error_msg="NOT YOUR ORDER")

class EmptyItemListError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=422, error_code="ERR_018", error_msg="EMPTY ITEM LIST")

class InvalidOrderStatusError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=409, error_code="ERR_021", error_msg="INVALID ORDER STATUS")
