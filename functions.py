"""
Модуль с основными функциями для работы с библиотекой
"""

from tkinter import filedialog as fd
from database import DataBase
from graphic import Root, PopUpWindow
import driver
import os

# TODO: 1. При создании новой базы данных необходимо сначала закрыть существующую базу при ее наличии
#       2. При создании новой базы автоматически добавлять расширение 'sqlite3' (не работает в Windows)
#       3. В функции load_database и create_new_database задвоение глобальной переменной 'db' - плохо


def create_main_window():
    """
    Создание основного окна программы
    """
    global root
    root = Root()
    root.mainloop()


def load_database():
    """
    Загрузка базы данных из файла '.sqlite3' - кнопка 'Загрузить'
    """
    file_name = fd.askopenfilename(filetypes=(("Database", "*.sqlite3"),))
    global db
    if file_name:
        db = DataBase(file_name)
        root.update_main_text_field("База успешно загружена!")


def save_database():
    """
    Сохранение базы данных в файл '.json' - кнопка 'Сохранить'
    """
    file_name = fd.asksaveasfilename(filetypes=(("Json files", '*.json'), ('Text files', '*.txt')),
                                     defaultextension="*.*")
    if file_name:
        file, ext = os.path.splitext(file_name)
        if ext == '.txt':
            my_driver = driver.TextDriver(file_name)
        else:
            my_driver = driver.JsonDriver(file_name)

        driver.SaveToFile(db, driver=my_driver).save()
        root.update_main_text_field(f"База успешно сохранена в файле {file_name}!")


def create_new_database():
    """
    Создание новой базы данных - кнопка 'Создать'
    """
    file_name = fd.asksaveasfilename(filetypes=(("Database", "*.sqlite3"),))
    global db
    if file_name:
        db = DataBase(file_name)
        db.create_database()
        root.update_main_text_field("База успешно создана!")


def show_welcome():
    """
    Отображение общей информации о библиотеке - кнопка 'В начало'
    """
    root.main_text_field_on()
    root.main_text_field_insert(f'В нашей библиотеке: {len(db.read_all_from_db())} различных книг\n')
    root.main_text_field_insert(f'Авторов в библиотеке: {len(db.read_from_database_by_filter("author"))}\n')
    root.main_text_field_insert(f'Жанров в библиотеке: {len(db.read_from_database_by_filter("genre"))}\n')
    root.main_text_field_off()


def show_catalog(filter_records=None):
    """
    Отображение каталога записей в библиотеке - кнопка 'Каталог'
    """
    root.main_text_field_on()
    if filter_records is None:
        records = db.read_all_from_db()
    else:
        records = filter_records

    for item in records:
        root.main_text_field_insert(f'id{item[0]} - "{item[1]}", {item[2]}, {item[3]}, {item[4]} год, {item[5]} шт.\n')
    root.main_text_field_off()


def new_record():
    """
    Отображение доп. окна для внесения новой записи в библиотеку - ннопка 'Добавить'
    """
    PopUpWindow(root, 500, 220).pop_up_add_record(db)


def delete_record():
    """
    Отображение доп. окна для удаления записи из библиотеки - ннопка 'Удалить'
    """
    PopUpWindow(root, 500, 140).pop_up_delete_record(db)


def edit_record():
    """
    Отображение доп. окна для редактирования существующей записи в библиотеке - кнопка 'Редактировать'
    """
    PopUpWindow(root, 520, 280).pop_up_update_record(db)


def find_record():
    """
    Отображение доп. окна для поиска записей в библиотеке - кнопка "Поиск"
    """
    PopUpWindow(root, 480, 200).pop_up_find_record(root, db)


def biblio_close(db=None):
    """
    Закрытие основного окна программы
    """
    if db is not None:
        db.cursor.close()
    root.destroy()

