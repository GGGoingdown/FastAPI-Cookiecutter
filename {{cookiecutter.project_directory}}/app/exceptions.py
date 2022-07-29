class InternalException(Exception):
    error_code: int


class BaseInternalServiceException(InternalException):
    tier: str
    entity: str

    def __init__(self, message: str) -> None:
        self.error_message = f"{self.tier} - {self.entity} - {message}"
        super().__init__(f"Ops! Something went wrong. [{self.error_code}]")
