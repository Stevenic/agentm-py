class RequestError(Exception):
    """
    Represents an error that occurred during a model request.
    """

    def __init__(self, message: str, status: int, name: str = 'RequestError'):
        """
        Creates a new `RequestError` instance.

        :param message: Message describing the error.
        :param status: HTTP status code of the error.
        :param name: Optional. Name of the error.
        """
        super().__init__(message)
        self.status = status
        self.name = name

    @property
    def status_code(self) -> int:
        """
        HTTP status code of the error.
        """
        return self.status
