import unittest
import uuid
from decimal import Decimal

import constants
from bank import NumiBank
from models import Customer, Loan
from numibank_exceptions import (
    CustomerHasOutstandingLoanError,
    CustomerNotFoundError,
    InvalidInterestRateError,
    InvalidLoanAmountError,
    InvalidLoanRepaymentAmountError,
    LoanNotFoundError,
    NumiBankError,
)


class TestNumiBank(unittest.TestCase):
    """
    Test Runner for the edge cases of the numibank class
    Customer Management:
        Creating a customer with an already existing ID (test_create_customer_already_exists)
    Loan Management:
        Granting a loan to a non-existent customer (test_lend_customer_not_found)
        Loan amount validation (assuming ValueError is raised for invalid amounts in Loan constructor) (test_lend_invalid_loan_amount)
        Loan repayment processing (test_repay_success)
    Loan Repayment Scenarios:
        Partial loan repayment (test_loan_repayment_scenario)
        Attempting to overpay a loan (test_loan_repayment_scenario)
    Not handled at the moment:
        Loan Validation: Expand current tests to cover more scenarios like negative, overpayment etc. Also consider more contexual errors.
        Loan Repayment: Same as above, and specifially to habdle negative repayment amounts.
        Error Handling: The test_lend_invalid_loan_amount currently asserts a ValueError. I took an easy way out here.
    TODO WHat if I delete that custimer during loan creating? Hmm may be considered an edge case but the tests can use Mocking and Patchiung to handle this scenario for me, thus separating customer creation and loan creation and processing.
    """

    def setUp(self):
        self.bank = NumiBank()
        self.customer = self.bank.create_customer('Muniu Kariuki')

    def test_create_customer(self):
        """
        Test that creating a new customer works successfully.
        """
        initial_customer_count = len(self.bank.customers)

        customer = self.bank.create_customer(customer_name := "John Doe")

        self.assertIsInstance(customer, Customer)
        self.assertIsInstance(customer.id, str)
        self.assertIsInstance(uuid.UUID(customer.id, version=4), uuid.UUID)
        self.assertEqual(customer.name, customer_name)
        self.assertEqual(self.bank.customers[customer.id], customer)
        self.assertEqual(len(self.bank.customers), initial_customer_count + 1)

    def test_create_loan(self):
        """
        Test that granting a loan to a customer works successfully.
        """
        initial_loan_count = len(self.bank.loans)
        amount = constants.MINIMUM_LOAN_AMOUNT
        interest_rate = constants.DEFAULT_INTEREST_RATE

        loan = self.bank.lend(
            self.customer.id, amount, interest_rate
        )

        self.assertEqual(loan.customer, self.customer)
        self.assertEqual(loan.amount, amount)
        self.assertEqual(loan.interest_rate, interest_rate)
        self.assertEqual(self.bank.loans[self.customer.id], loan)
        self.assertEqual(len(self.bank.loans), initial_loan_count + 1)

    def test_lend_customer_not_found(self):
        """
        Test that lending to a non-existent customer raises a CustomerNotFoundError.
        """
        initial_loan_count = len(self.bank.loans)
        amount = constants.MINIMUM_LOAN_AMOUNT
        invalid_customer_id = 'invalid id'

        with self.assertRaises(CustomerNotFoundError) as e:
            self.bank.lend(invalid_customer_id, amount)
        self.assertEqual(
            str(e.exception),
            f"CustomerNotFoundError: Customer with ID {invalid_customer_id} does not exist"
        )
        self.assertEqual(
            e.exception.message,
            f"Customer with ID {invalid_customer_id} does not exist"
        )
        self.assertEqual(len(self.bank.loans), initial_loan_count)

    def test_init_loan_with_invalid_customer_object(self):
        amount = constants.MINIMUM_LOAN_AMOUNT
        interest_rate = constants.DEFAULT_INTEREST_RATE

        with self.assertRaises(NumiBankError) as e:
            Loan('invalid customer object', amount, interest_rate)
        self.assertEqual(e.exception.message, "Invalid customer object")

    def test_init_loan_with_invalid_amount(self):
        amount = Decimal(-1)
        interest_rate = constants.DEFAULT_INTEREST_RATE

        with self.assertRaises(InvalidLoanAmountError) as e:
            Loan(self.customer, amount, interest_rate)
        self.assertEqual(
            e.exception.message,
            f"Loan amount must be between {constants.MINIMUM_LOAN_AMOUNT} and {constants.MAXIMUM_LOAN_AMOUNT}"
        )

    def test_lend_customer_with_outstanding_loan(self):
        self.bank.lend(self.customer.id, constants.MINIMUM_LOAN_AMOUNT)
        initial_loan_count = len(self.bank.loans)

        with self.assertRaises(CustomerHasOutstandingLoanError) as e:
            self.bank.lend(self.customer.id, constants.MINIMUM_LOAN_AMOUNT)
        self.assertEqual(
            e.exception.message,
            f"Customer with ID {self.customer.id} already has an outstanding loan"
        )
        self.assertEqual(len(self.bank.loans), initial_loan_count)

    def test_lend_invalid_interest_rate(self):
        initial_loan_count = len(self.bank.loans)
        invalid_interest_rates = [
            Decimal(-0.01),
            constants.MINIMUM_INTEREST_RATE - Decimal(0.01),
            constants.MAXIMUM_INTEREST_RATE + Decimal(0.01),
        ]

        for invalid_rate in invalid_interest_rates:
            with self.assertRaises(InvalidInterestRateError) as e:
                self.bank.lend(
                    self.customer.id,
                    constants.MINIMUM_LOAN_AMOUNT,
                    invalid_rate,
                )
            self.assertEqual(
                e.exception.message,
                f"Interest rate must be between {constants.MINIMUM_INTEREST_RATE} "
                f"and {constants.MAXIMUM_INTEREST_RATE}"
            )
            self.assertEqual(len(self.bank.loans), initial_loan_count)

    def test_lend_invalid_loan_amount(self):
        """
        Test if InvalidLoanAmountError is raised when the loan amount is invalid (negative amounts, amounts not within range).
        """
        initial_loan_count = len(self.bank.loans)
        interest_rate = constants.DEFAULT_INTEREST_RATE
        invalid_loan_amounts = [
            Decimal(-1),
            Decimal(0),
            Decimal(constants.MINIMUM_LOAN_AMOUNT - 1),
            Decimal(constants.MAXIMUM_LOAN_AMOUNT + 1),
        ]

        for invalid_amount in invalid_loan_amounts:
            with self.assertRaises(InvalidLoanAmountError) as e:
                self.bank.lend(
                    self.customer.id,
                    invalid_amount,
                    interest_rate,
                )
            self.assertEqual(
                e.exception.message,
                f"Loan amount must be between {constants.MINIMUM_LOAN_AMOUNT} "
                f"and {constants.MAXIMUM_LOAN_AMOUNT}"
            )
            self.assertEqual(len(self.bank.loans), initial_loan_count)

    def test_loan_repayment(self):
        """
        Test that processing a loan repayment works successfully.
        """
        amount = constants.MAXIMUM_LOAN_AMOUNT
        interest_rate = constants.MAXIMUM_INTEREST_RATE
        loan = self.bank.lend(self.customer.id, amount, interest_rate)
        repayment_amount = Decimal(2)

        self.bank.repay(self.customer.id, repayment_amount)

        self.assertEqual(len(loan.repayments), 1)
        self.assertEqual(loan.repayments[0], repayment_amount)
        self.assertEqual(loan.outstanding_debt, amount * (Decimal(1) + interest_rate) - repayment_amount)
        self.assertEqual(loan.total_repayments, repayment_amount)

    def test_loan_repayment_for_customer_without_loan(self):
        amount = constants.MAXIMUM_LOAN_AMOUNT
        interest_rate = constants.MAXIMUM_INTEREST_RATE
        repayment_amount = Decimal(2)

        with self.assertRaises(LoanNotFoundError) as e:
            self.bank.repay(self.customer.id, repayment_amount)
        self.assertEqual(
            e.exception.message,
            f"Customer with ID {self.customer.id} does not have an outstanding loan"
        )

    def test_loan_repayment_validation(self):
        amount = constants.MAXIMUM_LOAN_AMOUNT
        interest_rate = constants.MAXIMUM_INTEREST_RATE
        loan = self.bank.lend(self.customer.id, amount, interest_rate)
        scenarios = [
            {
                'invalid_repayment_amount': Decimal(-1),
                'error_message': "Amount must be positive"
            },
            {
                'invalid_repayment_amount': Decimal(0),
                'error_message': "Amount must be positive"
            },
            {
                'invalid_repayment_amount': Decimal(loan.outstanding_debt + 1),
                'error_message': "Amount exceeds outstanding debt"
            },
        ]

        for scenario in scenarios:
            with self.assertRaises(InvalidLoanRepaymentAmountError) as e:
                self.bank.repay(self.customer.id, scenario['invalid_repayment_amount'])

            self.assertEqual(
                e.exception.message,
                scenario['error_message']
            )

    def test_get_customer_info(self):
        scenarios = [
            {
                'customer': self.customer,
                'loan': self.bank.lend(self.customer.id, constants.MINIMUM_LOAN_AMOUNT)
            },
            {
                'customer': self.bank.create_customer("John Doe"),
                'loan': None
            },
        ]

        for scenario in scenarios:
            customer_info = self.bank.get_customer_info(scenario['customer'].id)

            self.assertEqual(customer_info['customer'], scenario['customer'])
            self.assertEqual(customer_info['loan'], scenario['loan'])

    def test_get_customer_info_for_nonexistent_customer(self):
        self.assertIsNone(self.bank.get_customer_info('nonexistent id'))
