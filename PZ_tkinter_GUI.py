import tkinter as tk


window = tk.Tk()
window.title('Pierwiastk życia')
window.geometry('440x170')

title_label = tk.Label(text="WITAJ W PROGRAMIE PIERWIASTKI ŻYCIA")
title_label.config(font=("Cantarell 15 bold"))
title_label.pack(pady=15, padx=20)

create_button = tk.Button(text='Utwórz nową bazę danych', )
create_button.pack(pady=5)
open_button = tk.Button(text='Otwórz istniejącą bazę danych')
open_button.pack(pady=5)

menu_bar = tk.Menu(window)
option_menu = tk.Menu(menu_bar, tearoff=0)
option_menu.add_command(label="Ustawienia")
menu_bar.add_cascade(label="Opcje", menu=option_menu)

helpmenu = tk.Menu(menu_bar, tearoff=0)
helpmenu.add_command(label="Jak korzystać?")
helpmenu.add_command(label="O programie...")
menu_bar.add_cascade(label="Pomoc", menu=helpmenu)

window.config(menu=menu_bar)


window.mainloop()