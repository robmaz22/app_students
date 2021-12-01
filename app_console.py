import curses
import curses.textpad
import os
import sqlite3
from curses import wrapper

from database_operations import operations
from student_generator import generator


# Classes Based on https://github.com/mingrammer/python-curses-scroll-example
class ResultScreen:
    UP = -1
    DOWN = 1

    def __init__(self, items, stdscr):
        self.stdscr = stdscr
        self.items = items
        self.skip_lines = len(self.items[0][1]) + 1
        self.max_lines = (curses.LINES // self.skip_lines) - 2
        self.top = 0
        self.bottom = len(self.items) - 1
        self.current = 0
        self.page = self.bottom // self.max_lines

    def run(self):
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def input_stream(self):
        while True:
            self.display()

            ch = self.stdscr.getch()
            if ch == curses.KEY_UP:
                self.paging(self.UP)
            elif ch == curses.KEY_DOWN:
                self.paging(self.DOWN)
            elif ch == ord(' '):
                break

    def paging(self, direction):

        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction

        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        if (direction == self.UP) and (current_page >= 0):
            self.top = max(0, self.top - self.max_lines)
            return

        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        self.stdscr.erase()
        main_counter = 0
        sub_counter = main_counter + 1
        for items in self.items[self.top:self.top + self.max_lines]:
            self.stdscr.addstr(main_counter, 0, items[0], curses.color_pair(2))
            for line in items[1]:
                self.stdscr.addstr(sub_counter, 0, line)
                sub_counter += 1
            main_counter += self.skip_lines
            sub_counter = main_counter + 1
        self.stdscr.addstr(curses.LINES - 1, 0,
                           '(↑) and (↓) arrows to navigate (Space to return)',
                           curses.color_pair(3))
        self.stdscr.refresh()


class EditScreen:
    @classmethod
    def load_students_list(cls):
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM STUDENTS''')
        cls.students_list = [generator.Student(
            info) for info in cursor.fetchall()]
        conn.close()

    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.UP = -1
        self.DOWN = 1

        self.init_curses()
        self.load_students_list()

        self.max_lines = curses.LINES - 1
        self.load_properties()

    def load_properties(self):
        self.items = [f'{i + 1}. {getattr(info, "name")} {getattr(info, "last_name")}' for i, info in
                      enumerate(self.students_list)]
        self.items.insert(0, 'STUDENT LIST')
        self.top = 0
        self.bottom = len(self.items)
        self.current = 0
        self.page = self.bottom // self.max_lines

    def init_curses(self):
        curses.noecho()
        curses.cbreak()

        curses.start_color()

        self.current = curses.color_pair(1)

    def run(self):
        try:
            self.input_stream()
        except KeyboardInterrupt:
            pass
        finally:
            curses.endwin()

    def input_stream(self):
        while True:
            self.display()

            ch = self.stdscr.getch()
            if ch == curses.KEY_UP:
                self.scroll(self.UP)
            elif ch == curses.KEY_DOWN:
                self.scroll(self.DOWN)
            elif ch == curses.KEY_LEFT:
                self.paging(self.UP)
            elif ch == curses.KEY_RIGHT:
                self.paging(self.DOWN)
            elif ch == curses.KEY_BACKSPACE:
                self.delete_student()
            elif ch == 101:
                if not self.current == 0:
                    self.edit_student(new=False)
            elif ch == 110:
                self.edit_student()
            elif ch == 115:
                operations.save_database(
                    db_file='students.db', students_list=self.items[1:])
                generator.save_to_csv(
                    output_file='students.csv', students_list=self.items[1:])
                self.stdscr.erase()
                self.stdscr.addstr(0, 0, 'Database saved! Press any key',
                                   curses.color_pair(3))
                self.stdscr.getch()
                break
            elif ch == curses.ascii.ESC:
                break

    def scroll(self, direction):
        next_line = self.current + direction

        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return

        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return

        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return

        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return

    def paging(self, direction):
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)

        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return

        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return

    def display(self):
        self.stdscr.erase()
        self.stdscr.addstr(self.max_lines, 0,
                           'Press e to edit, BACKSPACE to delete, s to save, ESC to exit',
                           curses.color_pair(3))
        for idx, item in enumerate(self.items[self.top:self.top + self.max_lines]):
            if idx == self.current:
                self.stdscr.addstr(idx, 0, item, curses.color_pair(1))
            else:
                self.stdscr.addstr(idx, 0, item, curses.color_pair(2))
        self.stdscr.refresh()

    def edit_student(self, new=True):
        self.stdscr.erase()

        selected = self.current - 1
        is_new = new
        is_modified = False

        while True:
            self.stdscr.erase()
            self.stdscr.addstr(0, 0,
                               '=====================PREVIEW====================',
                               curses.color_pair(1))

            if is_new:
                self.stdscr.addstr(1, 0, str(f'Sex: -\n'
                                             f'First Name: -\n'
                                             f'Last Name: -\n'
                                             f'City: -\n'
                                             f'Test Points: -\n'
                                             f'Work Points: -\n'))
            elif is_modified:
                self.stdscr.addstr(1, 0, str(f'Sex: {new_sex}\n'
                                             f'First Name: {new_name}\n'
                                             f'Last Name: {new_last_name}\n'
                                             f'City: {new_city}\n'
                                             f'Test Points: {new_test_points}\n'
                                             f'Work Points: {new_work_points}\n'))
            else:
                self.stdscr.addstr(
                    1, 0, str(self.students_list[selected].__str__()))

            self.stdscr.addstr(7, 0,
                               '================================================',
                               curses.color_pair(1))
            self.stdscr.addstr(9, 0,
                               'To edit press enter to return press ESC',
                               curses.color_pair(3))

            curses.noecho()
            curses.curs_set(0)

            ch = self.stdscr.getch()

            if ch == curses.ascii.ESC:
                if not is_modified:
                    break

                self.stdscr.erase()
                self.stdscr.addstr(
                    0, 0, 'TEMPORARY INFORMATION:', curses.color_pair(1))
                self.stdscr.addstr(1, 0,
                                   str(f'Sex: {new_sex}\n'
                                       f'First Name: {new_name}\n'
                                       f'Last Name: {new_last_name}\n'
                                       f'City: {new_city}\n'
                                       f'Test Points: {new_test_points}\n'
                                       f'Work Points: {new_work_points}\n'))
                self.stdscr.addstr(self.max_lines, 0,
                                   'To save press s or any other key to discard',
                                   curses.color_pair(3))
                ch = self.stdscr.getch()
                if ch == 115:
                    if is_new:
                        new_info = [None,
                                    new_sex,
                                    new_name,
                                    new_last_name,
                                    new_city,
                                    new_test_points,
                                    new_work_points]

                        self.students_list.append(generator.Student(new_info))
                    else:
                        self.students_list[selected].sex = new_sex
                        self.students_list[selected].name = new_name
                        self.students_list[selected].last_name = new_last_name
                        self.students_list[selected].city = new_city
                        self.students_list[selected].test_points = new_test_points
                        self.students_list[selected].work_points = new_work_points

                    self.load_properties()
                break
            else:
                curses.echo()
                curses.curs_set(1)

                self.stdscr.addstr(10, 0, 'Sex: ')
                self.stdscr.addstr(11, 0, 'First name: ')
                self.stdscr.addstr(12, 0, 'Last name: ')
                self.stdscr.addstr(13, 0, 'City: ')
                self.stdscr.addstr(14, 0, 'Test points: ')
                self.stdscr.addstr(15, 0, 'Work points: ')

                new_sex = self.stdscr.getstr(10, 5, 30).decode("utf-8")
                new_name = self.stdscr.getstr(11, 12, 30).decode("utf-8")
                new_last_name = self.stdscr.getstr(12, 11, 30).decode("utf-8")
                new_city = self.stdscr.getstr(13, 6, 30).decode("utf-8")
                new_test_points = self.stdscr.getstr(
                    14, 13, 30).decode("utf-8")
                new_work_points = self.stdscr.getstr(
                    15, 13, 30).decode("utf-8")
                is_modified = True

                self.stdscr.refresh()

    def delete_student(self):
        if self.current == 0:
            return
        del self.students_list[self.current - 1]
        self.load_properties()
        self.stdscr.refresh()


def generate_report(stdscr):
    global header_color
    global second_header_color
    global info_color
    global option_color
    global higlighted_color
    global wrong_color

    stdscr.clear()

    base_choices = []
    advance_choices = {}

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Wybrane opcje:', header_color)
        stdscr.addstr(1, 0, 'Podstawowa analiza:', second_header_color)
        counter = 0

        for c in base_choices:
            stdscr.addstr(2, counter, c)
            counter += len(c) + 1

        stdscr.addstr(3, 0, 'Zaawansowana analiza:', second_header_color)
        counter = 0
        for c in advance_choices.values():
            stdscr.addstr(4, counter, c)
            counter += len(c) + 1

        stdscr.addstr(6, 0, 'Best test (Press 1)', option_color)
        stdscr.addstr(7, 0, 'Best work (Press 2)', option_color)
        stdscr.addstr(8, 0, 'Best total (Press 3)', option_color)
        stdscr.addstr(
            9, 0, 'Sex comparison - advanced (Press 4)', option_color)
        stdscr.addstr(
            10, 0, 'City comparison - advanced (Press 5)', option_color)

        stdscr.addstr(curses.LINES - 1, 0,
                      'Press space to generate report, d to clear analyses, ESC to return', info_color)

        key = stdscr.getkey()

        if key == ' ':
            if not advance_choices:
                advance_choices = None
            if base_choices:
                report = operations.Report(
                    'report.docx', base_choices, list(advance_choices))
                report.add_basic_content()
                if report.advanced_categories is not None:
                    report.add_advanced_content()
                report.save()
                stdscr.clear()
                stdscr.addstr(
                    0, 0, 'Raport generated. Press any key', info_color)
                stdscr.getkey()
                break
            else:
                stdscr.clear()
                stdscr.addstr(
                    0, 0, 'At least one basic analysis should be chosen! Press any key', wrong_color)
                stdscr.getkey()
        elif key == 'd':
            base_choices.clear()
            advance_choices.clear()
        elif key == '1':
            if 'test' not in base_choices:
                base_choices.append('test')
        elif key == '2':
            if 'work' not in base_choices:
                base_choices.append('work')
        elif key == '3':
            if 'total' not in base_choices:
                base_choices.append('total')

        elif key == '4':
            if 'sex' not in advance_choices:
                advance_choices[1] = 'sex'
        elif key == '5':
            if 'city' not in advance_choices:
                advance_choices[2] = 'city'
        elif ord(key) == 27:
            break


def edit(stdscr):
    stdscr.clear()
    edit_screen = EditScreen(stdscr)
    edit_screen.run()


def how_many_students(stdscr):
    stdscr.clear()
    EditScreen.load_students_list()
    allowed_number = len(EditScreen.students_list)
    string = f'How many students to show (1-{allowed_number}):'
    stdscr.addstr(0, 0, string)
    curses.echo()
    curses.curs_set(1)
    how_many = stdscr.getstr(0, len(string) + 1, 3)
    stdscr.clear()

    if int(how_many) <= allowed_number:
        return int(how_many)
    else:
        stdscr.clear()
        stdscr.addstr('You typed wrong value. Press any key', wrong_color)
        stdscr.getkey()
        return None


def show_result(stdscr, query):
    how_many = how_many_students(stdscr)

    if how_many is not None:
        students = operations.best_results(
            query, how_many, False, 'students.db')
        stdscr.clear()
        screen = ResultScreen(students, stdscr)
        screen.run()
        stdscr.refresh()


def show_advanced(stdscr):
    global header_color
    global higlighted_color
    global option_color
    global info_color
    global wrong_color

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Available analyses:', header_color)
        stdscr.addstr(1, 0, 'Sex comparison (Press 1)', option_color)
        stdscr.addstr(2, 0, 'City comparison (Press 2)', option_color)
        stdscr.addstr(curses.LINES - 1, 0, 'Press space to return', info_color)
        answer = stdscr.getkey()

        names = ['Students total number:',
                 'Students number for each category:',
                 'Average test points for each category:',
                 'Average work points for each category:',
                 'Average total points for each category:']

        if answer == '1':
            stdscr.clear()
            results = operations.advanced('students.db', 1)

            for name, values in zip(names, results):
                stdscr.clear()
                stdscr.addstr(curses.LINES - 1, 0,
                              'Press any key to continue',
                              info_color)
                stdscr.addstr(0, 0, name, higlighted_color)
                if len(values) == 1:
                    stdscr.addstr(1, 0, str(values[0][0]))
                    stdscr.getkey()
                    continue
                counter = 1
                for value in values:
                    stdscr.addstr(counter, 0, f'* {value[0]}:')
                    stdscr.addstr(counter, len(value[0]) + 4, str(value[1]))
                    counter += 1
                stdscr.getkey()

        elif answer == '2':
            stdscr.clear()
            results = operations.advanced('students.db', 2)

            for name, values in zip(names, results):
                stdscr.clear()
                stdscr.addstr(curses.LINES - 1, 0,
                              'Press any key to continue',
                              info_color)
                stdscr.addstr(0, 0, name, higlighted_color)
                if len(values) == 1:
                    stdscr.addstr(1, 0, str(values[0][0]))
                    stdscr.getkey()
                    continue
                counter = 1
                for value in values:
                    stdscr.addstr(counter, 0, f'* {value[0]}:')
                    stdscr.addstr(counter, len(value[0]) + 4, str(value[1]))
                    counter += 1
                stdscr.getkey()

        elif answer == ' ':
            return
        else:
            stdscr.clear()
            stdscr.addstr('You typed wrong value. Press any key', wrong_color)
            stdscr.getkey()
            stdscr.clear()


def run(stdscr):
    global header_color
    global second_header_color
    global info_color
    global option_color
    global higlighted_color
    global wrong_color

    stdscr.clear()
    if not os.path.exists('students.db'):
        stdscr.addstr(
            0, 0, 'No database file. Do you want to create it?[y/n]', info_color)
        stdscr.refresh()
        answer = stdscr.getkey()
        if answer == 'y':
            stdscr.clear()
            stdscr.addstr(0, 0, 'Path:')
            curses.echo()
            curses.curs_set(1)
            path = stdscr.getstr(0, 6, 30)
            stdscr.clear()
            operations.create_from_csv(path.decode("utf-8").strip())
            stdscr.addstr(
                0, 0, 'Success! Database created. Press any key', info_color)
            stdscr.getkey()
            stdscr.clear()

    while True:
        stdscr.addstr(0, 0, 'Result analysis', header_color)
        stdscr.addstr(1, 0, 'Please select a category to show',
                      higlighted_color)
        stdscr.addstr(2, 0, 'Best test scores (Press 1)', option_color)
        stdscr.addstr(3, 0, 'Best work scores (Press 2)', option_color)
        stdscr.addstr(4, 0, 'Best total scores (Press 3)', option_color)
        stdscr.addstr(5, 0, 'Advanced analysis (Press 4)', option_color)
        stdscr.addstr(curses.LINES - 1, 0,
                      'Press space to return, r to generate report, ESC to quit', info_color)
        stdscr.refresh()

        answer = stdscr.getkey()

        if answer == '1':
            show_result(stdscr, 'test')
            stdscr.clear()
        elif answer == '2':
            show_result(stdscr, 'work')
            stdscr.clear()
        elif answer == '3':
            show_result(stdscr, 'total')
            stdscr.clear()
        elif answer == '4':
            show_advanced(stdscr)
            stdscr.clear()
        elif answer == 'r':
            generate_report(stdscr)
            stdscr.clear()
        elif answer == ' ':
            return
        elif ord(answer) == 27:
            exit()
        else:
            stdscr.clear()
            stdscr.addstr('You typed wrong value. Press any key',
                          wrong_color)
            stdscr.getkey()
            stdscr.clear()


def main(stdscr):
    global header_color
    global second_header_color
    global info_color
    global option_color
    global higlighted_color
    global wrong_color

    # COLORS
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    header_color = curses.color_pair(1)

    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    second_header_color = curses.color_pair(2)

    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    info_color = curses.color_pair(3)

    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    option_color = curses.color_pair(4)

    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    higlighted_color = curses.color_pair(5)

    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)
    wrong_color = curses.color_pair(6)

    curses.curs_set(0)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, 'What do you want to do?', header_color)
        stdscr.addstr(1, 0, '1. Start analysis (Press space)', option_color)
        stdscr.addstr(2, 0, '2. Edit students (Press e)', option_color)
        stdscr.addstr(curses.LINES - 1, 0, 'To quit press ESC', info_color)
        stdscr.refresh()

        answer = stdscr.getkey()

        if answer == ' ':
            run(stdscr)
        elif answer == 'e':
            edit(stdscr)
            run(stdscr)
        elif ord(answer) == 27:
            exit()
        else:
            stdscr.clear()
            stdscr.addstr('You typed wrong value. Press any key', wrong_color)
            stdscr.getkey()


if __name__ == '__main__':
    wrapper(main)
