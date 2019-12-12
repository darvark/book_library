import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Creates db file if not exists, if exists then open connection to db
    and return connection obejct
    :param db_file:
    :return:
    """

    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return connection


def close_connection(connection):
    """
    Closing connection to database
    :param:
    :return:
    """

    if connection:
        connection.close()


def __read_query_file(file_name):
    """
    Reads sql file and return string with content
    :param file_name:
    :return: string
    """

    with open(file_name, "r") as f:
        return f.read()


def __create_tables__(connection, sql_file):
    """
    Create tables from .sql file
    :param connection:
    :param sql_file:
    :return:
    """

    create_query = __read_query_file(sql_file)

    try:
        c = connection.cursor()
        sqlite3.complete_statement(create_query)
        c.executescript(create_query)
    except Error as e:
        print(e)


def __execute_insert_query(connection, query, query_data):
    """
    Execute sql query
    :param connection:
    :param query:
    :param query_data:
    :return: last row id
    """

    try:
        cur = connection.cursor()
        with connection:
            cur.execute(query, query_data)
        return cur.lastrowid
    except Error as e:
        print(e)


def __execute_search_query(connection, query, query_data):
    """
    Execute sql query
    :param connection:
    :param query:
    :param query_data:
    :return: rows
    """

    try:
        cur = connection.cursor()
        with connection:
            cur.execute(query, query_data)
        return cur.fetchall()
    except Error as e:
        print(e)


def insert_data_book(connection, query_data):
    """
    Insert data to book table
    :param connection:
    :param query:
    :return: last row id
    """

    query = """INSERT INTO ksiazka(tytul, autor, wydawca, wlasciciel, isbn, stron, opis) VALUES (?,?,?,?,?,?,?)"""

    return __execute_insert_query(connection, query, query_data)


def create_book_order(connection, query_data):
    """
    Insert data to order table
    :param connection:
    :param query:
    :return: last row id
    """

    query = """INSERT INTO zamowienie(id_ksiazka, id_czytelnik, data_zamowienia, data_wypozyczenia, data_zwrotu, id_ksiazka, id_czytelnik) VALUES (?,?,?,?,?,?,?)"""

    return __execute_insert_query(connection, query, query_data)


def add_user(connection, query_data):
    """
    Insert data to user table
    :param connection:
    :param query:
    :return: last row id
    """

    query = """INSERT INTO czytelnik(imie, nazwisko, telefon, mail) VALUES (?,?,?,?)"""

    return __execute_insert_query(connection, query, query_data)


def find_book_title(connection, query_data):
    """
    Finds book in a database
    :param connection:
    :param query_data:
    :return:
    """

    query = """SELECT * FROM ksiazka WHERE  title=?"""
    return __execute_search_query(connection, query, query_data)


def find_book_author(connection, query_data):
    """
    Finds book in a database
    :param connection:
    :param query_data:
    :return:
    """

    query = """SELECT * FROM ksiazka WHERE  autor=?"""
    return __execute_search_query(connection, query, query_data)


def find_book_owner(connection, query_data):
    """
    Finds book in a database
    :param connection:
    :param query_data:
    :return:
    """

    query = """SELECT * FROM ksiazka WHERE  wlasciciel = ?"""
    return __execute_search_query(connection, query, query_data)


def find_user_history(connection, query_data):
    """
    """

    query = """SELECT * FROM czytelnik WHERE * """
    return __execute_search_query(connection, query, query_data)


def show_rentals(connection, query_data):
    """
    """

    query = """SELECT * FROM czytelnik WHERE * """
    return __execute_search_query(connection, query, query_data)


def add_user(connection, query_data):
    """
    """

    query = """SELECT * FROM czytelnik WHERE * """
    return __execute_insert_query(connection, query, query_data)

def add_book(connection, query_data):
    """
    """

    query = """SELECT * FROM czytelnik WHERE * """
    return __execute_insert_query(connection, query, query_data)


if __name__ == "__main__":
    pass
