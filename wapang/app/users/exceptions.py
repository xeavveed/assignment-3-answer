from wapang.common.exceptions import WapangException

class EmailAlreadyExistsException(WapangException):
    def __init__(self) -> None:
        super().__init__(
            status_code=409, 
            error_code="ERR_004", 
            error_msg="EMAIL ALREADY EXISTS"
        )

class NicknameNotSetError(WapangException):
    def __init__(self) -> None:
        super().__init__(status_code=422, error_code="ERR_015", error_msg="NICKNAME NOT SET")