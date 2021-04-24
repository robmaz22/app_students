import random

# listy z imionami i nazwiskami
female_n = ["Agata", "Agnieszka", "Aleksandra", "Alicja", "Amanda", "Amelia",
            "Anastazja", "Andżelika", "Aneta", "Anita", "Anna", "Antonia",
            "Barbara", "Bernadeta", "Bożena", "Dagmara", "Danuta", "Daria",
            "Diana", "Dominika", "Dorota", "Edyta", "Eliza", "Emilia", "Ewa",
            "Ewelina", "Gabriela", "Ilona", "Iwona", "Izabela", "Jagoda",
            "Joanna", "Jolanta", "Julia", "Justyna", "Kaja", "Karina", "Karolina",
            "Katarzyna", "Kinga", "Klaudia", "Magdalena", "Maja", "Małgorzata", "Maria",
            "Mariola", "Martyna", "Marzena", "Monika", "Nadia", "Natalia", "Olga", "Oliwia",
            "Patrycja", "Paula", "Paulina", "Roksana", "Róża", "Sabina", "Sandra", "Sara", "Sylwia",
            "Teresa", "Urszula", "Weronika", "Wiktoria", "Wioleta", "Zuzanna", "Zyta", "Żaneta"]
male_n = ["Adam", "Albert", "Aleks", "Aleksander", "Andrzej", "Arkadiusz", "Artur", "Bartosz", "Błażej",
          "Damian", "Daniel", "Dariusz", "Dawid", "Dominik", "Fabian", "Filip", "Gerard", "Grzegorz",
          "Hubert", "Igor", "Jacek", "Jakub", "Jan", "Julian", "Kacper", "Kamil", "Karol", "Kornel",
          "Krystian", "Krzysztof", "Łukasz", "Maciej", "Maksymilian", "Mariusz", "Marcin", "Marek", "Mateusz",
          "Michał", "Miłosz", "Mikołaj", "Nikodem", "Norbert", "Oskar", "Patryk", "Paweł", "Piotr", "Przemysław",
          "Rafał", "Robert", "Sebastian", "Sławomir", "Szymon", "Tomasz", "Tymoteusz", "Wiktor", "Wojciech"]
lnames = ["Nowak", "Kowalski", "Wiśniewski", "Wójcik", "Kowalczyk", "Kamiński", "Lewandowski", "Zieliński",
          "Szymański", "Woźniak", "Dąbrowski", "Kozłowski", "Jankowski", "Mazur", "Wojciechowski", "Kwiatkowski",
          "Krawczyk", "Kaczmarek", "Piotrowski", "Grabowski"]
schools = ["Kraków", "Poznań", "Rzeszów", "Warszawa", "Kielce", "Toruń", "Białystok", "Opole", "Katowice",
           "Szczecin", "Jelenia Góra"]

fname = 'students.txt'
sex = 1
print('Ile uczniów?')
number = int(input('>>>'))
nr = 1
print("Czy wyświetlać dane?[T/n]")
option = input(">>>")

with open(fname, 'w') as file:
    for i in range(number):
        sex = random.randint(1, 2)

        if sex == 1:
            lname = random.choice(lnames)
            if lname.endswith('i'):
                tmp = list(lname)
                tmp[-1] = 'a'
                lname = ''.join(tmp)
            student = f'{random.choice(female_n)},{lname},{random.randint(1, 7)},{random.choice(schools)},{random.randint(10, 50)},{random.randint(10, 50)}\n'
        else:
            student = f'{random.choice(male_n)},{random.choice(lnames)},{random.randint(1, 7)},{random.choice(schools)},{random.randint(10, 50)},{random.randint(10, 50)}\n'

        file.write(student)

if option == 'T' or option == 't':
    nr = 1

    with open(fname, 'r') as file:
        content = file.readlines()

    for student in content:
        line = student.replace('\n', '').split(',')
        print('Uczeń nr', nr)
        print(
            f'\tImię: {line[0]}\n\tNazwisko: {line[1]}\n\tKlasa: {line[2]}\n\tSzkoła: {line[3]}\n\tTest: {line[4]}\n\tPraca: {line[5]}\n')
        nr += 1

print('Zakończono')
