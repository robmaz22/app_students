import sqlite3
from student_generator import generator


class Test:
    def __init__(self):
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM STUDENTS''')
        self.students_list = [generator.Student(
            info) for info in cursor.fetchall()]
        conn.close()

        self.current = 0

    def edit_student(self, new=True):
        selected = self.current
        is_new = new
        is_modified = False

        print('=====================PREVIEW====================')
        print(f'Sex: -\nFirst Name: -\nLast Name: -\nCity: -\nTest Points: -\nWork Points: -\n')
        print('================================================')

        choice = input('>>>')
        
        if choice == 'stop' and is_modified:
            print('Do you want to save? if not type clear')
            choice = input('>>>')
            if choice == 'clear':
                return
            print('Saved')
        elif choice == 'enter':
            pass
        else:
            return
            
        
    # def edit_student(self, new=True):
    #         # self.stdscr.erase()
    #         selected = self.current - 1
    #         is_new = new
    #         is_modified = False
    #         while True:
    #             self.stdscr.erase()
    #             self.stdscr.addstr(
    #                 0, 0, '=====================PREVIEW====================', curses.color_pair(1))
    #             if is_new:
    #                 self.stdscr.addstr(1, 0, str(f'Sex: -\n'
    #                                             f'First Name: -\n'
    #                                             f'Last Name: -\n'
    #                                             f'City: -\n'
    #                                             f'Test Points: -\n'
    #                                             f'Work Points: -\n'))
    #             else:
    #                 self.stdscr.addstr(
    #                     1, 0, str(self.students_list[selected].__str__()))
    #             self.stdscr.addstr(
    #                 7, 0, '================================================', curses.color_pair(1))
    #             self.stdscr.addstr(
    #                 9, 0, 'To edit press enter to return press ESC', curses.color_pair(3))

    #             curses.noecho()
    #             curses.curs_set(0)

    #             ch = self.stdscr.getch()
    #             if ch == curses.ascii.ESC:
    #                 if is_modified:
    #                     self.stdscr.erase()
    #                     self.stdscr.addstr(
    #                         0, 0, str(self.students_list[selected].__str__()))
    #                     self.stdscr.addstr(self.max_lines, 0, 'To save press s or any other key to discard',
    #                                     curses.color_pair(3))
    #                     ch = self.stdscr.getch()
    #                     if ch == 115:

    #                         if new_sex is not None:
    #                             if is_new:
    #                                 new_info = [None,
    #                                             new_sex,
    #                                             new_name,
    #                                             new_last_name,
    #                                             new_city,
    #                                             new_test_points,
    #                                             new_work_points]

    #                 self.students_list.append(generator.Student(new_info))
    #                 self.load_properties()
    #                 selected = len(self.items) - 1
    #                 is_new = False
    #                 else:
    #                     self.students_list[selected].sex = new_sex
    #                     self.students_list[selected].name = new_name
    #                     self.students_list[selected].last_name = new_last_name
    #                     self.students_list[selected].city = new_city
    #                     self.students_list[selected].test_points = new_test_points
    #                     self.students_list[selected].work_points = new_work_points

    #                     self.load_properties()
    #             else:
    #                 break

    #             curses.echo()
    #             curses.curs_set(1)

    #             self.stdscr.addstr(10, 0, 'Sex: ')
    #             self.stdscr.addstr(11, 0, 'First name: ')
    #             self.stdscr.addstr(12, 0, 'Last name: ')
    #             self.stdscr.addstr(13, 0, 'City: ')
    #             self.stdscr.addstr(14, 0, 'Test points: ')
    #             self.stdscr.addstr(15, 0, 'Work points: ')

    #             new_sex = self.stdscr.getstr(10, 5, 30).decode("utf-8")
    #             new_name = self.stdscr.getstr(11, 12, 30).decode("utf-8")
    #             new_last_name = self.stdscr.getstr(12, 11, 30).decode("utf-8")
    #             new_city = self.stdscr.getstr(13, 6, 30).decode("utf-8")
    #             new_test_points = self.stdscr.getstr(14, 13, 30).decode("utf-8")
    #             new_work_points = self.stdscr.getstr(15, 13, 30).decode("utf-8")
    #             is_modified = True

    #             self.stdscr.refresh()

test = Test()
test.edit_student()