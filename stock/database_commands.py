import sqlite3
from typing import Type
from datetime import datetime


def connect_to_database() -> Type:
    """
    Connects to a database
    :return: connection and a cursor for database
    """
    con = sqlite3.connect('database/expenses.db')
    cur = con.cursor()
    return con, cur


def disconnect_from_database(con: Type) -> None:
    """
    Disconnects from database
    :return: None
    """
    con.commit()
    con.close()


def drop_database() -> None:
    """
    Deletes all inforamtion from database
    :return: None
    """
    con, cur = connect_to_database()
    cur.execute('DELETE FROM expenses')
    cur.execute('DELETE FROM incomes')
    cur.execute('DELETE FROM classfied_expenses')
    disconnect_from_database(con)


def add_expense(value: int, description: str, category: str) -> None:
    """
    Adds a money spend record to a database
    :param value: amount of spended money
    :param description: what was the money spent on
    :param category: category of an expense
    :return: None
    """
    con, cur = connect_to_database()
    cur.execute(f'INSERT INTO expenses (date, description, value)'
                f'VALUES ("{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}", "{description}", {value})')
    cur.execute(f'INSERT INTO classfied_expenses (date, category)'
                f'VALUES ("{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}", "{category}")')
    disconnect_from_database(con)


def add_income(value: int) -> None:
    """
    Adds a money income record to a database
    :param value: amount of income
    :param description: where were money got
    :return: None
    """
    con, cur = connect_to_database()
    cur.execute(f'INSERT INTO incomes (date, value)'
                f'VALUES ("{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}", {value})')
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


def get_spend_for_stats() -> list:
    """
    Compare database tables and return extense with description replaced as category
    :return: list with all reworked extenses
    """
    con, cur = connect_to_database()
    cur.execute(f'SELECT date, category FROM classfied_expenses')
    with_categories = list()
    spends = list()
    for i in cur.fetchall():
        with_categories.append([i[0], i[1]])
    for i in with_categories:
        cur.execute(f"SELECT value FROM expenses WHERE date='{i[0]}'")
        for j in cur.fetchall():
            spend = [i[1], j[0]]
            spends.append(spend)
    disconnect_from_database(con)
    return spends


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


def get_history() -> tuple:
    """
    Gets all expenses
    :return: None
    """
    con, cur = connect_to_database()
    cur.execute(f'SELECT * FROM expenses')
    result = cur.fetchall()
    return result
