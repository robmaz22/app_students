import tkinter as tk

def create_new():
    welcome_frame.pack_forget()
    create_frame = tk.Frame(root, bg='yellow')
    create_frame.pack(fill='both', expand=1)
    new_button = tk.Button(create_frame, text='Wczytaj z pliku...')
    new_button.pack(pady=30)
    read_button =tk.Button(create_frame, text='Stwórz ręcznie')
    read_button.pack()

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

welcome_frame = tk.Frame(root, bg='yellow')
welcome_frame.pack()
title_label = tk.Label(welcome_frame, text="WITAJ W PROGRAMIE DO ANALIZY DANYCH", bg='green')
title_label.config(font=("Cantarell 13 bold"))
title_label.pack(pady=15, padx=20)
create_button = tk.Button(welcome_frame, text='Utwórz nową bazę danych', command=create_new)
create_button.pack(pady=5)
open_button = tk.Button(welcome_frame, text='Otwórz istniejącą bazę danych')
open_button.pack(pady=5)


root.mainloop()