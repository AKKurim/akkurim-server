from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, message: str, table: str, id: str) -> None:
        super().__init__(
            status_code=status_code,
            detail={
                "table": table,
                "id": str(id),
                "message": message,
            },
        )


class AlreadyUpdatedError(CustomHTTPException):
    def __init__(
        self,
        table: str,
        id: str,
        detail: str = "The resource was already updated by someone else before your synchronization.",
    ) -> None:
        super().__init__(status_code=409, message=detail, table=table, id=id)


class NotFoundError(CustomHTTPException):
    def __init__(
        self,
        table: str,
        id: str,
        detail: str = "Resource not found.",
    ) -> None:
        super().__init__(status_code=404, message=detail, table=table, id=id)


class AlreadyExistsError(CustomHTTPException):
    def __init__(
        self,
        table: str,
        id: str,
        detail: str = "Resource already exists.",
    ) -> None:
        super().__init__(status_code=409, message=detail, table=table, id=id)


class UniqueViolationErrorHTTP(CustomHTTPException):
    def __init__(
        self,
        table: str,
        column: str,
        value: str,
        detail: str = "Unique violation error.",
    ) -> None:
        # TODO fix this to be more descriptive
        super().__init__(
            status_code=409, message=detail, table=table, id=f"{column}={value}"
        )


class ForeignKeyViolationErrorHTTP(CustomHTTPException):
    def __init__(
        self,
        table: str,
        column: str,
        value: str,
        detail: str = "Foreign key violation error.",
    ) -> None:
        # TODO fix this to be more descriptive
        super().__init__(
            status_code=409, message=detail, table=table, id=f"{column}={value}"
        )
