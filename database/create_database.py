import sqlite3


def create_from_txt(path_to_txt):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE students
                   (name, sname, class, school, test, work)''')

    with open(path_to_txt) as file:
        content = file.readlines()
        for line in content:
            info = line.replace('\n', '').split(',')
            cur.execute(f"INSERT INTO students VALUES {tuple(info)}")

    con.commit()
    con.close()

def highest_score_test(n=3):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute('''SELECT 
    name, sname, school, test
    FROM students
    ORDER BY test DESC''')

    results = cur.fetchall()

    for idx in range(n):
        print(idx+1, 'MIEJSCE:')
        print(f'{results[idx][0]} {results[idx][1]} ({results[idx][2]})\n{results[idx][3]} punktów')
        print('-'*15)

    con.commit()
    con.close()

def highest_score_total(n=3):
    con = sqlite3.connect('pierwiastki_zycia.db')
    cur = con.cursor()

    cur.execute('''SELECT 
    name, sname, school, test, work
    FROM students
    ORDER BY (test + work) DESC''')

    results = cur.fetchall()

    for idx in range(n):
        print(idx+1, 'MIEJSCE:')
        total = int(results[idx][3]) + int(results[idx][4])

        print(f'{results[idx][0]} {results[idx][1]} ({results[idx][2]})\n{total} punktów')
        print('-'*15)

    con.commit()
    con.close()
