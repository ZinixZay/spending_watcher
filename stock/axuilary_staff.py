from database_commands import add_expense, add_income, count_incomes, get_spend_for_stats, count_expenses
from logical_part import select_expense_class
from config import Data, colors, imgs
from random import choice
from PyQt5.QtGui import QColor


class SpendRecord:
    """
    Class of an expense record
    """
    def __init__(self, value: int, description: str):
        self.value = value
        self.description = description

    def submit_record(self) -> None:
        """
        Adds an expense to database
        :return: None
        """
        add_expense(value=self.value, description=self.description, category=select_expense_class(self.description))


class IncomeRecord:
    """
    Class of an income record
    """
    def __init__(self, value: int):
        self.value = value

    def submit_record(self) -> None:
        """
        Adds an income to database
        :return: None
        """
        add_income(value=self.value)


def get_current_amount() -> int:
    """
    Counts money available
    :return: money user has
    """
    result = count_incomes() - count_expenses()
    return result


def generate_chart_data() -> list:
    """
    Reduces data to stock sample for chart work
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
        avail_colors = colors.copy()
        color = choice(avail_colors)
        del avail_colors[avail_colors.index(color)]
        chart_data.append(Data(category, amount, QColor(color), QColor(color)))
    return chart_data


def choose_photo(val: int) -> str:
    """
    Finds suitable photo for current amount
    :param val: current balance
    :return: path to a photo
    """
    if val == 0:
        path = f'img/{imgs[4]}'
    elif val < 100:
        path = f'img/{imgs[1]}'
    elif val < 500:
        path = f'img/{imgs[2]}'
    elif val < 5000:
        path = f'img/{imgs[3]}'
    elif val < 15000:
        path = f'img/{imgs[5]}'
    elif val < 100000:
        path = f'img/{imgs[0]}'
    else:
        path = f'img/{imgs[-1]}'
    return path
