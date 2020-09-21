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
        but_m0 = Button(self.frame_menu, text="В начало", activeforeground="blue",
                        font='arial 16', width=12, command=f.show_welcome, state='disabled')
        but_m0.pack()
        but_m1 = Button(self.frame_menu, text="Каталог", activeforeground="blue",
                        font='arial 16', width=12, command=f.show_catalog, state='disabled')
        but_m1.pack()
        but_m2 = Button(self.frame_menu, text="Добавить", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        but_m2.pack()
        but_m3 = Button(self.frame_menu, text="Удалить", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        but_m3.pack()
        but_m4 = Button(self.frame_menu, text="Редактировать", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        but_m4.pack()
        but_m5 = Button(self.frame_menu, text="Поиск", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        but_m5.pack()
        but_m6 = Button(self.frame_menu, text="Сохранить", activeforeground="blue",
                        font='arial 16', width=12, state='disabled')
        but_m6.pack()
        but_m7 = Button(self.frame_menu, text="Загрузить", command=f.load_database, activeforeground="blue",
                        font='arial 16', width=12, state='normal')
        but_m7.pack()
        but_m8 = Button(self.frame_menu, text="Выйти", command=f.biblio_close, activeforeground="blue",
                        font='arial 16', width=12).pack(side=BOTTOM)

        text1 = Text(self.frame_main, wrap=WORD, font="arial 14", bg="lightgray")
        text1.pack()
