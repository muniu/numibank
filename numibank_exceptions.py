class CustomerAlreadyExistsError(Exception):
    """Raised when attempting to create a customer that already exists."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CustomerNotFoundError(Exception):
    """Raised when attempting to perform an operation on a non-existent customer."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidLoanAmountError(Exception):
    """Raised when a loan amount falls outside the allowed range OR an overpayment is detected"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
