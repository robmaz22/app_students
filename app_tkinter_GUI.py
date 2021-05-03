import tkinter as tk
from tkinter import filedialog
from database import create_database
from tkinter import messagebox


# Otwieranie bazy danych z pliku txt z podanej lokalizacji
def open_file():
    filename = filedialog.askopenfilename(filetypes=[("Plik tekstowy", "*.txt")])
    create_database.create_from_txt(filename)
    messagebox.showinfo(title='Komunikat', message='Utworzono bazę danych!')


# tworzenie bazy danych ręcznie
def create_manual():
    edit_window = tk.Tk()
    edit_window.title('Stwórz bazę')

    title_label = tk.Label(edit_window, text='Podaj dane ucznia').grid(column=0, row=0, columnspan=2)
    name_label = tk.Label(edit_window, text='Imię').grid(column=0, row=1)
    lname_label = tk.Label(edit_window, text='Nazwisko').grid(column=0, row=2)
    class_label = tk.Label(edit_window, text='Klasa').grid(column=0, row=3)
    school_label = tk.Label(edit_window, text='Szkoła').grid(column=0, row=4)
    test_label = tk.Label(edit_window, text='Punkty za test').grid(column=0, row=5)
    work_label = tk.Label(edit_window, text='Punkty za pracę').grid(column=0, row=6)

    name_entry = tk.Entry(edit_window).grid(column=1, row=1)
    lname_entry = tk.Entry(edit_window).grid(column=1, row=2)
    class_entry = tk.Entry(edit_window).grid(column=1, row=3)
    school_entry = tk.Entry(edit_window).grid(column=1, row=4)
    test_entry = tk.Entry(edit_window).grid(column=1, row=5)
    work_entry = tk.Entry(edit_window).grid(column=1, row=6)

    save_button = tk.Button(edit_window, text='Zapisz').grid(column=0, row=7, padx=10, pady=10)
    delete_button = tk.Button(edit_window, text='Wyczyść dane').grid(column=1, row=7, padx=10, pady=10)


# Przejście na wybór nowej bazy danych
def create_new():
    welcome_frame.pack_forget()
    create_frame = tk.Frame(root, bg='white')
    create_frame.pack(fill='both', expand=1)
    new_button = tk.Button(create_frame, text='Wczytaj z pliku...', command=open_file)
    new_button.pack(pady=30)
    read_button = tk.Button(create_frame, text='Stwórz ręcznie', command=create_manual)
    read_button.pack()


# tworzenie głównego okna i menu
root = tk.Tk()
root.title('My App')
root.geometry('440x170')

menu_bar = tk.Menu(root)
option_menu = tk.Menu(menu_bar, tearoff=0)
option_menu.add_command(label="Ustawienia")
menu_bar.add_cascade(label="Opcje", menu=option_menu)
helpmenu = tk.Menu(menu_bar, tearoff=0)
helpmenu.add_command(label="Jak korzystać?")
helpmenu.add_command(label="O programie...")
menu_bar.add_cascade(label="Pomoc", menu=helpmenu)

root.config(menu=menu_bar)

welcome_frame = tk.Frame(root, bg='white')
welcome_frame.pack(fill='both', expand=1)
title_label = tk.Label(welcome_frame, text="WITAJ W PROGRAMIE DO ANALIZY DANYCH", bg='white')
title_label.config(font=("Cantarell 13 bold"))
title_label.pack(pady=15, padx=20)
create_button = tk.Button(welcome_frame, text='Utwórz nową bazę danych', command=create_new)
create_button.pack(pady=5)
open_button = tk.Button(welcome_frame, text='Otwórz istniejącą bazę danych')
open_button.pack(pady=5)

root.mainloop()
