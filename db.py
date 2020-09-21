"""
Модуль для работы с базой данных SQLite
"""

import sqlite3
from sqlite3 import Error
import random


def connection_to_database(file_name):
    """
    Соединение с базой данных библиотеки
    :return: sqlite3.connect
    """
    try:
        return sqlite3.connect(file_name)
    except Error:
        print(Error)


def create_db(database):
    """
    Создание базы данных библиотеки
    :param database: база данных
    """
    cursor = database.cursor()
    cursor.execute("""
        CREATE TABLE books(
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL, 
        author text NOT NULL, 
        genre text NOT NULL,
        year integer,
        amount integer
        )""")
    database.commit()


# def insert_to_db(database):
#     """
#     Добавление данных в библиотеку
#     :param database: база данных
#     """
#     cursor = database.cursor()
#     cursor.execute("INSERT INTO books (name, author, genre, year, amount) "
#                    "VALUES('Война и мир', 'Лев Толстой', 'Роман', 1865, 3)")
#     database.commit()


# def read_all_from_db(database):
#     """
#     Получение всех данных из базы
#     :param database: база данных
#     :return: список кортежей записей
#     """
#     cursor = database.cursor()
#     cursor.execute("""
#         SELECT *
#         FROM books
#         ORDER BY id
#         """)
#     data = cursor.fetchall()
#     return data


def read_author_from_db(database):
    """
    Чтение данных из колонки 'author'
    :param database: база данных
    :return: список авторов
    """
    cursor = database.cursor()
    cursor.execute("""
        SELECT author
        FROM books
        """)
    data = cursor.fetchall()
    return data


def read_genre_from_db(database):
    """
    Чтение данных из колонки 'genre'
    :param database: база данных
    :return: список жанров
    """
    cursor = database.cursor()
    cursor.execute("""
        SELECT genre
        FROM books
        """)
    data = cursor.fetchall()
    return data


def read_year_from_db(database):
    """
    Чтение данных из колонки 'year'
    :param database: база данных
    :return: список годов написания всех книг
    """
    cursor = database.cursor()
    cursor.execute("""
        SELECT year 
        FROM books 
        """)
    data = cursor.fetchall()
    return data


def insert_new_record(database, name, author, genre, year):
    """
    Добавление новой записи по введенным данным
    :param database: база данных
    :param name: Название книги
    :param author: Автор
    :param genre: Жанр
    :param year: Год
    """
    cursor = database.cursor()
    entities = (name, author, genre, year, random.randint(0, 5))
    cursor.execute(
        '''INSERT INTO books(name, author, genre, year, amount) 
        VALUES(?, ?, ?, ?, ?)
        ''', entities)
    database.commit()


def delete_record(database, record):
    """
    Удаление записи из базы данных
    :param database: база данных
    :param record: id записи из Combobox
    """
    cursor = database.cursor()
    cursor.execute("""
        DELETE FROM books WHERE id=?""", (record,))
    database.commit()


def choose_record(database, record):
    """
    Выбор записи из библиотеки по ее id
    :param database: база данных
    :param record: id записи
    :return: список (из 1 кортежа) выбранной записи
    """
    cursor = database.cursor()
    cursor.execute("""
        SELECT * FROM books WHERE id=?""", (record,))
    data = cursor.fetchall()
    return data


def update_record(database, id_rec, name_rec, author_rec, genre_rec, year_rec):
    """
    Обновление данных выбранной записи в библиотеке
    :param database: база данных
    :param id_rec: id выбранной записи
    :param name_rec: название книги
    :param author_rec: автор
    :param genre_rec: жанр
    :param year_rec: год
    """
    cursor = database.cursor()
    cursor.execute(
        '''UPDATE books SET name=?, author=?, genre=?, year=? 
        WHERE id=?''', (name_rec, author_rec, genre_rec, year_rec, id_rec))
    database.commit()


def select_record_by_filter(database, name_rec, author_rec, genre_rec):
    cursor = database.cursor()
    cursor.execute("""
        SELECT * FROM books 
        WHERE name=? OR author=? OR genre=?""", (name_rec, author_rec, genre_rec))
    data = cursor.fetchall()
    return data


if __name__ == "__main__":
    db = connection_to_database()
    #create_db(db)
    #insert_to_db(db)
    for item in read_all_from_db(db):
        print(item[3], item)
    print(read_all_from_db(db))
    print(set(read_year_from_db(db)))
    db.close()