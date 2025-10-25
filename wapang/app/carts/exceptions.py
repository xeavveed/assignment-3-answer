from wapang.common.exceptions import WapangException

class EmptyItemListError(WapangException):
    def __init__(self):
        super().__init__(status_code=422, error_code="ERR_024", error_msg="EMPTY ITEM LIST")