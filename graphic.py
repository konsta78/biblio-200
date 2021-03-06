"""
Модуль для работы с графическим интерфейсом на основе Tkinter
"""

from tkinter import *
from tkinter.ttk import Combobox
import functions as f
import re

WIDTH = 980
HEIGHT = 500


class Root(Tk):
    """
    Основное окно программы
    """
    def __init__(self):
        super().__init__()
        self.title("Библиотека (реализована на классах)")
        root_x = self.winfo_screenwidth() // 2 - WIDTH // 2
        root_y = self.winfo_screenheight() // 2 - HEIGHT // 2
        self.resizable(width=False, height=False)
        self.geometry(f"{WIDTH}x{HEIGHT}+{root_x}+{root_y}")
        self.frame_top = Frame(relief=RAISED, borderwidth=2)
        self.frame_menu = Frame(relief=RAISED, borderwidth=2)
        self.frame_main = Frame(relief=RAISED, borderwidth=2)
        self.frame_top.pack(side=TOP, fill=X)
        self.frame_menu.pack(side=LEFT, fill=Y)
        self.frame_main.pack(side=LEFT, fill=BOTH)
        Label(self.frame_top, text="Добро пожаловать в библиотеку!",
                       font='arial 20 bold', pady=10).pack()
        self.but_start = Button(self.frame_menu, text="В начало", activeforeground="blue",
                        font='arial 16', width=12, command=f.show_welcome, state='disabled')
        self.but_start.pack()
        self.but_catalog = Button(self.frame_menu, text="Каталог", activeforeground="blue",
                        font='arial 16', width=12, command=f.show_catalog, state='disabled')
        self.but_catalog.pack()
        self.but_add = Button(self.frame_menu, text="Добавить", activeforeground="blue",
                        font='arial 16', width=12, command=f.new_record, state='disabled')
        self.but_add.pack()
        self.but_del = Button(self.frame_menu, text="Удалить", activeforeground="blue",
                        font='arial 16', width=12, command=f.delete_record, state='disabled')
        self.but_del.pack()
        self.but_edit = Button(self.frame_menu, text="Редактировать", activeforeground="blue",
                        font='arial 16', width=12, command=f.edit_record, state='disabled')
        self.but_edit.pack()
        self.but_find = Button(self.frame_menu, text="Поиск", activeforeground="blue",
                        font='arial 16', width=12, command=f.find_record, state='disabled')
        self.but_find.pack()
        self.but_save = Button(self.frame_menu, text="Сохранить", activeforeground="blue",
                        font='arial 16', width=12, command=f.save_database, state='disabled')
        self.but_save.pack()
        self.but_create = Button(self.frame_menu, text="Создать", command=f.create_new_database, activeforeground="blue",
                               font='arial 16', width=12, state='normal')
        self.but_create.pack()
        self.but_load = Button(self.frame_menu, text="Загрузить", command=f.load_database, activeforeground="blue",
                        font='arial 16', width=12, state='normal')
        self.but_load.pack()
        self.but_exit = Button(self.frame_menu, text="Выйти", command=f.biblio_close, activeforeground="blue",
                        font='arial 16', width=12).pack(side=BOTTOM)

        self.main_text_field = Text(self.frame_main, wrap=WORD, font="arial 14", bg="lightgray")
        self.main_text_field.pack()

    def main_text_field_on(self):
        """
        Очистка поля для отображения информации
        """
        self.main_text_field.configure(state='normal')
        self.main_text_field.delete(1.0, 'end')

    def main_text_field_off(self):
        """
        Запрет на редактирование поля для отображения информации
        """
        self.main_text_field.configure(state='disabled')

    def main_text_field_insert(self, data_text):
        """
        Отображение информации в основном поле
        """
        self.main_text_field.insert('end', data_text)

    def update_main_text_field(self, text):
        """
        Разблокировка кнопок работы с базой данных после ее загрузки или создания
        """
        self.but_start.configure(state='normal')
        self.but_catalog.configure(state='normal')
        self.but_add.configure(state='normal')
        self.but_del.configure(state='normal')
        self.but_edit.configure(state='normal')
        self.but_find.configure(state='normal')
        self.but_save.configure(state='normal')
        self.main_text_field_on()
        self.main_text_field_insert(text)
        self.main_text_field_off()


