import constants
from numibank_exceptions import InvalidInterestRateError, InvalidLoanAmountError


class Validator:
    """
    Validator class to hold common utility functions that are reused across other modules in this project.
    """

    @staticmethod
    def is_positive(value):
        """
        Utility function to check that a value is a positive float.
        """
        return value > 0

    @staticmethod
    def is_within_range(value, lower_bound, upper_bound):
        """
        Utility function to check that a value passed is within the range defined by the user.
        """
        return lower_bound <= value <= upper_bound
