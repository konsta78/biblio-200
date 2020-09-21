"""
Модуль для работы с базой данных
"""

import sqlite3


class DataBase:
    def __init__(self, database):
        self.database = database
        database_connect = sqlite3.connect(self.database)
        self.cursor = database_connect.cursor()

    def read_all_from_db(self):
        """
        Получение всех данных из базы
        :param database: база данных
        :return: список кортежей записей
        """
        self.cursor.execute("""
            SELECT * 
            FROM books 
            ORDER BY id
            """)
        data = self.cursor.fetchall()
        return data

    def read_from_database_by_filter(self, filter_type):
        """
        Чтение данных из колонки 'author', 'genre' или 'year'
        :filter_type: параметр фильтрации (по автору, по жанру или по году)
        :return: перечень записей по фильтру
        """
        a = filter_type
        self.cursor.execute(f"""
                SELECT DISTINCT {a}
                FROM books
                """)
        data = self.cursor.fetchall()
        return data

    def database_close(self):
        self.cursor.close()


if __name__ == "__main__":
    db = DataBase("library_db.sqlite3")

    for item in db.read_from_database_by_filter('author'):
        print(item[0])

    #print(db.read_from_database_by_filter())
    db.database_close()