class PopUpWindow(Toplevel):
    """
    Всплывающие окна - общие параметры
    """
    def __init__(self, root, width, height):
        super().__init__()
        self.grab_set()
        nr_x = root.winfo_rootx() + root.winfo_reqwidth() // 2
        nr_y = root.winfo_rooty() + root.winfo_reqheight() // 2
        self.transient(root) # для Mac-OS
        self.geometry(f'{width}x{height}+{nr_x - width // 2}+{nr_y - height // 2}')
        self.lift() # для Mac-OS
        self.overrideredirect(True)

    def pop_up_add_record(self, db):
        """
        Окно - добавление новой записи
        """
        def on_click():
            db.add_new_record(new_name.get(), new_author.get(), new_genre.get(), new_year.get(), 5)
            self.destroy()
            f.show_catalog()

        Label(self, text="Добавление новой книги:",
                     font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W + E)
        Label(self, text="Название: ", font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        new_name = Entry(self, width=40)
        new_name.grid(row=1, column=1)
        Label(self, text="Автор: ", font='arial 14').grid(row=2, column=0, sticky=W, padx=10, pady=2)
        new_author = Entry(self, width=40)
        new_author.grid(row=2, column=1)
        Label(self, text="Жанр: ", font='arial 14').grid(row=3, column=0, sticky=W, padx=10, pady=2)
        new_genre = Entry(self, width=40)
        new_genre.grid(row=3, column=1)
        Label(self, text="Год создания: ", font='arial 14').grid(row=4, column=0, sticky=W, padx=10, pady=2)
        new_year = Entry(self, width=4)
        new_year.grid(row=4, column=1, sticky=W)
        Button(self, text="Сохранить", activeforeground="blue", command=on_click,
                      font='arial 16', width=10).grid(row=5, column=0, padx=10, pady=2)
        Button(self, text="Закрыть", activeforeground="blue", command=self.destroy,
                      font='arial 16', width=10).grid(row=5, column=1, sticky=E, pady=2)

    def pop_up_delete_record(self, db):
        """
        Окно - удаление записи
        """
        def on_click():
            pattern = r"\d+"
            match = re.search(pattern, combo.get())
            db.delete_from_database(match[0])
            self.destroy()
            f.show_catalog()

        Label(self, text="Удаление книги из библиотеки:",
                     font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W + E)
        Label(self, text="Выберите запись:",
                     font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        combo = Combobox(self, width=35, state='readonly',
                         values=[f"id{item[0]}  {item[1]}" for item in db.read_all_from_db()])
        combo.current(0)
        combo.grid(row=1, column=1)
        Button(self, text="Удалить", activeforeground="blue", command=on_click,
                      font='arial 16', width=10).grid(row=5, column=0, padx=10, pady=5)
        Button(self, text="Закрыть", activeforeground="blue", command=self.destroy,
                      font='arial 16', width=10).grid(row=5, column=1, sticky=E, pady=5)

    def pop_up_update_record(self, db):
        """
        Окно - редактирование записи
        """
        def on_click():
            db.update_record_in_database(int(id_edit.get()), name_edit.get(), author_edit.get(),
                          genre_edit.get(), year_edit.get())
            self.destroy()
            f.show_catalog()

        def show_selected(event):
            """
            Отображение данных выбранной записи для редактирования
            """
            pattern = r"\d+"
            match = re.search(pattern, combo.get())
            rec = db.get_record(int(match[0]))
            btn1.configure(state='normal')
            id_edit.configure(state='normal')
            id_edit.delete(0, END)
            id_edit.insert(END, rec[0][0])
            id_edit.configure(state='readonly')
            name_edit.delete(0, END)
            name_edit.insert(END, rec[0][1])
            author_edit.delete(0, END)
            author_edit.insert(END, rec[0][2])
            genre_edit.delete(0, END)
            genre_edit.insert(END, rec[0][3])
            year_edit.delete(0, END)
            year_edit.insert(END, rec[0][4])

        Label(self, text="Редактирование информации о книге:",
                     font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W + E)
        Label(self, text="Выберите запись:",
                      font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        combo = Combobox(self, width=35, state='readonly',
                         values=[f"id{item[0]}  {item[1]}" for item in db.read_all_from_db()])
        combo.grid(row=1, column=1)
        combo.bind("<<ComboboxSelected>>", show_selected)
        Label(self, text="Название: ", font='arial 14').grid(row=2, column=0, sticky=W, padx=10, pady=2)
        name_edit = Entry(self, width=40)
        name_edit.grid(row=2, column=1)
        Label(self, text="Автор: ", font='arial 14').grid(row=3, column=0, sticky=W, padx=10, pady=2)
        author_edit = Entry(self, width=40)
        author_edit.grid(row=3, column=1)
        Label(self, text="Жанр: ", font='arial 14').grid(row=4, column=0, sticky=W, padx=10, pady=2)
        genre_edit = Entry(self, width=40)
        genre_edit.grid(row=4, column=1)
        Label(self, text="Год создания: ", font='arial 14').grid(row=5, column=0, sticky=W, padx=10, pady=2)
        year_edit = Entry(self, width=4)
        year_edit.grid(row=5, column=1, sticky=W)
        Label(self, text="id: ", font='arial 14').grid(row=6, column=0, sticky=W, padx=10, pady=2)
        id_edit = Entry(self, width=4, state='readonly')
        id_edit.grid(row=6, column=1, sticky=W)
        btn1 = Button(self, text="Сохранить", activeforeground="blue", command=on_click,
                      font='arial 16', width=10, state='disabled')
        btn1.grid(row=7, column=0, padx=10, pady=5)
        Button(self, text="Закрыть", activeforeground="blue", command=self.destroy,
                      font='arial 16', width=10).grid(row=7, column=1, sticky=E, pady=5)

    def pop_up_find_record(self, root, db):
        """
        Окно - поиск записей по параметрам
        """
        def on_click():
            filter_records = db.select_records_by_filter(combo_name.get(), combo_author.get(), combo_genre.get())
            f.show_catalog(filter_records)
            self.destroy()

        Label(self, text="Поиск по базе данных:",
                     font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W + E)
        Label(self, text="По названию:",
                     font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        combo_name = Combobox(self, width=35, state='readonly',
                              values=[f"{item[1]}" for item in db.read_all_from_db()])
        combo_name.grid(row=1, column=1)

        Label(self, text="По автору:",
                     font='arial 14').grid(row=2, column=0, sticky=W, padx=10, pady=2)
        combo_author = Combobox(self, width=35, state='readonly',
                                values=[f"{item[0]}" for item in db.read_from_database_by_filter("author")])
        combo_author.grid(row=2, column=1)

        Label(self, text="По жанру:",
                     font='arial 14').grid(row=3, column=0, sticky=W, padx=10, pady=2)
        combo_genre = Combobox(self, width=35, state='readonly',
                               values=[f"{item[0]}" for item in db.read_from_database_by_filter("genre")])
        combo_genre.grid(row=3, column=1)

        btn1 = Button(self, text="Показать", activeforeground="blue",
                      font='arial 16', width=10, command=on_click)
        btn1.grid(row=7, column=0, padx=10, pady=5)
        Button(self, text="Закрыть", activeforeground="blue", command=self.destroy,
                      font='arial 16', width=10).grid(row=7, column=1, sticky=E, pady=5)