import unittest
from decimal import Decimal
from numibank_exceptions import CustomerAlreadyExistsError, CustomerNotFoundError, InvalidLoanAmountError
from numibank import NumiBank

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

    def test_create_customer_success(self):
        """
        Test that creating a new customer works successfully.
        """
        customer_id = 1001
        name = "Muniu Kariuki"

        customer = self.bank.create_customer(customer_id, name)

        self.assertEqual(customer.customer_id, customer_id)
        self.assertEqual(customer.name, name)
        self.assertEqual(self.bank.customers[customer_id], customer)

    def test_create_customer_already_exists(self):
        """
        Test that creating a customer with an existing ID raises a CustomerAlreadyExistsError.
        """
        customer_id = 1001
        name = "Muniu Kariuki"

        self.bank.create_customer(customer_id, name)

        with self.assertRaises(CustomerAlreadyExistsError) as e:
            self.bank.create_customer(customer_id, "Muniu KK")

        self.assertEqual(
            str(e.exception), f"Customer with ID {customer_id} already exists"
        )

    def test_lend_success(self):
        """
        Test that granting a loan to a customer works successfully.
        """
        customer_id = 1001
        name = "Muniu Kariuki"
        amount = 20.0 #lend 20 
        interest_rate = 0.05 #at an interest rate of 5%
        customer = self.bank.create_customer(customer_id, name)
        loan = self.bank.lend(customer.customer_id, customer.name, amount, interest_rate)

        self.assertEqual(loan.customer_id, customer_id)
        self.assertEqual(loan.amount, amount)
        self.assertEqual(loan.interest_rate, interest_rate)
        self.assertEqual(self.bank.loans[customer_id], loan)

    def test_lend_customer_not_found(self):
        """
        Test that lending to a non-existent customer raises a CustomerNotFoundError.
        """
        customer_id = 1002
        name = "Muniu Kariuki"
        amount = 20.0
        interest_rate = 0.05
        # customer = self.bank.create_customer(customer_id, name)
        with self.assertRaises(CustomerNotFoundError) as e:
            self.bank.lend(customer_id, name, amount, interest_rate)

        self.assertEqual(
            str(e.exception), f"Customer with ID {customer_id} does not exist"
        )

        
    def test_lend_invalid_loan_amount(self):
        """
        Test if InvalidLoanAmountError is raised when the loan amount is invalid (negative amounts, amounts not within range).
        """
        customer_id = 1001
        name = "Muniu Kariuki"
        amount = 5.0  # Below minimum loan amount
        interest_rate = 0.2
        customer = self.bank.create_customer(customer_id, name)
        with self.assertRaises(ValueError): #TODO As lend returns two types of Exceptions, asserting ValueError to provision for both. Given more time I'd have expanded these errors into codes and handled them here better.
            self.bank.lend(
                customer.customer_id,
                customer.name,
                Decimal(amount),
                Decimal(interest_rate),
            )

    def test_repay_success(self):
        """
        Test that processing a loan repayment works successfully.
        """
        customer_id = 1001
        name = "Muniu Kariuki"
        amount = 10.0
        interest_rate = 0.05

        customer = self.bank.create_customer(customer_id, name)
        loan = self.bank.lend(customer.customer_id, customer.name, amount, interest_rate)
        repayment_amount = 2.0

        self.bank.repay(customer_id, repayment_amount)

        self.assertEqual(len(loan.repayments), 1)
        self.assertEqual(loan.repayments[0], repayment_amount)


    def test_loan_repayment_scenario(self):
        """
        Test a loan repayment scenario with partial payment and exceeding payment.

        This test follows the given scenario:
        - Apio borrows $20 at 10% interest.
        - Apio repays $10.
        - Verifies remaining debt and repayments.
        - Attempts to repay more than outstanding amount, raising an error.
        """

        customer_id = 192
        name = "Apio"
        loan_amount = 20.0
        interest_rate = 0.1
        repayment_amount = 10.0

        customer = self.bank.create_customer(customer_id, name)
        self.bank.lend(customer.customer_id, customer.name, loan_amount, interest_rate)

        # Partial repayment
        self.bank.repay(customer_id, repayment_amount)
        
        # We want to know what the outstanding amount is i.e lend $20 at an interest of 10% = $22 as total outstanding
        # Then repay $10 leaving the outstanding at $12
        # Then attempt to repay $15, which should throw an error as it is above the due

        # Verify loan details
        loan = self.bank.loans[customer_id]
        #print ("Outstanding debt: ")
        #print (loan.outstanding_debt)
        #print ("Total Repayments: ")
        #print (loan.repayments)
        self.assertEqual(loan.outstanding_debt, 12.0, "Outstanding debt after partial payment")
        self.assertEqual(loan.repayments, [10.0], "Repayment history should be updated")

        # Attempt to overpay
        with self.assertRaises(InvalidLoanAmountError):
            self.bank.repay(customer_id, 15.0)


if __name__ == "__main__":
    unittest.main()