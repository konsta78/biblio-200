from tkinter import filedialog as fd
from database import DataBase
from graphic import Root, PopUpWindow


def create_main_window():
    global root
    root = Root()
    root.mainloop()


def load_database():
    file_name = fd.askopenfilename(filetypes=(("Database", "*.sqlite3"),))
    global db
    if file_name:
        db = DataBase(file_name)
        root.update_after_load_database()


def show_welcome():
    """
    Отображение общей информации о библиотеке - кнопка 'В начало'
    """
    root.main_text_field_on()
    root.main_text_field_insert(f'В нашей библиотеке: {len(db.read_all_from_db())} различных книг\n')
    root.main_text_field_insert(f'Авторов в библиотеке: {len(db.read_from_database_by_filter("author"))}\n')
    root.main_text_field_insert(f'Жанров в библиотеке: {len(db.read_from_database_by_filter("genre"))}\n')
    root.main_text_field_off()


def show_catalog():
    """
    Отображение каталога записей в библиотеке - кнопка 'Каталог'
    """
    root.main_text_field_on()
    for item in db.read_all_from_db():
        root.main_text_field_insert(f'id{item[0]} - "{item[1]}", {item[2]}, {item[3]}, {item[4]} год, {item[5]} шт.\n')
    root.main_text_field_off()


def new_record():
    """
    Отображение доп. окна для внесения новой записи в библиотеку -
    ннопка 'Добавить'
    """

    def save_nr():
        """
        Закрытие доп. окна и внесение новой записи в базу данных
        """
        db.add_new_record(db, new_name, new_author, new_genre, new_year, 5)
        nr_window.destroy()
        show_welcome()

    nr_window = PopUpWindow(root, 500, 220)
    new_name, new_author, new_genre, new_year = nr_window.pop_up_add_record()


def biblio_close():
    """
    Закрытие основного окна программы
    """
    try:
        if db:
            db.cursor.close()
    finally:
        root.destroy()

