import os
import random
import csv
import argparse as ap


class Student:
    info = None

    @classmethod
    def load_info(cls, language):
        info_files = os.path.join('personal_information', language)

        cls.info = {}

        for filename in os.listdir(info_files):
            full_path = os.path.join(info_files, filename)
            with open(full_path, 'r') as file:
                content = [word.rstrip() for word in file.readlines()]
                basename = filename.split('.')[0]
                cls.info[basename] = content

    def __init__(self, info):
        if info:
            self.sex = info[1]
            self.name = info[2]
            self.last_name = info[3]
            self.city = info[4]
            self.test_points = info[5]
            self.work_points = info[6]
        else:
            self.sex = random.choice(['m', 'f'])

            if self.sex == 'm':
                self.name = random.choice(self.info['male_names'])
            else:
                self.name = random.choice(self.info['female_names'])

            self.last_name = random.choice(self.info['last_names'])
            self.city = random.choice(self.info['cities'])
            self.test_points = random.randint(1, 50)
            self.work_points = random.randint(1, 50)

    def __str__(self):
        self._student_info = (f'Sex: {self.sex}\n'
                              f'First Name: {self.name}\n'
                              f'Last Name: {self.last_name}\n'
                              f'City: {self.city}\n'
                              f'Test Points: {self.test_points}\n'
                              f'Work Points: {self.work_points}\n')
        return self._student_info

    def edit(self, new_info):
        if isinstance(new_info, str):
            new_info = new_info.split(',')
        self.sex = new_info[0]
        self.name = new_info[1]
        self.last_name = new_info[2]
        self.city = new_info[3]
        self.test_points = new_info[4]
        self.work_points = new_info[5]

    def save_mode(self):
        return self.sex, self.name, self.last_name, self.city, self.test_points, self.work_points


def get_args():
    parser = ap.ArgumentParser(description='Script to generate n student with random personal  information')
    parser.add_argument('-n', '--number', type=int, required=True, help='Number of students to generate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show generated students')
    parser.add_argument('-o', '--output', required=False, default='../students.csv', help='Output path for csv file')
    parser.add_argument('-l', '--language', required=False, default='polish', help='Personal info language')

    return parser.parse_args()


def save_to_csv(output_file, students_list):
    with open(output_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for student in students_list:
            writer.writerow(student.save_mode())

    print(f'File {os.path.basename(output_file)} with {len(students_list)} students saved')


def main():
    args = get_args()
    Student.load_info(args.language)

    students = [Student(info=False) for _ in range(args.number)]

    if args.verbose:
        for i, student in enumerate(students):
            print(f'STUDENT {i + 1}')
            print(student)

    save_to_csv(args.output, students)


if __name__ == '__main__':
    main()
