from copy import copy
from dataclasses import dataclass, field
from decimal import Decimal
from typing import TypedDict, Optional
from uuid import uuid4

import constants
from numibank_exceptions import InvalidLoanAmountError, NumiBankError, InvalidInterestRateError, \
    InvalidLoanRepaymentAmountError
from numibank_validators import Validator


@dataclass
class Customer:
    """
    Customer Object

    Args:
        id: A unique id.
        name: The name of the customer.
    """
    name: str
    # collision of ids is possible, so we use a unique id
    id: str = field(default_factory=lambda: str(uuid4()))


class Loan:
    """
    Loan Object
    """

    def __init__(
            self,
            customer: Customer,
            amount: Decimal,
            interest_rate: Decimal,
    ):
        """
        Initializes a Loan object.

        Args:
        customer_id: The customer's ID.
        customer_name: The customer's name.
        amount: The loan amount (positive decimal).
        interest_rate: The interest rate as a decimal between 0.0 (inclusive) and 1.0 (inclusive).
        Raises:
        InvalidInterestRateError: If interest rate is invalid.
        InvalidLoanAmountError: If the loan amount is invalid.
        """
        if Validator.is_within_range(interest_rate, constants.MINIMUM_INTEREST_RATE, constants.MAXIMUM_INTEREST_RATE):
            self.interest_rate = interest_rate
        else:
            raise InvalidInterestRateError(
                f"Interest rate must be between {str(constants.MINIMUM_INTEREST_RATE)} "
                f"and {str(constants.MAXIMUM_INTEREST_RATE)}"
            )

        if not Validator.is_within_range(amount, constants.MINIMUM_LOAN_AMOUNT, constants.MAXIMUM_LOAN_AMOUNT):
            raise InvalidLoanAmountError(
                f"Loan amount must be between {constants.MINIMUM_LOAN_AMOUNT} "
                f"and {constants.MAXIMUM_LOAN_AMOUNT}"
            )

        self.amount = amount

        if isinstance(customer, Customer):
            self.customer = customer
        else:
            raise NumiBankError("Invalid customer object")

        self._repayments: list[Decimal] = []

    @property
    def outstanding_debt(self):
        """
        Calculates and returns the outstanding debt for the loan (including accrued interest).

        This assumes simple interest, where interest is charged only on the original loan amount.
        TODO For more complex scenarios, we should consider implementing compound interest.
        """
        if not self._repayments:
            # This ensures that if there are no repayments, we simply return the original loan amount
            return self.amount

        total_interest = self.amount * self.interest_rate
        return self.amount + total_interest - self.total_repayments

    @property
    def total_repayments(self):
        """
        Returns the total repayments made so far.
        """
        return sum(self._repayments)

    @property
    def repayments(self):
        """
        Returns a copy of the loan's repayment list. Late addition to help unit tests instead of asserting a print statement
        """
        return copy(self._repayments)  # Return a copy to avoid modification

    def add_repayment(self, amount: Decimal) -> None:
        """
        Adds a repayment to the loan.

        Args:
            amount: The repayment amount (as a Decimal).

        Raises:
            InvalidLoanAmountError: If the repayment amount is negative or exceeds the outstanding debt.
        """
        if not Validator.is_positive(amount):
            raise InvalidLoanRepaymentAmountError("Amount must be positive")

        if amount > self.outstanding_debt:
            raise InvalidLoanRepaymentAmountError("Amount exceeds outstanding debt")

        self._repayments.append(amount)


CustomerInfo = TypedDict('CustomerInfo', {'customer': Customer, 'loan': Optional[Loan]})
