from decimal import Decimal
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
        self, customer_id: int, customer_name: str,amount: Decimal, interest_rate: Decimal
    ):
        """
        Initializes a Loan object.

        Args:
        customer_id: The customer's ID.
        customer_name: The customer's name.
        amount: The loan amount (positive decimal).
        interest_rate: The interest rate as a decimal between 0.0 (inclusive) and 1.0 (inclusive).
        Raises:
        ValueError: If the amount or interest rate is invalid.
        """
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.amount = amount
        self.interest_rate = interest_rate
        #self.repayments = []  # List to store repayment amounts.
        self.repayments: list[Decimal] = []  # List to store repayment amounts (as Decimals)


        self.validate_loan_amount(amount)
        self.validate_interest_rate(interest_rate)

    def validate_loan_amount(self, amount):
        """
        Validate that the loan amount is within the range allowed
        """
        Validator.is_valid_loan_amount(amount)

    def validate_interest_rate(self, interest_rate):
        """
        Validate that the interest rate is within the allowed range
        """
        Validator.is_valid_interest_rate(interest_rate)


    @property
    def outstanding_debt(self):
        """
        Calculates and returns the outstanding debt for the loan (including accrued interest).

        This assumes simple interest, where interest is charged only on the original loan amount.
        TODO For more complex scenarios, we should consider implementing compound interest.
        """
        if not self.repayments:  # This ensures that if there are no repayments, we simply return the original loan amount to avoid division by zero.
            return self.amount
        total_interest = self.amount * self.interest_rate
        return self.amount + total_interest - sum(self.repayments)

    def add_repayment(self, amount: float) -> None:
        """
        Adds a repayment to the loan.

        Args:
            amount: The repayment amount (as a Decimal).

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