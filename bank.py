from decimal import Decimal
from typing import (
    Optional,
)  # TODO I need to refresh my understanding of type hinting using the typing module. A bit rusty coming from pre-python3.5 era.

import constants
from models import Customer, Loan, CustomerInfo
from numibank_exceptions import (
    CustomerNotFoundError,
    CustomerHasOutstandingLoanError, InvalidLoanAmountError, LoanNotFoundError,
)

import logging

logger = logging.getLogger(__name__)


class NumiBank:
    """
    A simple loan management system that allows you to create customers, manage loans,
    and process repayments.

    This class provides methods for:
        - Creating customers (`create_customer`)
        - Granting loans to customers (`lend`)
        - Processing loan repayments (`repay`)
        - Retrieving customer + loan information (`get_customer_info`)

    **Example Usage:**

    ```python
    # Example usage:

    from numibank import NumiBank
    bank = NumiBank()
    # Create a customer
    customer = bank.create_customer("Muniu Kariuki")
    # Grant a loan to the customer
    loan = bank.lend(customer.customer_id, Decimal(100.0), Decimal(0.05)) # 5% interest rate and our max we can loan is 100
    # Fetch  the outstanding
    outstanding_debt = loan.outstanding_debt
    print(f"Outstanding debt (no repayments yet): {outstanding_debt}")  # Expected Output: 105
    # let’s do a repayement
    loan.add_repayment(Decimal(5.0))  # Add a repayment
    print(f"Outstanding debt after repayment: {loan.outstanding_debt}")  # Expected Output: 100

    # Get customer information and loan details
    customer_info = bank.get_customer_info(customer_id)
    print(customer_info)
    """

    def __init__(self):
        # Dictionary to store customers (key: customer_id, value: Customer object)
        self.customers: dict[str, Customer] = {}
        # Dictionary to store loans (key: customer_id, value: Loan object)
        self.loans: dict[str, Loan] = {}

    def create_customer(self, name: str) -> Customer:
        """
        Creates a new customer in the bank's system.

        Args:
            name: The customer's full name (string).

        Returns:
            A Customer object representing the newly created customer.
        """
        customer = Customer(name)
        self.customers[customer.id] = customer

        return customer

    def lend(
            self, customer_id: str, amount: Decimal, interest_rate: Decimal = constants.DEFAULT_INTEREST_RATE
    ) -> Loan:
        """
        Initiates a loan for a customer, creating a new Loan object.

        Args:
        customer_id: The unique identifier for the customer.
        amount: The loan amount as a positive decimal.
        interest_rate: The interest rate for the loan (default set in constants). By assigning a default value,
        interest_rate becomes an optional argument, & you can omit the interest_rate argument if you want a loan with zero interest.

        Returns:
        A Loan object representing the created loan, or None if loan creation fails.

        Raises:
        CustomerNotFoundError: If a customer with the provided ID is not found.
        InvalidLoanAmountError: If the loan amount falls outside the allowed range.
        CustomerHasOutstandingLoanError: If the customer already has an outstanding loan.
        """
        customer = self._get_customer(customer_id)
        if customer_id in self.loans:
            raise CustomerHasOutstandingLoanError(
                f"Customer with ID {customer_id} already has an outstanding loan"
            )

        loan = Loan(customer, amount, interest_rate)  # Validation happens in Loan constructor
        self.loans[customer_id] = loan

        return loan

    def _get_customer(self, customer_id: str) -> Customer:
        try:
            return self.customers[customer_id]
        except KeyError:
            raise CustomerNotFoundError(
                f"Customer with ID {customer_id} does not exist"
            )

    def repay(self, customer_id: str, amount: Decimal) -> None:
        """
        Processes a loan repayment for a customer.

        Args:
            customer_id: The unique integer identifier for the customer.
            amount: The amount being repaid as a positive number.

        Raises:
            CustomerNotFoundError: If a customer with the provided ID is not found.
            LoanNotFoundError: If the customer does not have an existing loan.
            InvalidLoanAmountError: If an attempt to overpay an existing loan happens.
        """
        customer = self._get_customer(customer_id)

        try:
            loan = self.loans[customer_id]
        except KeyError:
            raise LoanNotFoundError(f"Customer with ID {customer.id} does not have an outstanding loan")

        loan.add_repayment(amount)

        logger.info(f"Repayment of {amount} successfully processed.")

    def get_customer_info(self, customer_id: str) -> Optional[CustomerInfo]:
        """
        Retrieves and returns a dictionary containing customer information and loan details for a given customer ID.

        Args:
        customer_id: The unique integer identifier for the customer.

        Returns:
        A dictionary containing customer information (name) and loan
        or None if the customer is not found.

        """
        try:
            customer = self._get_customer(customer_id)
        except CustomerNotFoundError:
            return None

        loan = self.loans.get(customer_id)

        return CustomerInfo(customer=customer, loan=loan)
