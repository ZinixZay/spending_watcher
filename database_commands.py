import sqlite3
from sqlite3 import Connection
from typing import NoReturn, Type
from datetime import datetime


def connect_to_database() -> Type:
    """
    connects to a database
    :return: NoReturn
    """
    con = sqlite3.connect('database/expenses.db')
    cur = con.cursor()
    return con, cur


def disconnect_from_database(con: Type) -> NoReturn:
    """
    disconnects from database
    :return: NoReturn
    """
    con.commit()
    con.close()


def add_record_to_a_database(value: int, description: str) -> NoReturn:
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

