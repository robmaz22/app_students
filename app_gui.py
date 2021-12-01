import os
import sqlite3
import sys

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTextEdit, QSpinBox, QListWidget, QLabel, \
    QLineEdit, QComboBox, QMessageBox, QFileDialog, QCheckBox, QTabWidget, QVBoxLayout

from database_operations import operations
from student_generator import generator


# Main window widgets
class WelcomeWindow(QWidget):
    def __init__(self, parent=None):
        super(WelcomeWindow, self).__init__(parent)
        uic.loadUi('UI/welcome_widget.ui', self)

        # buttons
        self.run_button = self.findChild(QPushButton, 'pushButton')
        self.edit_button = self.findChild(QPushButton, 'pushButton_2')
        self.exit_button = self.findChild(QPushButton, 'pushButton_3')


class AdvancedWindow(QWidget):
    def __init__(self, parent=None):
        super(AdvancedWindow, self).__init__(parent)
        uic.loadUi('UI/advanced_widget_1.ui', self)

        self.r_button = self.findChild(QPushButton, 'pushButton')
        self.r_button.clicked.connect(self.advanced_results)

        self.graphs_checkbox = self.findChild(QCheckBox, 'checkBox')

        self.analyses_box = self.findChild(QComboBox, 'comboBox')
        self.analyses_box.addItems(('', 'Sex comparison', 'City comparison'))

    def advanced_results(self):
        self.adv_window = AdvancedResultsWindow(self, self.analyses_box.currentText())
        self.adv_window.show()


class ResultWindow(QWidget):
    def __init__(self, parent=None):
        super(ResultWindow, self).__init__(parent)
        uic.loadUi('UI/result_widget.ui', self)

        # buttons
        self.new_button = self.findChild(QPushButton, 'pushButton_3')
        self.advanced_button = self.findChild(QPushButton, 'pushButton')

        # spinbox
        self.places = self.findChild(QSpinBox, 'spinBox')
        self.places.setMinimum(1)
        self.places.setValue(5)
        self.places.setMaximum(MainWindow.database_size)
        number = self.places.value()
        self.places.valueChanged.connect(self.update_run_window)

        test_text = operations.best_test(number, 'students.db')
        total_text = operations.best_total(number, 'students.db')

        # textbox
        self.text_box = self.findChild(QTextEdit, 'textEdit')
        self.text_box.setReadOnly(True)

        for text, var in [('BEST TEST:', test_text), ('BEST TOTAL', total_text)]:
            self.text_box.append(text)
            for items in var:
                self.text_box.append(items[0])
                for line in items[1]:
                    self.text_box.append(line)
            self.text_box.append('\n')

        self.text_box.moveCursor(QtGui.QTextCursor.Start)

    def update_run_window(self):
        actual_number = self.places.value()

        test_text = operations.best_test(actual_number, 'students.db')
        total_text = operations.best_total(actual_number, 'students.db')

        self.text_box.clear()
        for text, var in [('BEST TEST:', test_text), ('BEST TOTAL', total_text)]:
            self.text_box.append(text)
            for items in var:
                self.text_box.append(items[0])
                for line in items[1]:
                    self.text_box.append(line)
            self.text_box.append('\n')

        self.text_box.moveCursor(QtGui.QTextCursor.Start)


