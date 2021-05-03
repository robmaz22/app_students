import sqlite3


def base_content():
    con = sqlite3.connect('students.db')
    cur = con.cursor()

    cur.execute('''SELECT name, lname FROM students''')
    students_list = cur.fetchall()

    return students_list


def highest_score_test(n=3):
    con = sqlite3.connect('students.db')
    cur = con.cursor()

    cur.execute('''SELECT 
    name, lname, school, test
    FROM students
    ORDER BY test DESC''')

    results = cur.fetchall()

    text = """"""

    for idx in range(n):
        text += str(idx + 1) + ' MIEJSCE:\n'
        text += f'\t{str(results[idx][0])} {str(results[idx][1])} ({str(results[idx][2])})\n\t{str(results[idx][3])} punktów\n'
        text += '-' * 15
        text += '\n'

    con.commit()
    con.close()

    return text

def highest_score_total(n=3):
    con = sqlite3.connect('students.db')
    cur = con.cursor()

    cur.execute('''SELECT 
    name, lname, school, test, work, t_points
    FROM students
    ORDER BY (test + work + t_points) DESC''')

    results = cur.fetchall()

    text = """"""

    for idx in range(n):
        text += str(idx + 1) + ' MIEJSCE:\n'
        total = int(results[idx][3]) + int(results[idx][4]) + int(results[idx][5])

        text += f'\t{str(results[idx][0])} {str(results[idx][1])} ({str(results[idx][2])})\n\t{str(total)} punktów\n'
        text += '-' * 15
        text += '\n'

    con.commit()
    con.close()

    return text
