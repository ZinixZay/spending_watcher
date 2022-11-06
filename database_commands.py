import sqlite3
from sqlite3 import Connection
from typing import NoReturn, Type
from datetime import datetime


def connect_to_database() -> Type:
    """
    Connects to a database
    :return: NoReturn
    """
    con = sqlite3.connect('database/expenses.db')
    cur = con.cursor()
    return con, cur


def disconnect_from_database(con: Type) -> NoReturn:
    """
    Disconnects from database
    :return: NoReturn
    """
    con.commit()
    con.close()


def add_expense_to_a_database(value: int, description: str) -> NoReturn:
    """
    Adds a money spend record to a database
    :param value: amount of spended money
    :param description: what was the money spent on
    :return: NoReturn
    """
    con, cur = connect_to_database()
    cur.execute(f'INSERT INTO expenses (date, description, value)'
                f'VALUES ("{datetime.now().strftime("%d-%m-%Y %H:%M")}", "{description}", {value})')
    disconnect_from_database(con)


def add_income_to_a_database(value: int, description: str) -> NoReturn:
    """
    Adds a money income record to a database
    :param value: amount of income
    :param description: where were money got
    :return: NoReturn
    """
    con, cur = connect_to_database()
    cur.execute(f'INSERT INTO incomes (date, description, value)'
                f'VALUES ("{datetime.now().strftime("%d-%m-%Y %H:%M")}", "{description}", {value})')
    disconnect_from_database(con)


def count_incomes(month: int = 0, year: int = 0) -> int:
    """
    Counts incomes per month or for all the time
    :param year: if given - filters counting for this year
    :param month: if given - filters counting for this month
    :return: result of counting
    """
    con, cur = connect_to_database()
    result = 0
    if month == year == 0:
        cur.execute(f'SELECT value FROM incomes')
        for value in cur.fetchall():
            result += value[0]
    disconnect_from_database(con)
    return result


def count_expenses(month: int = 0, year: int = 0) -> int:
    """
    Counts expenses per month or for all the time
    :param year: if given - filters counting for this year
    :param month: if given - filters counting for this month
    :return: result of counting
    """
    con, cur = connect_to_database()
    result = 0
    if month == year == 0:
        cur.execute(f'SELECT value FROM expenses')
        for value in cur.fetchall():
            result += value[0]
    disconnect_from_database(con)
    return result
