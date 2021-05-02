import os
from database.create_database import *
from database.database_analysis import *


def edit_students():
    if not os.path.exists('pierwiastki_zycia.db'):
        print('Baza danych jest pusta nie można edytować!')
        return

    student_list = base_content()
    print('LISTA UCZNIÓW:')

    for id, info in enumerate(student_list):
        print(f'{id + 1}. {info[0]} {info[1]}')

    while True:
        print('Wybierz indeks, który chcesz edytować (Aby zatrzymać wpisz stop):')
        idx = input('>>> ')

        if idx == 'stop':
            break

        edit_record(int(idx))


def make_analysis():
    if not os.path.exists('students.db'):
        create_from_txt('students.txt')
        print('Podaj liczbę zespołów:')
        groups = int(input('>>> '))
        set_teams(groups)

        points = {}

        for group in range(groups):
            print(f'Podaj ilość punktów dla zespołu {group + 1}:')
            pts = int(input('>>>'))
            points[group + 1] = pts

        set_team_points(points)

    print('[INFO] ROZPOCZĘCIE ANALIZY...')
    print('Ile miejsc wyświetlić?')
    n = int(input('>>> '))

    print('=' * 16)
    print('UZYSKANE WYNIKI:')
    print('=' * 16)
    print()
    print('* NAJLEPSZY TEST:')
    highest_score_test(n)
    print()
    print('* NAJLEPSZY WYNIK OGÓLNY:')
    highest_score_total(n)


print('WITAJ W PROGRAMIE DO ANALIZY DANYCH!')
print('WYBIERZ OPCJĘ:\n1. Rozpocznij analizę\n2. Edytuj bazę danych\n3. Zakończ')
option = input('>>> ')

if int(option) == 1:
    make_analysis()
elif int(option) == 2:
    edit_students()
elif int(option) == 3:
    exit(0)
else:
    print('Niepoprawna wartość')
