from wapang.common.exceptions import WapangException

class ItemNotFoundError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=404, error_code="ERR_013", error_msg="ITEM NOT FOUND")

class ItemNotOwnedError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=403, error_code="ERR_014", error_msg="NOT YOUR ITEM")

class ItemNotEnoughStockError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=409, error_code="ERR_017", error_msg="NOT ENOUGH STOCK")