"""
Модуль для работы с графическим интерфейсом на основе Tkinter
"""

from tkinter import *
import functions as f

WIDTH = 980
HEIGHT = 500


class Root(Tk):
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
        lbl_head = Label(self.frame_top, text="Добро пожаловать в библиотеку!",
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
                        font='arial 16', width=12, state='disabled')
        self.but_del.pack()
        self.but_edit = Button(self.frame_menu, text="Редактировать", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        self.but_edit.pack()
        self.but_find = Button(self.frame_menu, text="Поиск", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        self.but_find.pack()
        self.but_save = Button(self.frame_menu, text="Сохранить", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        self.but_save.pack()
        self.but_load = Button(self.frame_menu, text="Загрузить", command=f.load_database, activeforeground="blue",
                        font='arial 16', width=12, state='normal')
        self.but_load.pack()
        self.but_exit = Button(self.frame_menu, text="Выйти", command=f.biblio_close, activeforeground="blue",
                        font='arial 16', width=12).pack(side=BOTTOM)

        self.main_text_field = Text(self.frame_main, wrap=WORD, font="arial 14", bg="lightgray")
        self.main_text_field.pack()

    def main_text_field_on(self):
        self.main_text_field.configure(state='normal')
        self.main_text_field.delete(1.0, 'end')

    def main_text_field_off(self):
        self.main_text_field.configure(state='disabled')

    def main_text_field_insert(self, data_text):
        self.main_text_field.insert('end', data_text)

    def update_after_load_database(self):
        self.but_start.configure(state='normal')
        self.but_catalog.configure(state='normal')
        self.but_add.configure(state='normal')
        self.but_del.configure(state='normal')
        self.but_edit.configure(state='normal')
        self.but_find.configure(state='normal')
        self.but_save.configure(state='normal')
        self.main_text_field_on()
        self.main_text_field_insert("База успешно загружена!")
        self.main_text_field_off()


class PopUpWindow(Toplevel):
    def __init__(self, root, width, height):
        super().__init__()
        self.grab_set()
        nr_x = root.winfo_rootx() + root.winfo_reqwidth() // 2
        nr_y = root.winfo_rooty() + root.winfo_reqheight() // 2
        self.geometry(f'{width}x{height}+{nr_x - width // 2}+{nr_y - height // 2}')
        self.overrideredirect(True)

    def pop_up_add_record(self):
        lbl1 = Label(self, text="Добавление новой книги:",
                     font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W + E)
        lbl2 = Label(self, text="Название: ", font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        new_name = Entry(self, width=40)
        new_name.grid(row=1, column=1)
        lbl3 = Label(self, text="Автор: ", font='arial 14').grid(row=2, column=0, sticky=W, padx=10, pady=2)
        new_author = Entry(self, width=40)
        new_author.grid(row=2, column=1)
        lbl4 = Label(self, text="Жанр: ", font='arial 14').grid(row=3, column=0, sticky=W, padx=10, pady=2)
        new_genre = Entry(self, width=40)
        new_genre.grid(row=3, column=1)
        lbl4 = Label(self, text="Год создания: ", font='arial 14').grid(row=4, column=0, sticky=W, padx=10, pady=2)
        new_year = Entry(self, width=4)
        new_year.grid(row=4, column=1, sticky=W)
        btn1 = Button(self, text="Сохранить", activeforeground="blue", command=f.new_record,
                      font='arial 16', width=10).grid(row=5, column=0, padx=10, pady=2)
        btn2 = Button(self, text="Закрыть", activeforeground="blue", command=self.destroy,
                      font='arial 16', width=10).grid(row=5, column=1, sticky=E, pady=2)
        return new_name.get(), new_author.get(), new_genre.get(), new_year.get()
