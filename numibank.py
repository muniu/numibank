from typing import (
    Optional,
    Dict,
)  # TODO I need to refresh my understanding of type hinting using the typing module. A bit rusty coming from pre-python3.5 era.
from decimal import Decimal
from numibank_exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
    InvalidLoanAmountError,
)
from models import Customer, Loan


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
    customer = bank.create_customer(1001, "Muniu Kariuki")
    # Grant a loan to the customer
    loan = bank.lend(customer.customer_id, customer.name, Decimal(100.0), Decimal(0.05)) # 5% interest rate and our max we can loan is 100
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

    def __init__(self, min_loan_amount=10, max_loan_amount=100):
        self.customers = (
            {}
        )  # Dictionary to store customers (key: customer_id, value: Customer object)
        self.loans = (
            {}
        )  # Dictionary to store loans (key: customer_id, value: Loan object)
        self.min_loan_amount = min_loan_amount
        self.max_loan_amount = max_loan_amount

    def create_customer(self, customer_id: int, name: str) -> Customer:
        """
        Creates a new customer in the bank's system.

        Args:
            customer_id: The unique identifier for the customer (integer).
            name: The customer's full name (string).

        Returns:
            A Customer object representing the newly created customer.

        Raises:
            CustomerAlreadyExistsError: If a customer with the provided ID already exists.
        """
        if customer_id in self.customers:
            raise CustomerAlreadyExistsError(
                f"Customer with ID {customer_id} already exists"
            )
        customer = Customer(customer_id, name)
        self.customers[customer_id] = customer
        return customer

    def lend(
        self, customer_id: int, name: str, amount: Decimal, interest_rate: Decimal = 0.0) -> Loan:
        """
        Initiates a loan for a customer, creating a new Loan object.

        Args:
        customer_id: The unique integer identifier for the customer.
        name: The customer's full name as a string.
        amount: The loan amount as a positive number.
        interest_rate: The interest rate for the loan (default 0.0). By assigning a default value,
        interest_rate becomes an optional argument, & you can omit the interest_rate argument if you want a loan with zero interest.

        Returns:
        A Loan object representing the created loan, or None if loan creation fails.

        Raises:
        CustomerNotFoundError: If a customer with the provided ID is not found.
        InvalidLoanAmountError: If the loan amount falls outside the allowed range.
        """
        if not customer_id in self.customers:
            raise CustomerNotFoundError(
                f"Customer with ID {customer_id} does not exist"
            )
        try:
            loan = Loan(customer_id, name, amount, interest_rate
            )  # Validation happens in Loan constructor
            self.loans[customer_id] = loan
            return loan
        except (CustomerNotFoundError, InvalidLoanAmountError) as e:
            # Re-raise the exception for the calling code to handle.
            # Figured might be better than print, as it offers more flexibility for the caller.
            # TODO could go as far as defining error codes (e.g., integers) to represent different failure scenarios and return the code instead of None.
            # The calling code would then need to check the return value and handle the error accordingly.
            raise e

    def repay(self, customer_id: int, amount: Decimal) -> None:
        """
        Processes a loan repayment for a customer.

        Args:
            customer_id: The unique integer identifier for the customer.
            amount: The amount being repaid as a positive number.

        Raises:
            CustomerNotFoundError: If a customer with the provided ID is not found.
            InvalidLoanAmountError: If an attempt to overpay an existing loan happens.
        """
        loan = self.loans.get(customer_id)  # Use get to handle non-existent customer_id
        if not loan:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
        loan = self.loans[customer_id]
        
        remaining_balance = loan.outstanding_debt - sum(
            repayment for repayment in loan.repayments
        )
        # Check for overpayment and provide informative message
        if amount > remaining_balance:
            raise InvalidLoanAmountError(f"Repayment amount {amount} exceeds outstanding debt")
            #return  # Exit the function if overpayment is attempted? 

        # Apply repayment logic if amount is less than or equal to remaining balance
        loan.repayments.append(amount)
        
        print(f"Repayment of {amount} successfully processed.")

    def get_customer_info(self, customer_id: int) -> Optional[Dict]:
        """
        Retrieves and returns a dictionary containing customer information and loan details for a given customer ID.

        Args:
        customer_id: The unique integer identifier for the customer.

        Returns:
        A dictionary containing customer information (name) and loan details (total loan amount, interest rate, total repayments, outstanding debt),
        or None if the customer is not found.

        Raises:
        CustomerNotFoundError: If a customer with the provided ID is not found.
        """
        loan = self.loans.get(customer_id)
        if not loan:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found")
