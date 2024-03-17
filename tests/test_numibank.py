import unittest
from numibank_exceptions import CustomerAlreadyExistsError, CustomerNotFoundError, InvalidLoanAmountError
from numibank import NumiBank

class TestNumiBank(unittest.TestCase):
    def setUp(self):
            self.bank = NumiBank()

    def test_create_customer(self):
            customer_id = self.bank.create_customer(1001, "Jomo Kenyatta").id
            self.assertEqual(customer_id, 1001)

            # Test duplicate customer creation
            with self.assertRaises(CustomerAlreadyExistsError):
                self.bank.create_customer(1001, "Jonathan Toroitich")

    def test_lend_loan(self):
            customer_id = self.bank.create_customer(2001, "Jonathan Toroitich").id
            loan = self.bank.lend(customer_id, "Jonathan Toroitich", 100.0, 0.05)

            self.assertIsNotNone(loan)
            self.assertEqual(loan.customer_id, customer_id)
            self.assertEqual(loan.amount, 100.0)
            self.assertEqual(loan.interest_rate, 0.05)
            self.assertEqual(loan.repayments, [])

            # Test lending to non-existent customer
            with self.assertRaises(CustomerNotFoundError):
                self.bank.lend(9999, "Non-Existent", 50.0, 0.1)

            # Test invalid loan amount
            with self.assertRaises(InvalidLoanAmountError):
                self.bank.lend(customer_id, "Jonathan Toroitich", -100.0, 0.05)

    def test_repay_loan(self):
            customer_id = self.bank.create_customer(3001, "Emilio Mwai").id
            self.bank.lend(customer_id, "Emilio Mwai", 50.0, 0.1)

            self.bank.repay(customer_id, 10.0)
            loan = self.bank.loans[customer_id]
            self.assertEqual(loan.outstanding_debt, 450.0)

            # Test repayment to non-existent customer
            with self.assertRaises(CustomerNotFoundError):
                self.bank.repay(9999, 50.0)

            # Test negative repayment amount
            with self.assertRaises(
                ValueError
            ):  # Maybe I should put a custom exception here
                self.bank.repay(customer_id, -25.0)


if __name__ == "__main__":
    unittest.main()
