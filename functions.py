from tkinter import filedialog as fd
from database import DataBase


def load_database():
    file_name = fd.askopenfilename(filetypes=(("Database", "*.sqlite3"),))
    global db
    if file_name:
        db = DataBase(file_name)
        print("база открыта")
        # but_m0.configure(state='normal')
        # but_m1.configure(state='normal')
        # but_m2.configure(state='normal')
        # but_m3.configure(state='normal')
        # but_m4.configure(state='normal')
        # but_m5.configure(state='normal')
        # but_m6.configure(state='normal')
        # text1.configure(state='normal')
        # text1.delete(1.0, 'end')
        # text1.insert('end', "База успешно загружена!")
        # text1.configure(state='disabled')


def show_welcome():
    pass


def show_catalog():
    pass


def biblio_close():
    """
    Закрытие основного окна программы
    """
    if db:
        db.cursor.close()
        print("база закрыта")