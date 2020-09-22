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
                        font='arial 16', width=12, state='disabled')
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