class NumiBankError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.message}'


class CustomerAlreadyExistsError(NumiBankError):
    """Raised when attempting to create a customer that already exists."""
    ...


class CustomerNotFoundError(NumiBankError):
    """Raised when attempting to perform an operation on a non-existent customer."""
    ...


class InvalidLoanAmountError(NumiBankError):
    """Raised when a loan amount falls outside the allowed range OR an overpayment is detected"""
    ...


class InvalidInterestRateError(NumiBankError):
    ...


class InvalidLoanRepaymentAmountError(NumiBankError):
    ...


class LoanNotFoundError(NumiBankError):
    ...


class CustomerHasOutstandingLoanError(NumiBankError):
    """Raised when attempting to lend to a customer who already has an outstanding loan."""
    ...
