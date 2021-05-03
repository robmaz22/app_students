import tkinter as tk
from tkinter import filedialog
from database import create_database
from tkinter import messagebox


class mainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('My App')
        self.master.geometry('440x170')

        self.create_menu()
        self.welcome_screen()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.master)
        self.option_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.option_menu.add_command(label="Ustawienia")
        self.menu_bar.add_cascade(label="Opcje", menu=self.option_menu)
        self.helpmenu = tk.Menu(self.menu_bar, tearoff=0)
        self.helpmenu.add_command(label="Jak korzystać?")
        self.helpmenu.add_command(label="O programie...")
        self.menu_bar.add_cascade(label="Pomoc", menu=self.helpmenu)

        self.master.config(menu=self.menu_bar)

    def welcome_screen(self):
        self.welcome_frame = tk.Frame(self.master, bg='white')
        self.welcome_frame.pack(fill='both', expand=1)
        self.title_label = tk.Label(self.welcome_frame, text="WITAJ W PROGRAMIE DO ANALIZY DANYCH", bg='white')
        self.title_label.config(font=("Cantarell 13 bold"))
        self.title_label.pack(pady=15, padx=20)
        self.create_button = tk.Button(self.welcome_frame, text='Utwórz nową bazę danych', command=self.create_new)
        self.create_button.pack(pady=5)
        self.open_button = tk.Button(self.welcome_frame, text='Otwórz istniejącą bazę danych')
        self.open_button.pack(pady=5)

    # wybór tworzenia nowej bazy
    def create_new(self):
        self.welcome_frame.pack_forget()
        self.create_frame = tk.Frame(self.master, bg='white')
        self.create_frame.pack(fill='both', expand=1)
        self.new_button = tk.Button(self.create_frame, text='Wczytaj z pliku...', command=self.open_file)
        self.new_button.pack(pady=30)
        self.read_button = tk.Button(self.create_frame, text='Stwórz ręcznie', command=self.create_manual)
        self.read_button.pack()

    def start_analysis(self):
        self.create_frame.pack_forget()

    # Otwieranie bazy danych z pliku txt z podanej lokalizacji
    def open_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Plik tekstowy", "*.txt")])
        create_database.create_from_txt(self.filename)
        messagebox.showinfo(title='Komunikat', message='Utworzono bazę danych!')
        self.start_analysis()

    # tworzenie bazy danych ręcznie
    def create_manual(self):
        self.edit_window = tk.Tk()
        self.edit_window.title('Stwórz bazę')

        self.title_label = tk.Label(self.edit_window, text='Podaj dane ucznia').grid(column=0, row=0, columnspan=2)
        self.name_label = tk.Label(self.edit_window, text='Imię').grid(column=0, row=1)
        self.lname_label = tk.Label(self.edit_window, text='Nazwisko').grid(column=0, row=2)
        self.class_label = tk.Label(self.edit_window, text='Klasa').grid(column=0, row=3)
        self.school_label = tk.Label(self.edit_window, text='Szkoła').grid(column=0, row=4)
        self.test_label = tk.Label(self.edit_window, text='Punkty za test').grid(column=0, row=5)
        self.work_label = tk.Label(self.edit_window, text='Punkty za pracę').grid(column=0, row=6)

        self.name_entry = tk.Entry(self.edit_window).grid(column=1, row=1)
        self.lname_entry = tk.Entry(self.edit_window).grid(column=1, row=2)
        self.class_entry = tk.Entry(self.edit_window).grid(column=1, row=3)
        self.school_entry = tk.Entry(self.edit_window).grid(column=1, row=4)
        self.test_entry = tk.Entry(self.edit_window).grid(column=1, row=5)
        self.work_entry = tk.Entry(self.edit_window).grid(column=1, row=6)

        self.save_button = tk.Button(self.edit_window, text='Zapisz').grid(column=0, row=7, padx=10, pady=10)
        self.delete_button = tk.Button(self.edit_window, text='Wyczyść dane').grid(column=1, row=7, padx=10, pady=10)



# tworzenie głównego okna i menu
root = tk.Tk()
app = mainWindow(root)

root.mainloop()
