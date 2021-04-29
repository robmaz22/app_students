import sqlite3
import random


def create_from_txt(path_to_txt):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE students
                   (id, name, sname, class, school, test, work)''')

    with open(path_to_txt) as file:
        content = file.readlines()
        for id, line in enumerate(content):
            info = line.replace('\n', '').split(',')
            info.insert(0, id)
            cur.execute(f"INSERT INTO students VALUES {tuple(info)}")

    con.commit()
    con.close()


def set_teams(n=5):
    con = sqlite3.connect('pierwiastki_zycia.db')
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
                        SET team = {team}
                        WHERE id = {id}''')

    con.commit()
    con.close()


def set_team_points(points_dict):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute(f'''ALTER TABLE students ADD t_points INT''')

    for group, pts in points_dict.items():
        cur.execute(f'''UPDATE students
                        SET t_points = {pts}
                        WHERE team = {group}''')

    con.commit()
    con.close()
