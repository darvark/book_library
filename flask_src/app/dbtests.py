import os
import sqlite3
import unittest
from sqlite3 import Error

import db_handler as dbh


class TestDatabaseHandler(unittest.TestCase):

    # def setUp(self):
    #     os.remove('test.db')

    def test01_create_table(self):
        """
        Checks only if we are creating required amount of tables in database
        """

        db = sqlite3.connect("test.db")
        dbh.__create_tables__(db, "baza.sql")
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            table_name = table_name[0]

        self.assertEqual(len(tables), 4)

    def test02_add_book(self):
        """
        Test module to add new book to database
        """

        db = sqlite3.connect("test.db")

        data = (
            "Wladca pierscieni",
            "J.R.R. Tolkien",
            "Muza",
            "Marcin Iwaniuk",
            8275462,
            430,
            "male slady uzytkowania",
        )

        id = dbh.insert_data_book(db, data)

        self.assertEqual(id, 1)


if __name__ == "__main__":
    if os.path.exists("test.db"):
        os.remove("test.db")
    unittest.main()
