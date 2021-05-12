import tkinter as tk
from tkinter import filedialog
from database import create_database
from tkinter import messagebox
from database import database_analysis
from GUI import edit_students


class mainWindow:

    # Inicjalizacja
    def __init__(self, master):
        self.master = master
        self.master.title('My App')
        self.master.geometry('440x170')
        self.master.resizable(False, False)

        self.create_menu()
        self.welcome_screen()

    # Tworzenie menu
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

    # Tworzenie ramki z głównym powitaniem
    def welcome_screen(self):
        self.welcome_frame = tk.Frame(self.master, bg='white')
        self.welcome_frame.pack(fill='both', expand=1)
        self.title_label = tk.Label(self.welcome_frame, text="WITAJ W PROGRAMIE DO ANALIZY DANYCH", bg='white')
        self.title_label.config(font="Cantarell 13 bold")
        self.title_label.pack(pady=15, padx=20)
        self.create_button = tk.Button(self.welcome_frame, text='Utwórz nową bazę danych', command=self.create_new)
        self.create_button.pack(pady=5)
        self.open_button = tk.Button(self.welcome_frame, text='Otwórz istniejącą bazę danych',
                                     command=self.open_exst_base)
        self.open_button.pack(pady=5)

    # wybór tworzenia nowej bazy
    def create_new(self):
        self.welcome_frame.pack_forget()
        self.create_frame = tk.Frame(self.master, bg='white')
        self.create_frame.pack(fill='both', expand=1)
        self.new_button = tk.Button(self.create_frame, text='Wczytaj z pliku...', command=self.open_file)
        self.new_button.pack(pady=30)
        self.read_button = tk.Button(self.create_frame, text='Stwórz ręcznie',
                                     command=lambda: edit_students.editStudents(self.master))
        self.read_button.pack()

    # wyświetlenie wyników analizy
    def print_result(self):

        self.master.geometry('600x500+200+200')
        self.analysis_frame.pack_forget()

        self.results_frame = tk.Frame(self.master, bg='white')
        self.results_frame.pack(fill='both', expand=1)

        text_box = tk.Text(self.results_frame, height=15, width=52)

        self.result = f'{"=" * 52}\n\t\t  UZYSKANE WYNIKI\n{"=" * 52}\n'
        self.result += '* NAJLEPSZY TEST:\n'
        self.result += database_analysis.highest_score_test(3)
        self.result += f'\n{"+" * 52}\n'
        self.result += '\n* NAJLEPSZY WYNIK OGÓLNY:\n'
        self.result += database_analysis.highest_score_total(3)

        text_box.insert(tk.END, self.result)
        text_box.config(state='disabled')
        text_box.pack()

    def open_exst_base(self):
        self.ex_database_path = filedialog.askopenfilename(filetypes=[("Database file", "*.db")])

        if self.ex_database_path is not None:
            database_analysis.set_db_name(self.ex_database_path)
            self.start_analysis(True)
        else:
            return

    # wybór po załadowaniu bazy
    def start_analysis(self, n):
        if n is True:
            self.welcome_frame.pack_forget()
        else:
            self.create_frame.pack_forget()

        self.analysis_frame = tk.Frame(self.master, bg='white')
        self.analysis_frame.pack(fill='both', expand=1)

        self.start_button = tk.Button(self.analysis_frame, text='Rozpocznij analizę', command=self.ask_team).pack(
            pady=30)
        self.insert_button = tk.Button(self.analysis_frame, text='Edytuj bazę', command=self.edit_base).pack(pady=10)

    def ask_team(self):
        mbox = messagebox.askquestion('Wybór zespółów',
                                      'Czy chcesz wylosować zespoły?\n(Użyj tej opcji jeśli utworzyłeś nową bazę lub zmodyfikowałeś istniejącą)')
        if mbox == 'yes':

            top = tk.Toplevel(self.master)

            def set_teams():

                points_dict = {}

                for key, entry in enumerate(top_entries):
                    points_dict[key + 1] = int(entry.get())

                create_database.set_teams(5)
                create_database.set_team_points(points_dict)

                top.destroy()
                self.print_result()

            top.geometry('150x150')
            top.title('Wybór zespołów')
            top.resizable(False, False)
            # top_frame = tk.Frame(top, bg='white').pack(fill='both', expand=1)
            top_entries = [tk.Entry(top, width=5) for _ in range(5)]

            for n, entry in enumerate(top_entries):
                tk.Label(top, text=f'Zespół {n + 1}').grid(padx=10, column=0, row=n)
                entry.grid(padx=5, column=1, row=n)

            accept_button = tk.Button(top, text='Zatwierdź', command=set_teams)
            accept_button.grid(column=0, row=5, columnspan=2)

        else:
            self.print_result()

    def edit_base(self):
        records = create_database.return_database(self.ex_database_path)
        edit_students.editStudents(self.master, records)

    # Otwieranie bazy danych z pliku txt z podanej lokalizacji
    def open_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Plik tekstowy", "*.txt")])
        if self.filename is not None:
            create_database.create_from_txt(self.filename)
            messagebox.showinfo(title='Komunikat', message='Utworzono bazę danych!')
            self.start_analysis(False)
        else:
            return


# Uruchomienie programu
if __name__ == "__main__":
    root = tk.Tk()
    app = mainWindow(root)

    root.mainloop()
