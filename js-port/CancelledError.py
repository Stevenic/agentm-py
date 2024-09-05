class CancelledError(Exception):
    """
    Represents an error that is returned when an Agent is cancelled.
    """
    def __init__(self, message: str = 'The operation was cancelled.'):
        """
        Creates a new `CancelledError` instance.
        :param message: Optional. Message describing the error.
        """
        super().__init__(message)
        self.name = 'CancelledError'
