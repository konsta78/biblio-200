"""
Дан каталог книг. Реализуйте библиотеку для хранения данных книг
и поиску по каталогу. Каталог должен поддерживать возможность добавления
и удаления книг, редактирования информации о книге, а также обладать
персистентностью (т.е. сохранять библиотеку в внешнем файле и подгружать обратно).
Также необходимо оформить точку входа, поддерживать поиск по различным параметрам
и обеспечить интерфейс взаимодействия пользователя с библиотекой.
"""

from tkinter import *
from tkinter import filedialog as fd
from database import DataBase
from graphic import Root


WIDTH = 980
HEIGHT = 500


def create_main_window():
    """
    Создание основного окна программы
    """
    root = Root()
    return root


if __name__ == "__main__":
    db = None
    root = create_main_window()
    root.mainloop()
