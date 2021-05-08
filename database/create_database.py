import sqlite3
import random


def create_from_txt(path_to_txt):
    con = sqlite3.connect('students.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE students
                   (id, name, lname, class, school, test, work)''')

    with open(path_to_txt) as file:
        content = file.readlines()
        for student_id, line in enumerate(content):
            info = line.replace('\n', '').split(',')
            info.insert(0, str(student_id))
            cur.execute(f"INSERT INTO students VALUES {tuple(info)}")

    con.commit()
    con.close()

def save_database(path, member_list):
    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute('''CREATE TABLE students
                       (id, name, lname, class, school, test, work)''')

    for member in member_list:
        cur.execute(f"INSERT INTO students VALUES {tuple(member.values())}")

    con.commit()
    con.close()

def set_teams(n=5):
    con = sqlite3.connect('students.db')
    cur = con.cursor()

    cur.execute('''SELECT COUNT(name) FROM students''')
    total = cur.fetchone()
    members = total[0] // n
    print(f'Sugerowana liczba członków: {members}')

    teams = []

    for team in range(n):
        counter = members
        while counter > 0:
            teams.append(team + 1)
            counter -= 1

    random.shuffle(teams)

    cur.execute(f'''ALTER TABLE students ADD team INT''')

    for id, team in enumerate(teams):
        cur.execute(f'''UPDATE students
                        SET team = "{team}"
                        WHERE id = "{id}"''')

    con.commit()
    con.close()


def set_team_points(points_dict):
    con = sqlite3.connect('students.db')
    cur = con.cursor()

    cur.execute(f'''ALTER TABLE students ADD t_points INT''')

    for group, pts in points_dict.items():
        cur.execute(f'''UPDATE students
                        SET t_points = "{pts}"
                        WHERE team = {group}''')

    con.commit()
    con.close()


def edit_record(idx):
    con = sqlite3.connect('students.db')
    cur = con.cursor()

    cur.execute(f'''SELECT * FROM students WHERE id == "{idx-1}"''')
    info = cur.fetchone()

    print('WYBRANY REKORD:')
    print(f'''* Imię: {info[1]}
* Nazwisko: {info[2]}
* Klasa: {info[3]}
* Szkoła: {info[4]}
* Punkty test: {info[5]}
* Punkty praca: {info[6]}
* Zespół: {info[7]}
* Punkty dla zespołu: {info[8]}''')

    print('Podaj nowe wartości (imię nazwisko klasa szkoła punkty_test punty_praca zespół punkty_zespołu):')
    new_student = input('>>> ')
    record = new_student.split(' ')

    cur.execute(f'''UPDATE students
SET name = "{record[0]}",
lname = "{record[1]}",
class = "{record[2]}",
school = "{record[3]}",
test = "{record[4]}",
work = "{record[5]}",
team = "{record[6]}",
t_points = "{record[7]}"
WHERE id = "{idx-1}"''')

    cur.execute(f'''SELECT * FROM students WHERE id == "{idx - 1}"''')
    info = cur.fetchone()

    print('UTWORZONY REKORD:')
    print(f'''* Imię: {info[1]}
* Nazwisko: {info[2]}
* Klasa: {info[3]}
* Szkoła: {info[4]}
* Punkty test: {info[5]}
* Punkty praca: {info[6]}
* Zespół: {info[7]}
* Punkty dla zespołu: {info[8]}''')

    con.commit()
    con.close()