class EditDatabase(QWidget):
    @classmethod
    def load_database(cls):
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM STUDENTS''')
        cls.students_list = [generator.Student(info) for info in cursor.fetchall()]
        conn.close()

    def __init__(self, parent=None):
        super(EditDatabase, self).__init__(parent)
        uic.loadUi('UI/edit_database_widget.ui', self)

        # buttons
        self.delete_button = self.findChild(QPushButton, "pushButton")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_student)

        self.edit_button = self.findChild(QPushButton, "pushButton_2")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_student)

        self.new_button = self.findChild(QPushButton, "pushButton_3")
        self.new_button.clicked.connect(lambda: self.edit_student(True))

        self.clear_button = self.findChild(QPushButton, "pushButton_4")
        self.clear_button.clicked.connect(self.clear_all)

        self.return_button = self.findChild(QPushButton, 'pushButton_6')
        self.update_button = self.findChild(QPushButton, 'pushButton_5')
        self.update_button.clicked.connect(self.update_database)

        # listbox
        self.listbox = self.findChild(QListWidget, "listWidget")
        try:
            for idx, info in enumerate(self.students_list):
                self.listbox.addItem(f'{idx + 1}. {getattr(info, "name")} {getattr(info, "last_name")}')
        except AttributeError:
            pass
        self.listbox.currentRowChanged.connect(self.student_preview)

    def update_list(self):
        self.listbox.clear()
        for idx, info in enumerate(self.students_list):
            self.listbox.addItem(f'{idx + 1}. {getattr(info, "name")} {getattr(info, "last_name")}')

    def edit_student(self, new=False):
        if new:
            self.edit_window = EditStudent(self)
        else:
            self.edit_window = EditStudent(self, row=self.listbox.currentRow())
        self.edit_window.show()

    def student_preview(self):
        try:
            info = self.students_list[self.listbox.currentRow()]
        except IndexError:
            self.name_label.setText('-')
            self.last_name_label.setText('-')
            self.city_label.setText('-')
            self.test_label.setText('-')
            self.work_label.setText('-')
            return

        self.delete_button.setEnabled(True)
        self.edit_button.setEnabled(True)

        self.name_label = self.findChild(QLabel, "label_7")
        self.name_label.setText(getattr(info, "name"))
        self.last_name_label = self.findChild(QLabel, "label_8")
        self.last_name_label.setText(getattr(info, "last_name"))
        self.city_label = self.findChild(QLabel, "label_9")
        self.city_label.setText(getattr(info, "city"))
        self.test_label = self.findChild(QLabel, "label_10")
        self.test_label.setText(getattr(info, "test_points"))
        self.work_label = self.findChild(QLabel, "label_11")
        self.work_label.setText(getattr(info, "work_points"))

    def delete_student(self):
        remove_index = self.listbox.currentRow()
        del self.students_list[remove_index]
        self.update_list()

    def clear_all(self):
        self.delete_button.setEnabled(False)
        self.edit_button.setEnabled(False)
        self.students_list.clear()
        self.listbox.clear()

    def update_database(self):
        global w
        operations.save_database(db_file='students.db', students_list=self.students_list)
        generator.save_to_csv(output_file='students.csv', students_list=self.students_list)
        QMessageBox.information(self, 'Success', 'Database created successfully!')
        w.start_welcome_window()


# Separate windows
class AdvancedResultsWindow(QMainWindow):
    def __init__(self, parent=None, mode='sex'):
        super(AdvancedResultsWindow, self).__init__(parent)
        uic.loadUi('UI/advanced_results.ui', self)
        self.mode = 1 if 'sex' in mode.lower() else 2
        self.results = operations.advanced('students.db', self.mode)
        names = ['Students total number:',
                 'Students number for each category:',
                 'Average test points for each category:',
                 'Average work points for each category:',
                 'Average total points for each category:']

        self.labels = [QLabel() for _ in range(len(self.results))]
        self.tabs = [QWidget() for _ in range(len(self.results))]

        self.tab_box = self.findChild(QTabWidget, "tabWidget")
        for i in range(len(self.results)):
            self.tab_box.addTab(self.tabs[i], f'Tab {i+1}')

        self.tab_box.setTabText(0, 'aaaa')

        # counter = 0
        # for name, values, label, tab in zip(names, self.results, self.labels, self.tabs):
        #     # tab.layout = QVBoxLayout()
        #     text = f'{name}\n'
        #     if len(values) == 1:
        #         text += str(values[0][0])
        #         text += '\n'
        #         # label.setText(text)
        #         # tab.layout.addWidget(label)
        #         # tab.setLayout(tab.layout)
        #         tab.setTabText(text)
        #         continue
        #     for value in values:
        #         text += f'* {value[0]}: {value[1]}\n'

            # tab.setTabText(text)
            # label.setText(text)
            # tab.layout.addWidget(label)
            # tab.setLayout(tab.layout)

            # self.text_box.append(name)
            # if len(values) == 1:
            #     self.text_box.append(str(values[0][0]))
            #     self.text_box.append('\n')
            #     continue
            # for value in values:
            #     self.text_box.append(f'* {value[0]}: {value[1]}')
            # self.text_box.append('\n')


class EditStudent(QMainWindow):
    def __init__(self, parent=None, row=None):
        super(EditStudent, self).__init__(parent)
        uic.loadUi('UI/edit_student.ui', self)
        self.row = row

        # Buttons
        self.save_button = self.findChild(QPushButton, 'pushButton_2')
        self.save_button.clicked.connect(self.save_student)
        self.clear_button = self.findChild(QPushButton, 'pushButton')
        self.clear_button.clicked.connect(self.clear_data)
        # Entries
        self.name_entry = self.findChild(QLineEdit, "lineEdit")
        self.last_name_entry = self.findChild(QLineEdit, "lineEdit_2")
        self.city_entry = self.findChild(QLineEdit, "lineEdit_3")
        # Combobox
        self.sex_cbox = self.findChild(QComboBox, "comboBox")
        self.sex_cbox.addItems(('', 'Male', 'Female'))
        # Spinboxes
        self.test_spinbox = self.findChild(QSpinBox, "spinBox")
        self.work_spinbox = self.findChild(QSpinBox, "spinBox_2")

        if self.row or self.row == 0:
            current_info = EditDatabase.students_list[row]
            if getattr(current_info, "sex") == 'm':
                self.sex_cbox.setCurrentIndex(1)
            else:
                self.sex_cbox.setCurrentIndex(2)
            self.name_entry.setText(getattr(current_info, "name"))
            self.last_name_entry.setText(getattr(current_info, "last_name"))
            self.city_entry.setText(getattr(current_info, "city"))
            self.test_spinbox.setValue(int(getattr(current_info, "test_points")))
            self.work_spinbox.setValue(int(getattr(current_info, "work_points")))

    def save_student(self):
        global w

        sex = 'f' if self.sex_cbox.currentText() == 'Female' else 'm'
        new_info = [None,
                    sex,
                    self.name_entry.text(),
                    self.last_name_entry.text(),
                    self.city_entry.text(),
                    str(self.test_spinbox.value()),
                    str(self.work_spinbox.value())]

        if self.row or self.row == 0:
            EditDatabase.students_list[self.row].edit(new_info)
        else:
            EditDatabase.students_list.append(generator.Student(new_info))

        w.start_edit_database_window(new=False)
        self.close()

    def clear_data(self):
        self.sex_cbox.setCurrentIndex(0)
        self.name_entry.setText('')
        self.last_name_entry.setText('')
        self.city_entry.setText('')
        self.test_spinbox.setValue(0)
        self.work_spinbox.setValue(0)


# Main window
class MainWindow(QMainWindow):
    @classmethod
    def load_database_info(cls, path):
        cls.database_path = path
        conn = sqlite3.connect(cls.database_path)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM STUDENTS''')
        cls.database_size = len(cursor.fetchall())
        conn.close()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # window properties
        self.setGeometry(50, 50, 450, 450)

        # widget vars
        self.welcome_window = None
        self.result_window = None
        self.edit_database = None
        self.advanced_window = None

        self.start_welcome_window()

    # set proper widget
    def start_welcome_window(self):
        self.welcome_window = WelcomeWindow(self)
        self.setWindowTitle("Student Analyser")
        self.setCentralWidget(self.welcome_window)
        self.welcome_window.run_button.clicked.connect(self.start_result_window)
        self.welcome_window.edit_button.clicked.connect(lambda: self.start_edit_database_window(True))
        self.welcome_window.exit_button.clicked.connect(exit)
        self.show()

    def start_result_window(self):
        self.result_window = ResultWindow(self)
        self.setWindowTitle("Results")
        self.setCentralWidget(self.result_window)
        self.result_window.new_button.clicked.connect(self.start_welcome_window)
        self.result_window.advanced_button.clicked.connect(self.start_advanced_window)
        self.show()

    def start_advanced_window(self):
        self.advanced_window = AdvancedWindow(self)
        self.setWindowTitle("Advanced Analysis")
        self.setCentralWidget(self.advanced_window)
        self.show()

    def start_edit_database_window(self, new=True):
        global w
        if new:
            option = QMessageBox.question(self, "Question", "Do you want to create new database?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if option == QMessageBox.Yes:
                option = QMessageBox.question(self, "Question", "Do you want to create database from csv file?",
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if option == QMessageBox.Yes:
                    os.remove('students.db')
                    path = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),
                                                       'CSV files (*.csv);;All files(*.*)')
                    operations.create_from_csv(path[0])
                    QMessageBox.information(self, 'Success', 'Database created successfully!')
                    w.load_database_info('students.db')
            EditDatabase.load_database()
        self.edit_database = EditDatabase(self)
        self.setWindowTitle("Edit database")
        self.setCentralWidget(self.edit_database)
        self.edit_database.return_button.clicked.connect(self.start_welcome_window)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.load_database_info('students.db')
    sys.exit(app.exec_())
