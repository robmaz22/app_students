import sqlite3
import csv
import os


def advanced(path='../students.db', mode=1):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    results = []
    if mode == 1:
        query = 'sex'
    else:
        query = 'city'

    cursor.execute(f'''SELECT
                    COUNT(id)
                    FROM
                    STUDENTS''')

    results.append(cursor.fetchall())

    cursor.execute(f'''SELECT {query},
                    COUNT(*)
                    AS
                    `number`
                    FROM
                    STUDENTS
                    GROUP
                    BY
                    {query}''')

    results.append(cursor.fetchall())


    cursor.execute(f'''SELECT {query},
                    AVG(test)
                    AS
                    `test`
                    FROM
                    STUDENTS
                    GROUP
                    BY
                    {query}''')

    records = [(x, round(y, 2)) for x,y in cursor.fetchall()]
    results.append(records)

    cursor.execute(f'''SELECT {query},
                    AVG(work)
                    AS
                    `work`
                    FROM
                    STUDENTS
                    GROUP
                    BY
                    {query}''')

    records = [(x, round(y, 2)) for x,y in cursor.fetchall()]
    results.append(records)

    cursor.execute(f'''SELECT {query},
                    AVG(test + work)
                    AS
                    `total`
                    FROM
                    STUDENTS
                    GROUP
                    BY
                    {query}''')

    records = [(x, round(y, 2)) for x,y in cursor.fetchall()]
    results.append(records)

    if query == 'sex':
        for records in results:
            for idx, items in enumerate(records):
                if len(items) == 1:
                    continue
                elif items[0] == 'm':
                    records[idx] = ('Men', items[1])
                else:
                    records[idx] = ('Women', items[1])

    conn.close()
    return results


def best_total(number, path='../students.db'):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    students_info = []

    cursor.execute(F'''SELECT * FROM STUDENTS
        ORDER BY cast(test as int) + cast(work as int) DESC
        LIMIT {number}''')

    for place, student in enumerate(cursor.fetchall()):
        tmp = []
        place = f'*{place + 1} place'
        tmp.append(f'\tFirst Name: {student[2]}')
        tmp.append(f'\tLast Name: {student[3]}')
        tmp.append(f'\tCity: {student[4]}')
        tmp.append(f'\tTest points: {student[5]}')
        tmp.append(f'\tTOTAL: {int(student[5]) + int(student[6])}')
        students_info.append([place, tmp])
    conn.close()
    return students_info


def best_test(number, path='../students.db'):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    students_info = []

    cursor.execute(f'''SELECT * FROM STUDENTS
    ORDER BY cast(test as int) DESC
    LIMIT {number}''')

    for place, student in enumerate(cursor.fetchall()):
        tmp = []
        place = f'*{place + 1} place'
        tmp.append(f'\tFirst Name: {student[2]}')
        tmp.append(f'\tLast Name: {student[3]}')
        tmp.append(f'\tCity: {student[4]}')
        tmp.append(f'\tTest points: {student[5]}')
        students_info.append([place, tmp])
    conn.close()
    return students_info


def save_database(db_file, students_list):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE STUDENTS')
    conn.execute('''CREATE TABLE STUDENTS
    (id, sex, first_name, last_name, city, test, work)''')

    for idx, student in enumerate(students_list):
        info = list(student.save_mode())
        info.insert(0, idx + 1)
        info = tuple(info)
        cursor.execute(f'''INSERT INTO STUDENTS
        (id, sex, first_name, last_name, city, test, work)
        VALUES {info}''')

    print('Database updated successfully!')
    conn.commit()
    conn.close()


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

    conn.commit()
    conn.close()


# def edit(stdscr):
#     flag = False
#     if input('Do you want to create new database?[y/n]\n>>>') == 'y':
#         os.remove('students.db')
#         path = input('File path to new csv file: ')
#         create_from_csv(path)
#         return
#
#     conn = sqlite3.connect('students.db')
#     cursor = conn.cursor()
#     cursor.execute('''SELECT * FROM STUDENTS''')
#     students_list = [generator.Student(info) for info in cursor.fetchall()]
#
#     if input('Do you want to show all students?[y/n]\n>>>') == 'y':
#         for nr, student in enumerate(students_list):
#             print(f'*STUDENT {nr + 1}')
#             print(student)
#
#     while True:
#         print('Student index to edit (Type stop if you finished)')
#         try:
#             index = int(input('>>>')) - 1
#         except ValueError:
#             break
#
#         print('Chosen student:')
#         print(students_list[index])
#         print('Type new information (use commas):')
#         info = input('>>>')
#         students_list[index].edit(info)
#         flag = True
#
#     if flag:
#         generator.save_database(db_file='students.db', students_list=students_list)
#         if input('Do you want to create csv file too?[y/n]') == 'y':
#             generator.save_to_csv(output_file='students.csv', students_list=students_list)
#
#     conn.close()
#
#
# ################################
# def save_database(db_file, students_list):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute('DROP TABLE STUDENTS')
#     conn.execute('''CREATE TABLE STUDENTS
#     (id, sex, first_name, last_name, city, test, work)''')
#
#     for idx, student in enumerate(students_list):
#         info = list(student.save_mode())
#         info.insert(0, idx + 1)
#         info = tuple(info)
#         cursor.execute(f'''INSERT INTO STUDENTS
#         (id, sex, first_name, last_name, city, test, work)
#         VALUES {info}''')
#
#     print('Database updated successfully!')
#     conn.commit()
#     conn.close()

if __name__ == '__main__':
    print(True)
    # print(os.listdir('./'))
    # create_from_csv(path='./students.csv')
    # print(advanced(mode=1))
