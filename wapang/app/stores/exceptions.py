from wapang.common.exceptions import WapangException

class StoreAlreadyExistsError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=409, error_code="ERR_008", error_msg="STORE ALREADY EXISTS")

class StoreInfoConflictError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=409, error_code="ERR_009", error_msg="STORE INFO CONFLICT")

class StoreNotFoundError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=404, error_code="ERR_010", error_msg="STORE NOT FOUND")

class StoreNotOwnedError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=403, error_code="ERR_011", error_msg="NO STORE OWNED")

class StoreUpdateForbiddenError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=403, error_code="ERR_012", error_msg="NOT YOUR STORE")