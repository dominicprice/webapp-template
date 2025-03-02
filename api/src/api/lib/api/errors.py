from fastapi import HTTPException


class NotFound(HTTPException):
    def __init__(self, detail: str = "not found"):
        super().__init__(404, detail)


class InvalidArgument(HTTPException):
    def __init__(self, detail: str = "invalid argument"):
        super().__init__(400, detail)


class NotImplemented(HTTPException):
    def __init__(self, detail: str = "not implemented"):
        super().__init__(501, detail)
