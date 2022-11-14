from database_commands import *
from logical_part import *
from config import Data


class SpendRecord:
    def __init__(self, value: int, description: str):
        self.value = value
        self.description = description

    def submit_record(self) -> NoReturn:
        """
        Adds an expense to database
        :return: NoReturn
        """
        add_expense(value=self.value, description=self.description, category=select_expense_class(self.description))


class IncomeRecord:
    def __init__(self, value: int, description: str):
        self.value = value
        self.description = description

    def submit_record(self) -> NoReturn:
        """
        Adds an income to database
        :return: NoReturn
        """
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


def generate_chart_data() -> list:
    """
    Reducts data to stock sample for chart work
    :return: data for chart
    """
    all_spends = get_spend_for_stats()
    spend_category_sum = dict()
    for spend in all_spends:
        if spend[0] not in spend_category_sum.keys():
            spend_category_sum[spend[0]] = spend[1]
        else:
            temp = spend_category_sum[spend[0]]
            temp += spend[1]
            spend_category_sum[spend[0]] = temp
    chart_data = list()
    for category, amount in spend_category_sum.items():
        chart_data.append(Data(category, amount, QtGui.QColor("#454895"), QtGui.QColor("#cfeef5")))
    return chart_data
