"""
Дан каталог книг. Реализуйте библиотеку для хранения данных книг
и поиску по каталогу. Каталог должен поддерживать возможность добавления
и удаления книг, редактирования информации о книге, а также обладать
персистентностью (т.е. сохранять библиотеку в внешнем файле и подгружать обратно).
Также необходимо оформить точку входа, поддерживать поиск по различным параметрам
и обеспечить интерфейс взаимодействия пользователя с библиотекой.
"""

from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog as fd
import json
import re

from db import *

WIDTH = 980
HEIGHT = 500


def create_main_window():
    """
    Создание основного окна программы
    """
    def load_database():
        file_name = fd.askopenfilename(filetypes=(("Database", "*.sqlite3"), ))
        global db
        if file_name:
            db = connection_to_database(file_name)
            but_m0.configure(state='normal')
            but_m1.configure(state='normal')
            but_m2.configure(state='normal')
            but_m3.configure(state='normal')
            but_m4.configure(state='normal')
            but_m5.configure(state='normal')
            but_m6.configure(state='normal')
            text1.configure(state='normal')
            text1.delete(1.0, 'end')
            text1.insert('end', "База успешно загружена!")
            text1.configure(state='disabled')

    def save_database():
        file_name = fd.asksaveasfilename(filetypes=(("Database", "*.json"), ))
        if file_name:
            with open(file_name, 'w') as f:
                for item in read_all_from_db(db):
                    json.dump(item, f, indent=4)
                f.close()
            text1.configure(state='normal')
            text1.delete(1.0, 'end')
            text1.insert('end', f"База успешно сохранена в файле {file_name}!")
            text1.configure(state='disabled')

    def show_welcome():
        """
        Отображение общей информации о библиотеке - кнопка 'В начало'
        """
        text1.configure(state='normal')
        text1.delete(1.0, 'end')
        text1.insert('end', f'В нашей базе: {len(read_all_from_db(db))} различных книг\n')
        author_list = []
        genre_list = []
        for item in read_all_from_db(db):
            author_list.append(item[2])
            genre_list.append(item[3])
        text1.insert('end', f'Всего авторов: {len(set(author_list))}\n')
        text1.insert('end', f'Всего жанров: {len(set(genre_list))}\n')
        #text1.insert('end', f"Самая древняя рукопись: {str(min(read_year_from_db(db)))} год\n")
        #text1.insert('end', f"Самая свежая рукопись: {str(max(read_year_from_db(db)))} год")
        text1.configure(state='disabled')

    def show_catalog():
        """
        Отображение каталога записей в библиотеке - кнопка 'Каталог'
        """
        text1.configure(state='normal')
        text1.delete(1.0, 'end')
        for item in read_all_from_db(db):
            text1.insert('end', f'id{item[0]} - "{item[1]}", {item[2]}, {item[3]}, {item[4]} год, {item[5]} шт.\n')
        text1.configure(state='disabled')

    def new_record():
        """
        Отображение доп. окна для внесения новой записи в библиотеку -
        ннопка 'Добавить'
        """
        def nr_exit():
            """
            Закрытие доп. окна при добавлении новой записи без сохранения результатов
            """
            nr_window.destroy()

        def save_nr():
            """
            Закрытие доп. окна и внесение новой записи в базу данных
            """
            insert_new_record(db, new_name.get(), new_author.get(), new_genre.get(), new_year.get())
            nr_window.destroy()
            show_welcome()

        nr_window = Toplevel()
        nr_window.grab_set()
        nr_x = root.winfo_rootx() + root.winfo_reqwidth() // 2
        nr_y = root.winfo_rooty() + root.winfo_reqheight() // 2
        nr_window.geometry(f'500x220+{nr_x - 500 // 2}+{nr_y - 300 // 2}')
        nr_window.overrideredirect(True)
        lbl1 = Label(nr_window, text="Добавление новой книги:",
                       font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W+E)
        lbl2 = Label(nr_window, text="Название: ", font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        new_name = Entry(nr_window, width=40)
        new_name.grid(row=1, column=1)
        lbl3 = Label(nr_window, text="Автор: ", font='arial 14').grid(row=2, column=0, sticky=W, padx=10, pady=2)
        new_author = Entry(nr_window, width=40)
        new_author.grid(row=2, column=1)
        lbl4 = Label(nr_window, text="Жанр: ", font='arial 14').grid(row=3, column=0, sticky=W, padx=10, pady=2)
        new_genre = Entry(nr_window, width=40)
        new_genre.grid(row=3, column=1)
        lbl4 = Label(nr_window, text="Год создания: ", font='arial 14').grid(row=4, column=0, sticky=W, padx=10, pady=2)
        new_year = Entry(nr_window, width=4)
        new_year.grid(row=4, column=1, sticky=W)
        btn1 = Button(nr_window, text="Сохранить", activeforeground="blue", command=save_nr,
                    font='arial 16', width=10).grid(row=5, column=0, padx=10, pady=2)
        btn2 = Button(nr_window, text="Закрыть", activeforeground="blue", command=nr_exit,
                    font='arial 16', width=10).grid(row=5, column=1, sticky=E, pady=2)

    def del_record():
        """
        Отображение доп. окна для удаления существующей записи из библиотеки -
        кнопка 'Удалить'
        """
        def dr_exit():
            """
            Закрытие доп. окна при удалении записи
            """
            dr_window.destroy()

        def del_r():
            """
            Закрытие доп. окна и удаление выбранной записи из библиотеки
            """
            pattern = r"\d+"
            match = re.search(pattern, combo.get())
            delete_record(db, match[0])
            dr_window.destroy()
            show_welcome()

        dr_window = Toplevel()
        dr_window.grab_set()
        dr_x = root.winfo_rootx() + root.winfo_reqwidth() // 2
        dr_y = root.winfo_rooty() + root.winfo_reqheight() // 2
        dr_window.geometry(f'500x140+{dr_x - 500 // 2}+{dr_y - 140 // 2}')
        dr_window.overrideredirect(True)
        lbl1 = Label(dr_window, text="Удаление книги из библиотеки:",
                       font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W+E)
        lbl2 = Label(dr_window, text="Выберите запись:",
                     font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        combo = Combobox(dr_window, width=35, state='readonly',
                         values=[f"id{item[0]}  {item[1]}" for item in read_all_from_db(db)])
        combo.current(0)
        combo.grid(row=1, column=1)
        btn1 = Button(dr_window, text="Удалить", activeforeground="blue", command=del_r,
                      font='arial 16', width=10).grid(row=5, column=0, padx=10, pady=5)
        btn2 = Button(dr_window, text="Закрыть", activeforeground="blue", command=dr_exit,
                      font='arial 16', width=10).grid(row=5, column=1, sticky=E, pady=5)

    def edit_record():
        """
        Отображение доп. окна для удаления существующей записи из библиотеки -
        кнопка 'Удалить'
        """
        def er_exit():
            """
            Закрытие доп. окна при удалении записи
            """
            er_window.destroy()

        def edit_r():
            """
            Закрытие доп. окна и удаление выбранной записи из библиотеки
            """
            update_record(db, int(id_edit.get()), name_edit.get(), author_edit.get(),
                          genre_edit.get(), year_edit.get())
            show_welcome()

        def show_selected(event):
            """
            Отображение данных выбранной записи для редактирования
            """
            pattern = r"\d+"
            match = re.search(pattern, combo.get())
            rec = choose_record(db, int(match[0]))
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

        er_window = Toplevel()
        er_window.grab_set()
        er_x = root.winfo_rootx() + root.winfo_reqwidth() // 2
        er_y = root.winfo_rooty() + root.winfo_reqheight() // 2
        er_window.geometry(f'520x280+{er_x - 500 // 2}+{er_y - 280 // 2}')
        er_window.overrideredirect(True)
        lbl1 = Label(er_window, text="Редактирование информации о книге:",
                        font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W+E)
        lbl12 = Label(er_window, text="Выберите запись:",
                     font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        combo = Combobox(er_window, width=35, state='readonly',
                         values=[f"id{item[0]}  {item[1]}" for item in read_all_from_db(db)])
        combo.grid(row=1, column=1)
        combo.bind("<<ComboboxSelected>>", show_selected)
        lbl2 = Label(er_window, text="Название: ", font='arial 14').grid(row=2, column=0, sticky=W, padx=10, pady=2)
        name_edit = Entry(er_window, width=40)
        name_edit.grid(row=2, column=1)
        lbl3 = Label(er_window, text="Автор: ", font='arial 14').grid(row=3, column=0, sticky=W, padx=10, pady=2)
        author_edit = Entry(er_window, width=40)
        author_edit.grid(row=3, column=1)
        lbl4 = Label(er_window, text="Жанр: ", font='arial 14').grid(row=4, column=0, sticky=W, padx=10, pady=2)
        genre_edit = Entry(er_window, width=40)
        genre_edit.grid(row=4, column=1)
        lbl4 = Label(er_window, text="Год создания: ", font='arial 14').grid(row=5, column=0, sticky=W, padx=10, pady=2)
        year_edit = Entry(er_window, width=4)
        year_edit.grid(row=5, column=1, sticky=W)
        lbl5 = Label(er_window, text="id: ", font='arial 14').grid(row=6, column=0, sticky=W, padx=10, pady=2)
        id_edit = Entry(er_window, width=4, state='readonly')
        id_edit.grid(row=6, column=1, sticky=W)
        btn1 = Button(er_window, text="Сохранить", activeforeground="blue", command=edit_r,
                      font='arial 16', width=10, state='disabled')
        btn1.grid(row=7, column=0, padx=10, pady=5)
        btn2 = Button(er_window, text="Закрыть", activeforeground="blue", command=er_exit,
                      font='arial 16', width=10).grid(row=7, column=1, sticky=E, pady=5)

    def find_record():
        """
        Отображение доп. окна для поиска записи по базе данных
        """
        def fr_exit():
            fr_window.destroy()

        def show_records_by_filter():
            """
            Вывод результатов сортировки записей
            """
            text1.configure(state='normal')
            text1.delete(1.0, 'end')
            for item in select_record_by_filter(db, combo_name.get(), combo_author.get(), combo_genre.get()):
                text1.insert('end', f'id{item[0]} - "{item[1]}", {item[2]}, {item[3]}, {item[4]} год, {item[5]} шт.\n')
            text1.configure(state='disabled')
            fr_exit()

        fr_window = Toplevel()
        fr_window.grab_set()
        fr_x = root.winfo_rootx() + root.winfo_reqwidth() // 2
        fr_y = root.winfo_rooty() + root.winfo_reqheight() // 2
        fr_window.geometry(f'480x200+{fr_x - 480 // 2}+{fr_y - 200 // 2}')
        fr_window.overrideredirect(True)
        lbl1 = Label(fr_window, text="Поиск по базе данных:",
                     font='arial 20 bold', pady=10).grid(row=0, columnspan=2, sticky=W+E)
        lbl2 = Label(fr_window, text="По названию:",
                     font='arial 14').grid(row=1, column=0, sticky=W, padx=10, pady=2)
        combo_name = Combobox(fr_window, width=35, state='readonly',
                         values=[f"{item[1]}" for item in read_all_from_db(db)])
        combo_name.grid(row=1, column=1)

        lbl3 = Label(fr_window, text="По автору:",
                     font='arial 14').grid(row=2, column=0, sticky=W, padx=10, pady=2)
        combo_author = Combobox(fr_window, width=35, state='readonly',
                         values=[f"{item[0]}" for item in set(read_author_from_db(db))])
        combo_author.grid(row=2, column=1)

        lbl4 = Label(fr_window, text="По жанру:",
                     font='arial 14').grid(row=3, column=0, sticky=W, padx=10, pady=2)
        combo_genre = Combobox(fr_window, width=35, state='readonly',
                         values=[f"{item[0]}" for item in set(read_genre_from_db(db))])
        combo_genre.grid(row=3, column=1)

        btn1 = Button(fr_window, text="Показать", activeforeground="blue",
                      font='arial 16', width=10, command=show_records_by_filter)
        btn1.grid(row=7, column=0, padx=10, pady=5)
        btn2 = Button(fr_window, text="Закрыть", activeforeground="blue", command=fr_exit,
                      font='arial 16', width=10).grid(row=7, column=1, sticky=E, pady=5)

    root = Tk()
    root.title("Библиотека v1.0")
    root_x = root.winfo_screenwidth() // 2 - WIDTH // 2
    root_y = root.winfo_screenheight() // 2 - HEIGHT // 2
    root.resizable(width=False, height=False)
    root.geometry(f"{WIDTH}x{HEIGHT}+{root_x}+{root_y}")
    frame_top = Frame(relief=RAISED, borderwidth=2)
    frame_menu = Frame(relief=RAISED, borderwidth=2)
    frame_main = Frame(relief=RAISED, borderwidth=2)
    frame_top.pack(side=TOP, fill=X)
    frame_menu.pack(side=LEFT, fill=Y)
    frame_main.pack(side=LEFT, fill=BOTH)
    label1 = Label(frame_top, text="Добро пожаловать в библиотеку!",
                   font='arial 20 bold', pady=10).pack()
    but_m0 = Button(frame_menu, text="В начало", activeforeground="blue",
                    font='arial 16', width=12, command=show_welcome, state='disabled')
    but_m0.pack()
    but_m1 = Button(frame_menu, text="Каталог", activeforeground="blue",
                    font='arial 16', width=12, command=show_catalog, state='disabled')
    but_m1.pack()
    but_m2 = Button(frame_menu, text="Добавить", activeforeground="blue",
                    font='arial 16', width=12, command=new_record, state='disabled')
    but_m2.pack()
    but_m3 = Button(frame_menu, text="Удалить", activeforeground="blue",
                    font='arial 16', width=12, command=del_record, state='disabled')
    but_m3.pack()
    but_m4 = Button(frame_menu, text="Редактировать", activeforeground="blue",
                    font='arial 16', width=12, command=edit_record, state='disabled')
    but_m4.pack()
    but_m5 = Button(frame_menu, text="Поиск", activeforeground="blue",
                    font='arial 16', width=12, command=find_record, state='disabled')
    but_m5.pack()
    but_m6 = Button(frame_menu, text="Сохранить", command=save_database, activeforeground="blue",
                    font='arial 16', width=12, state='disabled')
    but_m6.pack()
    but_m7 = Button(frame_menu, text="Загрузить", command=load_database, activeforeground="blue",
                    font='arial 16', width=12, state='normal')
    but_m7.pack()
    but_m8 = Button(frame_menu, text="Выйти", command=bl_close, activeforeground="blue",
                    font='arial 16', width=12).pack(side=BOTTOM)

    text1 = Text(frame_main, wrap=WORD, font="arial 14", bg="lightgray")
    text1.pack()
    return root


def bl_close():
    """
    Закрытие основного окна программы
    """
    if db:
        db.close()
    root.destroy()


if __name__ == "__main__":
    db = None
    root = create_main_window()
    root.mainloop()

