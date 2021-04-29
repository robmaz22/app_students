import os
from database.create_database import create_from_txt, set_teams, set_team_points
from database import database_analysis


def make_analysis():
    if not os.path.exists('pierwiastki_zycia.db'):
        create_from_txt('students.txt')
        print('Podaj liczbę zespołów:')
        groups = int(input('>>> '))
        set_teams(groups)

        points = {}

        for group in range(groups):
            print(f'Podaj ilość punktów dla zespołu {group+1}:')
            pts = int(input('>>>'))
            points[group+1] = pts

        set_team_points(points)

    print('[INFO] ROZPOCZĘCIE ANALIZY...')
    print('Ile miejsc wyświetlić?')
    n = int(input('>>> '))

    print('=' * 16)
    print('UZYSKANE WYNIKI:')
    print('=' * 16)
    print()
    print('* NAJLEPSZY TEST:')
    database_analysis.highest_score_test(n)
    print()
    print('* NAJLEPSZY WYNIK OGÓLNY:')
    database_analysis.highest_score_total(n)


print('WITAJ W PROGRAMIE PIERWIASTKI ŻYCIA!')
print('WYBIERZ OPCJĘ:\n1. Rozpocznij analizę\n2. Edytuj bazę danych\n3. Zakończ')
option = input('>>> ')

if int(option) == 1:
    make_analysis()
elif int(option) == 2:
    pass
elif int(option) == 3:
    exit(0)
else:
    print('Niepoprawna wartość')
