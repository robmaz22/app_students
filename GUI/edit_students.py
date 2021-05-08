from tkinter import *
from tkinter import messagebox
from tkinter import  filedialog
from database import create_database


class editStudents(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title('Stwórz bazę')
        self.geometry('705x250')
        self.add_frame = LabelFrame(self, text='Dodaj ucznia', width=190, height=190)
        self.add_frame.grid(column=0, row=0, sticky=N)
        self.list_frame = Frame(self)
        self.list_frame.grid(column=1, row=0)

        self.members = []

        self.scrollbar = Scrollbar(self.list_frame, orient=VERTICAL)
        self.scrollbar.grid(column=5, row=0, sticky=N + S + W, rowspan=7, pady=8)

        self.listbox = Listbox(self.list_frame, width=25, height=13, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.grid(column=3, row=0, columnspan=2, rowspan=7, pady=8)
        self.listbox.bind('<Double-1>', self.show_data)

        self.info = Text(self.list_frame, width=25, height=6, bg='yellow')
        self.info.grid(column=6, row=0, sticky=N, columnspan=2, pady=8)

        self.update_btn = Button(self.list_frame, text='Modyfikuj', command=self.update)
        self.update_btn.grid(column=6, row=1, sticky=N, pady=(4,2), columnspan=2)
        self.delete_btn = Button(self.list_frame, text='Usuń', command=self.del_record)
        self.delete_btn.grid(column=6, row=2, sticky=N, pady=(4,2), columnspan=2)
        self.save_btn = Button(self.list_frame, text='Zapisz bazę', command=self.save_data)
        self.save_btn.grid(column=6, row=3, sticky=N, pady=(4,2), columnspan=2)

        self.entries = [Entry(self.add_frame, width=15) for i in range(6)]
        names = ['Imię', 'Nazwisko', 'Klasa', 'Szkoła', 'Punkty za test', 'Punkty za pracę']

        self.id_value = 1

        id_label = Label(self.add_frame, text='ID').grid(column=0, row=0)

        self.id_entry = Entry(self.add_frame, width=3, justify='center')
        self.id_entry.insert(0, self.id_value)
        self.id_entry.config(state='readonly')
        self.id_entry.grid(row=0, column=1, padx=5)

        for n, entry in enumerate(self.entries):
            Label(self.add_frame, text=f'{names[n]}').grid(padx=10, column=0, row=n + 1)
            entry.grid(padx=5, column=1, row=n + 1)

        self.add_button = Button(self.add_frame, text='Dodaj', command=self.add_student)
        self.add_button.grid(column=0, row=7, columnspan=2,pady=(20,10), padx=40, sticky=W)
        self.clear_button = Button(self.add_frame, text='Wyczyść', command=self.clear_all)
        self.clear_button.grid(column=1, row=7,columnspan=2, pady=(20,10),padx=40, sticky=E)

    def add_student(self, update=False, upd_idx=0):

        student_info = {}
        names = ['name', 'lname', 'class', 'school', 'test', 'work']

        if update is False:
            student_info['id'] = self.id_value
            self.id_value += 1
        else:
            student_info['id'] = upd_idx + 1

        for n, entry in enumerate(self.entries):
            student_info[names[n]] = entry.get()
            entry.delete(0, END)

        if update is False:
            self.members.append(student_info)
        else:
            self.members[int(upd_idx)] = student_info

        members = []

        for id, student in enumerate(self.members):
            members.append(str(id + 1) + '.' + student['name'] + ' ' + student['lname'])

        self.listbox.delete(0, END)

        for n, mem in enumerate(members):
            self.listbox.insert(int(n), mem)

        self.id_entry.config(state='normal')
        self.id_entry.delete(0, END)
        self.id_entry.insert(0, self.id_value)
        self.id_entry.config(state='readonly')

        self.add_button.config(text='Dodaj', command=self.add_student)

    def clear_all(self):
        for entry in self.entries:
            entry.delete(0, END)

    def show_data(self, event):

        cur = self.listbox.curselection()

        id = int(self.listbox.get(cur)[0])

        self.info.delete(1.0, END)

        string = f"""Imię: {self.members[id - 1]['name']}
Nazwisko: {self.members[id - 1]['lname']}
Klasa: {self.members[id - 1]['class']}
Szkoła: {self.members[id - 1]['school']}
Punkty za test: {self.members[id - 1]['test']}
Punkty za pracę: {self.members[id - 1]['work']}"""

        self.info.insert(1.0, string)

    def update(self):
        cur = self.listbox.curselection()

        id = int(self.listbox.get(cur)[0])

        self.id_entry.config(state='normal')
        self.id_entry.delete(0, END)
        self.id_entry.insert(0, self.members[id-1]['id'])
        self.id_entry.config(state='readonly')

        data = []

        for val in self.members[id-1].values():
            data.append(val)

        for entry, val in zip(self.entries, data[1:]):
            entry.delete(0,END)
            entry.insert(0, val)

        self.add_button.config(text='Zamień', command=lambda: self.add_student(update=True, upd_idx = id-1))

    def del_record(self):

        try:
            cur = self.listbox.curselection()

            id = int(self.listbox.get(cur)[0])

            del self.members[id - 1]

            self.listbox.delete(0, END)

            members = []

            for id, student in enumerate(self.members):
                members.append(str(id + 1) + '.' + student['name'] + ' ' + student['lname'])

            for n, mem in enumerate(members):
                self.listbox.insert(int(n), mem)

            self.id_value -= 1
            self.id_entry.config(state='normal')
            self.id_entry.delete(0, END)
            self.id_entry.insert(0, self.id_value)
            self.id_entry.config(state='readonly')
        except:
            messagebox.showerror('Błąd', 'Baza jest pusta!\nNie można usunąć!')

    def save_data(self):
        path = filedialog.asksaveasfilename(title='Zapisz bazę', defaultextension='.db', filetypes=[("Database file", '*.db')])
        create_database.save_database(path, self.members)
        messagebox.showinfo('Sukces', 'Pomyślnie zapisano bazę danych')
        self.destroy()


def main():
    root = Tk()
    app = editStudents(root)

    app.mainloop()


if __name__ == '__main__':
    main()
