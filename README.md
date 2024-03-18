# NumiBank

This is a basic python based loan management system called NumiBank. The features are as follows:

* Lend, receive repayments and maintain an outstanding debt balance for multiple
customers
* Return a customer’s total repayments amount and outstanding debt
* Prevent customers from paying back more than they owe

## Design, Assumptions & Trade-Offs

### Key Design Decisions:
* Object-Oriented Approach: The code utilizes classes (Customer, Loan, NumiBank) to encapsulate data and functionalities, promoting maintainability.
* Error handling is implemented using custom exceptions and informative messages.
* Data validation is performed to ensure data integrity.

### Assumptions:
* Loan amounts and interest rates are represented by decimals.
* We assume simple interest. For compound interest, we'd need to modify the outstanding_debt calculation to account for interest on interest.
* The minimum and maximum loan amounts are configurable (currently set to defaults within the Validator class).

### Trade-offs:
* Conciseness over Comprehensiveness: The system prioritizes core functionalities over advanced features like loan terms or amortization schedules. This also applies to persistence and other requirements such as concurrency as per the instructions provided.
* Simplicity over User Interface: The code focuses on core logic, leaving out user interaction aspects, except from the provided unit tests.


### Room for Improvement:
* Completing Configurability: extend configurability for various validation parameters or incorporating configuration files for loan limits and interest rate ranges.
* Make use of sphinx or mkdocs to generate documentation based on the docstrings. 

## Project Structure


```python
numibank/
├── __init__.py  # Optional empty file to mark the directory as a package
├── models.py     # Contains Customer and Loan classes
├── numibank_validators.py    # Contains Validator class
├── numibank_exceptions.py    # Contains custom exceptions
├── numibank.py    # Contains NumiBank class
├── README.md     # Documentation for the project
├── requirements.txt    # Contains pip requirements for the project
└── tests/         # Folder for tests
    └── test_numibank.py # Tests for numibank.py

```

## Architecture

```bash
# TODO To complete the mermaid diagram
```

## Install Dependencies

```bash
pip install -r requirements.txt
```
### Optional formatting of the code (within the project directory)
```
black .
```
## Running Tests (without coverage)

```bash
python -m unittest tests/test_numibank.py  # Run from the project root
```
## Run tests (with coverage)
```bash
coverage run -m unittest tests/test_numibank.py # Run from the project root
coverage report #shows the coverage report as a percentage
```

## Final Thoughts

Thanks for the opportunity to complete the Numida Coding Assignment! I'm happy to present a complete application that implements all the core functionalities for customer creation, loan lending, repayments, and error handling. This demonstrates my understanding of the requirements and my ability to deliver a well-designed solution.

To ensure the reliability of the application, I've also developed a comprehensive test suite. It utilizes clear variable names, comments, and assertions for easy understanding and simplifies future maintenance.

While my recent focus has been on engineering and product management, my ability to quickly deliver a functional application and robust test suite demonstrates my adaptable skillset and continued passion for software development.

Overall, I'm confident that my combined experience in software engineering, organizational design and engineering management, and my eagerness to learn and adapt can significantly contribute to your team.




