from numibank_validators import Validator


class Customer:
    """
    Customer Object
    """

    def __init__(self, customer_id: int, name: str):
        """
        Initializes a Customer object.

        Args:
        customer_id: A unique id.
        name: The name of the customer.
        """
        self.customer_id = customer_id
        self.name = name

    @property
    def id(self):
        return self.customer_id


class Loan:
    """
    Loan Object
    """

    def __init__(
        self, customer_id: int, amount: float, interest_rate: float, customer_name: str
    ):
        """
        Initializes a Loan object.

        Args:
        customer_id: The customer's ID.
        amount: The loan amount (positive float).
        interest_rate: The interest rate (0.0 to 1.0, representing a percentage).
        customer_name: The customer's name.

        Raises:
        ValueError: If the amount or interest rate is invalid.
        """
        self.customer_id = customer_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.customer_name = customer_name
        self.repayments = []  # List to store repayment amounts.

        self.validate_loan_amount(amount)
        self.validate_interest_rate(interest_rate)

    def validate_loan_amount(self, amount):
        """
        TODO this docstring in a while
        """
        Validator.is_valid_loan_amount(amount)

    def validate_interest_rate(self, interest_rate):
        """
        TODO this docstring in a while
        """
        Validator.is_valid_interest_rate(interest_rate)

    @property
    def outstanding_debt(self):
        """
        Calculates and returns the outstanding debt for the loan.
        This is implemented as read-only (without a seeter) to prevent accidental modification of the calculated value.
        """
        return self.amount * (1 + self.interest_rate) - sum(
            repayment for repayment in self.repayments
        )

    def add_repayment(self, amount: float) -> None:
        """
        Adds a repayment to the loan.

        Args:
            amount: The repayment amount.

        Raises:
            ValueError: If the repayment amount is not positive.
        """
        try:
            Validator.is_positive(amount)
            self.repayments.append(amount)
        except ValueError as e:
            raise ValueError(
                f"Invalid repayment amount: {e}"
            ) from e  # "e" preserves the original traceback for better debugging in absence of my beloved  printstacktrace in java
    
    def get_repayments(self):
        """
        Returns a copy of the loan's repayment list. Late addition to help unit tests instead of asserting a print statement
        """
        return self.repayments[:]  # Return a copy to avoid modification
