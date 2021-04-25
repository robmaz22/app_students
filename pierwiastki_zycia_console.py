import os
from database import create_database


def make_analysis():
    if not os.path.exists('pierwiastki_zycia.db'):
        create_database.create_from_txt('students.txt')

    print('Ile miejsc?')
    n = int(input('>>> '))

    print('='*16)
    print('UZYSKANE WYNIKI:')
    print('=' * 16)
    print()
    print('* NAJLEPSZY TEST:')
    create_database.highest_score_test(n)
    print()
    print('* NAJLEPSZY WYNIK OGÓLNY:')
    create_database.highest_score_total(n)


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
