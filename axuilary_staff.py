from database_commands import *
from logical_part import *


class SpendRecord:
    def __init__(self, value: int, description: str):
        self.value = value
        self.description = description

    def submit_record(self):
        add_expense(value=self.value, description=self.description, category=select_expense_class(self.description))


class IncomeRecord:
    def __init__(self, value: int, description: str):
        self.value = value
        self.description = description

    def submit_record(self):
        add_income(value=self.value, description=self.description)


# Error Classes


class AddRecordError(Exception):
    pass


class RecordValueError(AddRecordError):
    pass


class RecordDescriptionError(AddRecordError):
    pass


# Axuilary Functions

def get_current_amount() -> int:
    """
    Creates txt file with corrent amount of money
    :return: NoReturn
    """
    result = count_incomes() - count_expenses()
    return result