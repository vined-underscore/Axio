class InvalidToken(Exception):
    """
    Custom exception for token commands
    """
    def __init__(self):
        self.message = "You provided an invalid token."
        super().__init__(self.message)


class AxioException(Exception):
    """
    Custom exception to display errors on Discord
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
