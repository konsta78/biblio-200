"""
Модуль для работы с базой данных
"""

import sqlite3


class DataBase:
    def __init__(self, database):
        self.database = database
        self.database_connect = sqlite3.connect(self.database)
        self.cursor = self.database_connect.cursor()

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

    def add_new_record(self, name, author, genre, year, amount):
        """
         Добавление новой записи по введенным данным
         :param name: Название книги
         :param author: Автор
         :param genre: Жанр
         :param year: Год издания
         :param amount: Кол-во экземпляров
         """
        entities = (name, author, genre, year, amount)
        self.cursor.execute(
            '''INSERT INTO books(name, author, genre, year, amount) 
            VALUES(?, ?, ?, ?, ?)
            ''', entities)
        self.database_connect.commit()

    def delete_from_database(self, record):
        """
        Удаление записи из базы данных
        :param record: id записи из Combobox
        """
        self.cursor.execute("""
            DELETE FROM books WHERE id=?""", (record,))
        self.database_connect.commit()

    def get_record(self, record):
        """
        Выбор записи из библиотеки по ее id
        :param record: id записи
        :return: список (из 1 кортежа) выбранной записи
        """
        self.cursor.execute("""
            SELECT * FROM books WHERE id=?""", (record,))
        data = self.cursor.fetchall()
        return data

    def update_record_in_database(self, id_rec, name_rec, author_rec, genre_rec, year_rec):
        """
        Редактирование выбранной записи в библиотеке
        :param id_rec: id выбранной записи
        :param name_rec: название книги
        :param author_rec: автор
        :param genre_rec: жанр
        :param year_rec: год
        """
        self.cursor.execute(
            '''UPDATE books SET name=?, author=?, genre=?, year=? 
            WHERE id=?''', (name_rec, author_rec, genre_rec, year_rec, id_rec))
        self.database_connect.commit()

    def database_close(self):
        self.cursor.close()


if __name__ == "__main__":
    db = DataBase("library_db.sqlite3")

    for item in db.read_from_database_by_filter('author'):
        print(item[0])

    print(db.read_from_database_by_filter('author'))
    db.database_close()