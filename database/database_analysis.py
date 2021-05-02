import sqlite3


def base_content():
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute('''SELECT name, lname FROM students''')
    students_list = cur.fetchall()

    return students_list


def highest_score_test(n=3):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute('''SELECT 
    name, lname, school, test
    FROM students
    ORDER BY test DESC''')

    results = cur.fetchall()

    for idx in range(n):
        print(idx + 1, 'MIEJSCE:')
        print(f'\t{results[idx][0]} {results[idx][1]} ({results[idx][2]})\n\t{results[idx][3]} punktów')
        print('-' * 15)

    con.commit()
    con.close()


def highest_score_total(n=3):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute('''SELECT 
    name, lname, school, test, work, t_points
    FROM students
    ORDER BY (test + work + t_points) DESC''')

    results = cur.fetchall()

    for idx in range(n):
        print(idx + 1, 'MIEJSCE:')
        total = int(results[idx][3]) + int(results[idx][4]) + int(results[idx][5])

        print(f'\t{results[idx][0]} {results[idx][1]} ({results[idx][2]})\n\t{total} punktów')
        print('-' * 15)

    con.commit()
    con.close()
