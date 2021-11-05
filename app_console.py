import os
import sqlite3
import csv
from student_generator import generator


### database functions ##########
def create_from_csv(path):
    conn = sqlite3.connect('students.db')
    conn.execute('''CREATE TABLE STUDENTS 
    (id, sex, first_name, last_name, city, test, work)''')
    cursor = conn.cursor()

    with open(path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for idx, row in enumerate(reader):
            row.insert(0, idx + 1)
            row = tuple(row)
            cursor.execute(f'''INSERT INTO STUDENTS 
            (id, sex, first_name, last_name, city, test, work)
            VALUES {row}''')

    print('Database created successfully!')
    conn.commit()
    conn.close()


def best_test(number):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(F'''SELECT * FROM STUDENTS
    ORDER BY cast(test as int) DESC
    LIMIT {number}''')

    for place, student in enumerate(cursor.fetchall()):
        student_info = f'\t*{place + 1} place:\n'
        student_info += f'\tFirst Name: {student[2]}\n'
        student_info += f'\tLast Name: {student[3]}\n'
        student_info += f'\tCity: {student[4]}\n'
        student_info += f'\tTest points: {student[5]}\n'
        print(student_info)

    conn.close()


def best_total(number):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(F'''SELECT * FROM STUDENTS
    ORDER BY cast(test as int) + cast(work as int) DESC
    LIMIT {number}''')

    for place, student in enumerate(cursor.fetchall()):
        student_info = (f'\t*{place + 1} place:\n'
                        f'\tFirst Name: {student[2]}\n'
                        f'\tLast Name: {student[3]}\n'
                        f'\tCity: {student[4]}\n'
                        f'\tTest points: {student[5]}\n'
                        f'\tWork points: {student[6]}\n'
                        f'\tTOTAL: {int(student[5]) + int(student[6])}\n')
        print(student_info)

    conn.close()


def advanced():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    # number of students
    cursor.execute('''SELECT COUNT(id) FROM STUDENTS''')
    total = cursor.fetchone()[0]
    print(f'Total students number: {total} where,')
    cursor.execute('''SELECT COUNT(id) FROM STUDENTS WHERE sex = "f"''')
    women = cursor.fetchone()[0]
    print(f'* Women: {women} ({(women / total) * 100:.1f}%)')
    cursor.execute('''SELECT COUNT(id) FROM STUDENTS WHERE sex = "m"''')
    men = cursor.fetchone()[0]
    print(f'* Men: {men} ({(men / total) * 100:.1f}%)')
    print()
    # average test
    cursor.execute('''SELECT AVG(test) FROM STUDENTS''')
    print(f'Average test result: {cursor.fetchone()[0]:.1f} where,')
    cursor.execute('''SELECT AVG(test) FROM STUDENTS WHERE sex = "f"''')
    print(f'* Women: {cursor.fetchone()[0]:.1f}')
    cursor.execute('''SELECT AVG(test) FROM STUDENTS WHERE sex = "m"''')
    print(f'* Men: {cursor.fetchone()[0]:.1f}')
    print()
    # average work
    cursor.execute('''SELECT AVG(work) FROM STUDENTS''')
    print(f'Average work result: {cursor.fetchone()[0]:.1f} where,')
    cursor.execute('''SELECT AVG(work) FROM STUDENTS WHERE sex = "f"''')
    print(f'* Women: {cursor.fetchone()[0]:.1f}')
    cursor.execute('''SELECT AVG(work) FROM STUDENTS WHERE sex = "m"''')
    print(f'* Men: {cursor.fetchone()[0]:.1f}')

    conn.close()


def edit():
    flag = False
    if input('Do you want to create new database?[y/n]\n>>>') == 'y':
        os.remove('students.db')
        path = input('File path to new csv file: ')
        create_from_csv(path)
        return

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM STUDENTS''')
    students_list = [generator.Student(info) for info in cursor.fetchall()]

    if input('Do you want to show all students?[y/n]\n>>>') == 'y':
        for nr, student in enumerate(students_list):
            print(f'*STUDENT {nr + 1}')
            print(student)

    while True:
        print('Student index to edit (Type stop if you finished)')
        try:
            index = int(input('>>>')) - 1
        except ValueError:
            break

        print('Chosen student:')
        print(students_list[index])
        print('Type new information (use commas):')
        info = input('>>>')
        students_list[index].edit(info)
        flag = True

    if flag:
        generator.save_database(db_file='students.db', students_list=students_list)
        if input('Do you want to create csv file too?[y/n]') == 'y':
            generator.save_to_csv(output_file='students.csv', students_list=students_list)

    conn.close()


################################


def run():
    if not os.path.exists('students.db'):
        print('No database file. Do you want to create it?[y/n]')
        answer = input('>>>')
        if answer.lower() == 'y':
            path = input('File path: ')
            create_from_csv(path)

    print('How many places to show?')
    how_many = int(input('>>>'))

    result_dict = {'TEST WINNERS:': best_test,
                   'TOTAL WINNERS:': best_total}

    for key, func in result_dict.items():
        print(key)
        func(how_many)

    print('Do you want to start more advanced analysis?[y/n]')
    answer = input('>>>')
    if answer.lower() == 'y':
        advanced()


def main():
    print('What do you want to do?')
    print('1. Start analysis')
    print('2. Edit students')
    print('3. Exit')
    answer = input('>>>')

    if answer == '1':
        run()
    elif answer == '2':
        edit()
        run()
    elif answer == '3':
        exit()
    else:
        print('Wrong value')


if __name__ == '__main__':
    main()
