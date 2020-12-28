#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# sudo apt install python3-tk
import os
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import locale

w = 655
h = 660
w_help = 810
h_help = 600
h_st = 48
register = 0
start_switch = '#'
file_exclude = 'mysearch.exclude'
myemail = '646976696b733230303840676d61696c2e636f6d'
version = 3


def CenteredWindow(root):
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = int((sw - w) / 2)
    y = int((sh - h) / 2)
    return w, h, x, y


def get_files_exclude(file_exclude):
    exclude_list = []
    if os.path.exists(file_exclude):
        with open(file_exclude, 'r') as f:
            f_lines = f.readlines()
        for f_line in f_lines:
            if f_line.strip().startswith(start_switch):
                continue
            elif f_line.strip() and not f_line.strip() in exclude_list:
                exclude_list.append(f_line.strip())
    else:
        return []
    return exclude_list


def compare_path_with_exclude(path, exclude):
    if not exclude:
        return 0
    if set(path.split('/')) & set(exclude):
        return 1
    else:
        return 0


class MySearch():
    def __init__(self, master):
        self.get_exclude_list()
        self.get_folder_rab()
        self.esc_bind = 0
        self.register = 0
        self.recursive = 0

        frame1 = LabelFrame(master, height=1)
        frame1.pack(padx=5, pady=5, side=TOP, fill=X)
        frame2 = LabelFrame(master)
        frame2.pack(padx=5, pady=5, side=TOP, fill=X)
        frame3 = LabelFrame(master, text='Found files')
        frame3.pack(padx=5, pady=5, side=TOP, fill=X)
        frame4 = LabelFrame(master, text='File content')
        frame4.pack(padx=5, pady=5, side=TOP, fill=X)

        # search in folder
        self.l_search_in = Label(frame1, text='Search in:')
        self.l_search_in.pack(side=LEFT)
        self.e_search_in = Entry(frame1)
        self.e_search_in.pack(side=LEFT, expand=1, fill=X)
        self.e_search_in.insert(0, self.folder_rab)

        self.b_up = Button(frame1, text='UP', command=self.folder_up)
        self.b_up.pack(side=RIGHT)

        # filter
        self.l_name = Label(frame2, text='Name:')
        self.l_name.grid(row=1, column=0, pady=3, sticky=W)
        self.e_name = Entry(frame2, width=27)
        self.e_name.grid(row=1, column=1, padx=3, pady=3, columnspan=2)

        self.l_content = Label(frame2, text='Content:')
        self.l_content.grid(row=1, column=3, pady=3, sticky=W)
        self.e_content = Entry(frame2, width=27)
        self.e_content.grid(row=1, column=4, padx=3, pady=3, columnspan=2)

        self.l_modif = Label(frame2, text='Modification date:')
        self.l_modif.grid(row=2, column=0, pady=3, sticky=W)
        self.e_modif_start = Entry(frame2, width=13)
        self.e_modif_start.grid(row=2, column=1, padx=1, pady=3)
        self.e_modif_end = Entry(frame2, width=13)
        self.e_modif_end.grid(row=2, column=2, padx=1, pady=3)

        self.l_size = Label(frame2, text='File size(Mb):')
        self.l_size.grid(row=3, column=0, pady=3, sticky=W)
        self.e_size_start = Entry(frame2, width=13)
        self.e_size_start.grid(row=3, column=1, padx=1, pady=3)
        self.e_size_end = Entry(frame2, width=13)
        self.e_size_end.grid(row=3, column=2, padx=1, pady=3)

        self.chb_register_var = IntVar()
        self.chb_register = Checkbutton(frame2, variable=self.chb_register_var, onvalue=1, offvalue=0,
                                        command=self.register_on)
        self.chb_register.grid(row=4, column=0, pady=3, sticky=W)
        self.chb_register.configure(text='Case sensitive')

        self.chb_recursive_var = IntVar()
        self.chb_recursive = Checkbutton(frame2, variable=self.chb_recursive_var, onvalue=1, offvalue=0,
                                         command=self.recursive_on)
        self.chb_recursive.grid(row=5, column=0, pady=3, sticky=W)
        self.chb_recursive.configure(text='Recursive')

        self.b_start = Button(frame2, width=15, height=3, command=self.start_search, text='START')
        self.b_start.grid(row=2, column=4, rowspan=3, columnspan=2, pady=17)

        # window for find files
        self.l_filepath = Label(frame3)
        self.lb_files = Listbox(frame3, selectmode=SINGLE)  # EXTENDED or SINGLE
        scr_horiz_lb_files = Scrollbar(frame3, orient=HORIZONTAL)
        self.lb_files.config(xscrollcommand=scr_horiz_lb_files.set)
        scr_horiz_lb_files.config(command=self.lb_files.xview)
        scr_vert_lb_files = Scrollbar(frame3, orient=VERTICAL)
        self.lb_files.config(yscrollcommand=scr_vert_lb_files.set)
        scr_vert_lb_files.config(command=self.lb_files.yview)

        self.l_filepath.pack(side=TOP, fill=X)
        scr_horiz_lb_files.pack(side=BOTTOM, fill=X)
        self.lb_files.pack(side=LEFT, expand=True, fill=BOTH)
        scr_vert_lb_files.pack(side=RIGHT, fill=Y)
        
        # window for content
        self.lb_content = Listbox(frame4, selectmode=SINGLE)  # EXTENDED or SINGLE
        scr_horiz_content = Scrollbar(frame4, orient=HORIZONTAL)
        self.lb_content.config(xscrollcommand=scr_horiz_content.set)
        scr_horiz_content.config(command=self.lb_content.xview)
        scr_vert_content = Scrollbar(frame4, orient=VERTICAL)
        self.lb_content.config(yscrollcommand=scr_vert_content.set)
        scr_vert_content.config(command=self.lb_content.yview)

        scr_horiz_content.pack(side=BOTTOM, fill=X)
        self.lb_content.pack(side=LEFT, expand=True, fill=BOTH)
        scr_vert_content.pack(side=RIGHT, fill=Y)

        self.print_dirs_files_list()

    def get_exclude_list(self):
        try:
            exclude_file_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), file_exclude)
        except:
            exclude_file_path = os.path.join(os.getcwd(), file_exclude)
        if os.path.exists(exclude_file_path):
            self.exclude_list = get_files_exclude(exclude_file_path)
        else:
            self.exclude_list = []

    def get_folder_rab(self):
        try:
            self.folder_rab = os.path.normpath(self.e_search_in.get())
        except:
            self.folder_rab = os.getcwd()

    def set_folder_rab(self):
        self.e_search_in.delete(0, END)
        self.e_search_in.insert(END, self.folder_rab)

    def start_search(self):
        self.esc_bind = 0
        self.search_name = self.e_name.get()
        self.search_content = self.e_content.get()
        self.folder_rab = os.path.normpath(self.e_search_in.get())
        self.set_folder_rab()
        self.lb_files.delete(0, END)
        self.lb_content.delete(0, END)
        self.l_filepath.configure(text='Wait, searching . . .', anchor='w')
        self.files_dic = {}
        if not os.path.exists(self.folder_rab):
            self.lb_files.insert('Error: No folder {}'.format(self.folder_rab))
            return
        if self.recursive:
            self.print_dirs_files_list_in_lb_files_recursive()
        else:
            self.print_dirs_files_list_in_lb_files_locale()

        dirs, files = [], []
        self.lb_files.delete(0, END)
        for file_name in self.files_dic.keys():
            f_list = self.files_dic[file_name]
            for f_path in sorted(f_list):
                if os.path.isdir(f_path):
                    dirs.append(f_path)
                else:
                    files.append(f_path)

        if len(self.folder_rab) == 1 or os.path.splitdrive(self.folder_rab)[1] == '\\':
            len_folder_rab = len(self.folder_rab)
        else:
            len_folder_rab = len(self.folder_rab) + 1

        for dir_path in sorted(dirs, key=self.sort_by_name):
            self.lb_files.insert(END, '[{}]'.format(dir_path[len_folder_rab:]))
        for f_path in sorted(files, key=self.sort_by_name):
            self.lb_files.insert(END, f_path[len_folder_rab:])
        if len(dirs) + len(files):
            self.l_filepath.configure(text='Found matches  dirs:{}  files:{}'.format(len(dirs), len(files)), anchor='w')
        else:
            self.l_filepath.configure(text='No matches', anchor='w')

    def print_dirs_files_list(self):
        self.lb_files.delete(0, END)
        self.lb_content.delete(0, END)
        self.get_folder_rab()
        self.set_folder_rab()
        files = [os.path.join(self.folder_rab, f) for f in os.listdir(self.folder_rab) if
                 os.path.isfile(os.path.join(self.folder_rab, f))]
        dirs = [os.path.join(self.folder_rab, f) for f in os.listdir(self.folder_rab) if
                 os.path.isdir(os.path.join(self.folder_rab, f))]
        for dir_path in sorted(dirs, key=self.sort_by_name):
            self.lb_files.insert(END, '[' + os.path.basename(dir_path) + ']')
            self.lb_files.update()
            if self.esc_bind:
                return
        for file_path in sorted(files, key=self.sort_by_name):
            self.lb_files.insert(END, os.path.basename(file_path))
            self.lb_files.update()
            if self.esc_bind:
                return
        if len(dirs) + len(files):
            self.l_filepath.configure(text='All  dirs:{}  files:{}'.format(len(dirs), len(files)), anchor='w')
        else:
            self.l_filepath.configure(text='No dirs and files', anchor='w')

    def print_in_lb(self, path, files):
        for file_name in files:
            file_path = os.path.join(path, file_name)
            if compare_path_with_exclude(file_path, self.exclude_list):
                continue
            if self.e_name.get() and not self.find_name_in_path(file_path, self.search_name):
                continue
            if self.e_content.get() and not self.find_content_in_file(file_path):
                continue
            if not self.compare_size_file(file_path):
                continue
            if not self.compare_date_file(file_path):
                continue
            # self.l_filepath.configure(text=file_path, anchor='w')
            file_name = os.path.basename(file_path)
            if file_name in self.files_dic.keys():
                self.files_dic[file_name] = self.files_dic[file_name] + [file_path]
            else:
                self.files_dic[file_name] = [file_path]
            if os.path.isdir(file_path):
                self.lb_files.insert(END, '[{}]'.format(os.path.basename(file_path)))
            else:
                self.lb_files.insert(END, os.path.basename(file_path))
            self.lb_files.update()
            if self.esc_bind:
                self.l_filepath.configure(text='')
                return 1
        self.l_filepath.configure(text='')
        return 0

    def print_dirs_files_list_in_lb_files_locale(self):
        self.lb_files.delete(0, END)
        dirs = [d for d in os.listdir(self.folder_rab) if os.path.isdir(os.path.join(self.folder_rab, d))]
        files = [f for f in os.listdir(self.folder_rab) if os.path.isfile(os.path.join(self.folder_rab, f))]
        if self.print_in_lb(self.folder_rab, dirs):
            return
        if self.print_in_lb(self.folder_rab, files):
            return

    def print_dirs_files_list_in_lb_files_recursive(self):
        paths = self.get_dirs_files_in_folder()
        self.lb_files.delete(0, END)
        self.lb_files.update()
        for path, dirs, files in paths:
            if compare_path_with_exclude(path, self.exclude_list):
                continue
            if self.print_in_lb(path, dirs):
                self.esc_bind = 0
                return
            if self.print_in_lb(path, files):
                self.esc_bind = 0
                return

    def get_dirs_files_in_folder(self):
        self.get_folder_rab()
        self.dirs_list, self.files_list = [], []
        for path, dirs, files in os.walk(self.folder_rab, topdown=True):
            yield path, dirs, files
            # for dir in dirs:
            #     dir_path = os.path.join(path, dir)
            #     self.dirs_list.append(dir_path)
            # for file_name in files:
            #     file_path = os.path.join(path, file_name)
            #     self.files_list.append(file_path)

    def folder_up(self):
        folder_new = os.path.dirname(self.folder_rab)
        self.e_search_in.delete(0, END)
        if os.path.exists(folder_new):
            self.folder_rab = folder_new
        self.set_folder_rab()
        self.print_dirs_files_list()

    def open_folder_as_filedialog(self, event):
        self.get_folder_rab()
        folder_new = filedialog.askdirectory(initialdir=self.folder_rab)
        if folder_new:
            if os.path.exists(folder_new):
                self.folder_rab = folder_new
            self.set_folder_rab()
            self.print_dirs_files_list()

    def update_folder(self, event):
        self.print_dirs_files_list()

    def key_ecs_bind(self, event):
        self.menu_close(event='')
        if messagebox.askyesno('Stop searching?', 'Are you sure?'):
            self.esc_bind = 1

    def register_on(self):
        if self.chb_register_var.get():
            self.register = 1
        else:
            self.register = 0

    def recursive_on(self):
        if self.chb_recursive_var.get():
            self.recursive = 1
        else:
            self.recursive = 0

    def find_name_in_path(self, path, name):
        if not self.register:
            path = path.lower()
            name = name.lower()
        if path and name:
            if path[len(self.folder_rab):].find(name) != -1:
                return 1
        return 0

    def search_content_in_file(self):
        content = self.e_content.get()
        file_path = os.path.join(self.folder_rab, self.lb_files.get(self.lb_files.curselection()))
        res_list = []
        if content and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    for i, line in enumerate(f.readlines()):
                        if self.register:
                            if line.find(content) != -1:
                                res_list.append([i + 1, line.strip()])
                        else:
                            if line.lower().find(content.lower()) != -1:
                                res_list.append([i + 1, line.strip()])
            except:
                pass
                # print('Error open', file_path)
        return res_list

    def line_clicked(self, event):
        self.lb_content.delete(0, END)
        file_name = os.path.normpath(self.lb_files.get(self.lb_files.curselection()))
        file_path = os.path.normpath(os.path.join(self.folder_rab, file_name))
        try:
            if file_name and self.e_content.get() and os.path.exists(file_path):
                self.content_list = self.search_content_in_file()
                if self.content_list:
                    for content in self.content_list:
                        self.lb_content.insert(END, content)
                return
            if not self.e_content.get():
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    self.lb_content.insert(END, line.strip())
                    self.lb_content.update()
        except:
            return

    def line_clicked_double(self, event):
        self.get_folder_rab()
        # self.lb_content.delete(0, END)
        file_name = self.lb_files.get(self.lb_files.curselection())
        if file_name.startswith('[') and file_name.endswith(']'):
            self.folder_rab = os.path.normpath(os.path.join(self.folder_rab, file_name[1:-1]))
            self.set_folder_rab()
            self.print_dirs_files_list()
            return
        else:
            file_path = os.path.normpath(os.path.join(self.folder_rab, file_name))
            if os.path.islink(file_path):
                return
            if os.path.isfile(file_path):
                if sys.platform == 'win32':
                    try:
                        os.startfile(file_path)
                        return
                    except:
                        return
                try:
                    subprocess.run(['xdg-open', file_path])
                    return
                except:
                    return
            else:
                return

    def find_content_in_file(self, file_path):
        if os.path.exists(file_path):
            content = self.e_content.get()
            try:
                with open(file_path, 'r') as f:
                    for line in f.readlines():
                        if self.register:
                            if line.find(content) == -1:
                                continue
                            else:
                                return 1
                        else:
                            if line.lower().find(content.lower()) == -1:
                                continue
                            else:
                                return 1
                return 0
            except:
                return 0

    def compare_size_file(self, file_path):
        if self.e_size_start.get() or self.e_size_end.get():
            if os.path.isfile(file_path):
                KB = 1024.0
                MB = KB * KB
                try:
                    size_start = float(self.e_size_start.get())
                except:
                    size_start = 0
                try:
                    size_end = float(self.e_size_end.get())
                except:
                    size_end = MB*MB

                try:
                    size_file = os.stat(file_path).st_size
                except:
                    return 0

                if size_start * MB < size_file < size_end * MB:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 1

    def compare_date_file(self, file_path):
        if self.e_modif_start.get() or self.e_modif_end.get():
            try:
                e_start = self.e_modif_start.get()
                time_start = time.mktime((int(e_start.split('.')[0]),
                                          int(e_start.split('.')[1]),
                                          int(e_start.split('.')[2]),
                                          0, 0, 0, 0, 0, 0))
            except:
                time_start = time.mktime((time.localtime(0)))
            try:
                e_end = self.e_modif_end.get()
                time_end = time.mktime((int(e_end.split('.')[0]),
                                          int(e_end.split('.')[1]),
                                          int(e_end.split('.')[2]),
                                          0, 0, 0, 0, 0, 0))
            except:
                time_end = time.mktime((time.localtime(time.time())))
            try:
                mtime_file = os.stat(file_path).st_mtime
            except:
                return 0
            if time_start < mtime_file < time_end:
                return 1
            else:
                return 0
        else:
            return 1

    def sort_by_name(self, f_path):
        return f_path[len(self.folder_rab):].lower()

    def menu_close(self, event):
        try:
            self.help.destroy()
        except:
            pass

    def help_print(self, event):
        help_txt_ru = '''
    Описание:
    MySearch предназначен для поиска папок и файлов по имени,
    по содержимому в файлах, по указанной дате изменения,
    по заданному размеру в мегабайтах.

    Основное управление:

    "Search in:"
    Двойной клик по строке пути поиска откроется меню выбора пути поиска.
    По умолчанию: путь поиска, это место запуска программы Mysearch.

    "Name:"
    Задайте имя файла или папки поиска.
    Для поиска файлов по расширению, укажите расширение файла (например: .jpg)

    "Content:"
    Задайте слово, которое необходимо найти в файлах.

    "Modification date"
    Укажите начало (левое поле) и окончание (правое поле) даты изменения файла
    Если отсутствует дата начала, то ищется с времени равное ноль.
    Если отсутствует дата окончания, то ищется до даты запуска программы.
    Формат даты: YYYY.mm.dd
    (Пример: 2020.11.05)

    "File zise"
    Укажите минимальное (левое поле) и максимальное (правое поле) размер файла в МБ.
    Если искомый размер файла меньше 1 Мб, то значение указывается с точкой.
    (пример 100 МБ: 100)
    (пример 120 КБ: 0.12)
    (пример 120 Байт: 0.00012)

    "Case sensitive"
    Если установлен флаг, то поиск будет с учетом регистра.
    Флаг влияет на "Name:" и "Content:"

    "Recursive"
    Установите флажек для поиска файлов рекурсивно.
    (поиск во всех вложенных папках и подпапках)

    Клавиши клавиатуры:
    1. "Esc" - Прервать поиск.
    2. "F1" - Помощь.
    3. "F3" - Вывести все папки и файлы в окне "Found files"
        (файл mysearch.exclude не учитывается)

    Общее дополнение:
    1. Имена папок в поле "Found files" выделяются слева и справа значками
        '[' и ']' соответственно (Пример: [folder])
    2. Двойной клик по имени ПАПКИ в окне "Found files" переход в эту папку
    3. Одинарный клик по имени файла в окне "Found files":
        если нет параметра поиска по содержимому в поле "Content:",
        выведет содержимое тестового файла в окне "File content";
        если указан "Content:", то покажет строку совпадения
        и номер строки в окне "File content" ("Start" можно не нажимать)
    4. Двойной клик по имени файла в окне "Found files",
        откроет файл в редакторе по умолчанию.
    5. Кнопка "Start" - начать поиск с учетом параметров поиска
        (если параметров нет - вывести список всех папок и файлов
        за исключением тех, которые указаны в файле mysearch.exclude)

    Для запуска программы в Debian, Ubuntu, OpenSuse:
    sudo apt install python3-tk
        '''
        help_txt_en = ''' 
    Description:
    MySearch is designed to search for folders and files by name,
    by content in files, by specified modification date,
    by the specified size in megabytes.

    Main control:

    "Search in:"
    Double-clicking on the search path line will open the search path selection menu.
    Default: search path, this is where the Mysearch program starts.

    "Name:"
    Specify a name for the file or search folder.
    To search for files by extension, specify the file extension (for example: .jpg)

    "Content:"
    Enter the word that you want to find in the files.

    "Modification date"
    Specify the start (left margin) and end (right margin) of the file modified date
    If there is no start date, then the search is performed with a time equal to zero.
    If there is no end date, it is searched before the program start date.
    Date format: YYYY.mm.dd
    (Example: 2020.11.05)

    "File zise"
    Enter the minimum (left margin) and maximum (right margin) file size in MB.
    If the required file size is less than 1 MB, then the value is indicated with a period.
    (example 100 MB: 100)
    (example 120 KB: 0.12)
    (example 120 Bytes: 0.00012)

    "Case sensitive"
    If the flag is set, the search will be case sensitive.
    The flag affects "Name:" and "Content:"

    "Recursive"
    Check the box to search for files recursively.
    (search in all subfolders and subfolders)

    Keyboard Keys:
    1. "Esc" - Abort the search.
    2. "F1" - Help.
    3. "F3" - Display all folders and files in the "Found files" window
        (the mysearch.exclude file is ignored)

    General addition:
    1. Folder names in the "Found files" field are highlighted on the left 
        and right with icons '[' and ']' respectively 
        (Example: [folder])
    2. Double click on the FOLDER name in the "Found files" window 
        to go to this folder
    3. Single click on the file name in the "Found files" window:
        if there is no content search parameter in the "Content:" field,
        will display the contents of the test file in the "File content" window;
        if "Content:" is specified, it will show the match string
        and the line number in the "File content" window ("Start" can be omitted)
    4. Double click on the file name in the "Found files" window,
        will open the file in the default editor.
    5. "Start" button - start the search based on the search parameters
        (if there are no parameters, display a list of all folders and files
        excluding those specified in the mysearch.exclude file)

    To run the program on Debian, Ubuntu, OpenSuse:
    sudo apt install python3-tk
        '''

        if locale.getdefaultlocale()[0] == 'ru_RU':
            help_txt = help_txt_ru
        else:
            help_txt = help_txt_en

        sw = 770
        sh = 400
        # x = int((sw - w) / 2)
        # y = int((sh - h) / 2)
        self.help = Toplevel()
        self.help.geometry('{}x{}+{}+{}'.format(sw, sh, 0, 0))
        self.help.title('Help MySearch v' + str(version))
        text_window = Text(self.help)  # , width=width_w, height=height_w)
        text_window.pack(side=LEFT, fill=BOTH, expand=True)
        # button = Button(help, text=self.lang_dic['text_button'], command=help.destroy)
        # button.pack(side=BOTTOM)
        text_window.insert(END, help_txt)

        scrollbar1 = Scrollbar(self.help)
        scrollbar1.pack(side=RIGHT, fill=Y)
        text_window.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=text_window.yview)
        self.help.bind('<Escape>', self.menu_close)


def get_end_time_program():
    file_path = sys.argv[0]
    try:
        f = open(file_path, 'rb')
        # print('open file')
        f.seek(64, 0)
        time_end = int(f.read(10).decode())
        f.close()
        time_start = int(time.time())
        if int(time_start) > int(time_end):
            sys.exit(0)
    except:
        # print('Error time')
        sys.exit(0)
    # print('TIME OK!!!!!')


def main():
    root = Tk()

    root.title('My search files v' + str(version))
    root.geometry('{}x{}+{}+{}'.format(*CenteredWindow(root)))

    app = MySearch(root)

    app.e_search_in.bind('<Double-ButtonRelease-1>', app.open_folder_as_filedialog)
    app.lb_files.bind('<ButtonRelease-1>', app.line_clicked)
    app.lb_files.bind('<Double-ButtonRelease-1>', app.line_clicked_double)  # xdg-open , kde-open

    root.bind('<F1>', app.help_print)
    root.bind('<Escape>', app.key_ecs_bind)
    root.bind('<F3>', app.update_folder)

    root.mainloop()


if __name__ == '__main__':
    if sys.platform == 'win32':
        get_end_time_program()
    main()
