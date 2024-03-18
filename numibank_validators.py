class Validator:
    """ "
    Validator class to hold common utility functions that are reused across other modules in this project.
    """

    @staticmethod
    def is_positive(value):
        """
        Utility function to check that a value is a positive float.
        """
        if value <= 0:
            raise ValueError(
                f"{value} is not a valid amount. Only positive values allowed."
            )
        return True

    @staticmethod
    def is_within_range(value, lower_bound, upper_bound):
        """ "
        Utility function to check that a value passed is within the range defined by the user.
        """
        if value < lower_bound or value > upper_bound:
            raise ValueError(
                f"{value} must be between {lower_bound} and {upper_bound}."
            )
        return True

    @staticmethod
    def is_valid_interest_rate(value):
        """
        We use a Decimal to define interest and this function checks that the values are between 0.0 and 1.0
        """
        return Validator.is_within_range(value, 0.0, 1.0)

    @staticmethod
    def is_valid_loan_amount(value, min_loan=10, max_loan=100):
        """
        Validates if the provided value is a valid loan amount within the defined range.

        is_positive ensures the loan amount is positive, and not a negative value.
        is_within_range checks if the value falls within the specified range, borrowing from the above function.
        Finally, this function combines these checks and allows for customizable loan limits.
        TODO Externalise the values so user can define them.
        """
        Validator.is_positive(value)
        Validator.is_within_range(value, min_loan, max_loan)
        return True
    