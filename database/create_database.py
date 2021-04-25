import sqlite3


def create_from_txt(path_to_txt):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE students
                   (name, sname, class, school, test, work)''')

    with open(path_to_txt) as file:
        content = file.readlines()
        for line in content:
            info = line.replace('\n', '').split(',')
            cur.execute(f"INSERT INTO students VALUES {tuple(info)}")

    con.commit()
    con.close()

