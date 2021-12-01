import os
import sqlite3
import sys

import matplotlib
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
                             QDesktopWidget, QFileDialog, QGridLayout, QLabel,
                             QLineEdit, QListWidget, QMainWindow, QMessageBox,
                             QPushButton, QRadioButton, QSpinBox, QTabWidget,
                             QTextEdit, QWidget)

from database_operations import operations
from student_generator import generator

matplotlib.use('Qt5Agg')
sns.set()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=800, height=800, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


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
        uic.loadUi('UI/advanced_widget.ui', self)

        # buttons
        self.show_button = self.findChild(QPushButton, 'pushButton')
        self.show_button.setEnabled(False)
        self.show_button.clicked.connect(self.advanced_results)
        
        self.return_button = self.findChild(QPushButton, 'pushButton_2')

        self.analyses_box = self.findChild(QComboBox, 'comboBox')
        self.analyses_box.addItems(('', 'Sex comparison', 'City comparison'))
        self.analyses_box.currentTextChanged.connect(self.change_button)


    def change_button(self):
        if self.analyses_box.currentText() == '':
            self.show_button.setEnabled(False)
        else:
            self.show_button.setEnabled(True)
    
    def advanced_results(self):
        self.adv_window = AdvancedResultsWindow(
            self, self.analyses_box.currentText())
        self.adv_window.show()


class ResultWindow(QWidget):
    def __init__(self, parent=None):
        super(ResultWindow, self).__init__(parent)
        uic.loadUi('UI/result_widget.ui', self)

        # buttons
        self.new_button = self.findChild(QPushButton, 'pushButton_3')
        self.advanced_button = self.findChild(QPushButton, 'pushButton')
        self.report_button = self.findChild(QPushButton, 'pushButton_2')
        self.report_button.clicked.connect(
            self.start_report_window)

        # combobox
        self.mode = self.findChild(QComboBox, 'comboBox')
        self.mode.addItems(('test', 'work', 'total'))
        self.mode.currentTextChanged.connect(self.update_run_window)
        query = self.mode.currentText()

        # spinbox
        self.actual_number = 5
        self.places = self.findChild(QSpinBox, 'spinBox')
        self.places.setMinimum(1)
        self.places.setValue(self.actual_number)
        self.places.setMaximum(MainWindow.database_size)
        number = self.places.value()
        self.places.valueChanged.connect(self.update_run_window)

        self.text = operations.best_results(
            query, number, False, 'students.db')

        # textbox
        self.text_box = self.findChild(QTextEdit, 'textEdit')
        self.text_box.setReadOnly(True)

        self.print_text()

    def update_run_window(self):
        self.actual_number = self.places.value()
        actual_query = self.mode.currentText()

        self.text = operations.best_results(
            actual_query, self.actual_number, False, 'students.db')

        self.print_text()

    def print_text(self):
        self.text_box.clear()
        for items in self.text:
            self.text_box.append(str(items[0]))
            for line in items[1]:
                self.text_box.append(line)
            self.text_box.append('\n')
        self.text_box.moveCursor(QtGui.QTextCursor.Start)

    def start_report_window(self):
        self.report_window = ReportWindow(actual_number=self.actual_number)
        self.report_window.show()


class EditDatabase(QWidget):
    @classmethod
    def load_database(cls):
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM STUDENTS''')
        cls.students_list = [generator.Student(
            info) for info in cursor.fetchall()]
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
                self.listbox.addItem(
                    f'{idx + 1}. {getattr(info, "name")} {getattr(info, "last_name")}')
        except AttributeError:
            pass
        self.listbox.currentRowChanged.connect(self.student_preview)

    def update_list(self):
        self.listbox.clear()
        for idx, info in enumerate(self.students_list):
            self.listbox.addItem(
                f'{idx + 1}. {getattr(info, "name")} {getattr(info, "last_name")}')

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
        operations.save_database(
            db_file='students.db', students_list=self.students_list)
        generator.save_to_csv(output_file='students.csv',
                              students_list=self.students_list)
        QMessageBox.information(
            self, 'Success', 'Database created successfully!')
        w.start_welcome_window()


# Separate windows
class ReportWindow(QMainWindow):
    def __init__(self, parent=None, actual_number=5):
        super(ReportWindow, self).__init__(parent)
        uic.loadUi('UI/report_window.ui', self)
        
        #set window size and position
        x, y, w, h = MainWindow.adjust_ui_window(self)
        self.setGeometry(x, y, w, h)

        # button
        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.generate_raport)

        # spinbox
        self.places = self.findChild(QSpinBox, 'spinBox')
        self.places.setMinimum(1)
        self.places.setValue(actual_number)
        self.places.setMaximum(MainWindow.database_size)

        # checkboxes
        self.chbox_test = self.findChild(QCheckBox, "checkBox")
        self.chbox_work = self.findChild(QCheckBox, "checkBox_2")
        self.chbox_total = self.findChild(QCheckBox, "checkBox_3")

        self.chbox_adv_sex = self.findChild(QCheckBox, "checkBox_4")
        self.chbox_adv_city = self.findChild(QCheckBox, "checkBox_5")

    def generate_raport(self):
        categories = []
        adv_categories = []

        if self.chbox_test.isChecked():
            categories.append('test')

        if self.chbox_work.isChecked():
            categories.append('work')

        if self.chbox_total.isChecked():
            categories.append('total')

        if self.chbox_adv_sex.isChecked():
            adv_categories.append(1)

        if self.chbox_adv_city.isChecked():
            adv_categories.append(2)

        if categories:
            report = operations.Report(
                'report.docx', categories, adv_categories, self.places.value())
            report.add_basic_content()
            if report.advanced_categories is not None:
                report.add_advanced_content()
            report.save()
            QMessageBox.information(self, 'Done', 'Report created')
            self.close()
        else:
            QMessageBox.warning(
                self, 'Error', 'At least one category must be selected')
            return


class AdvancedResultsWindow(QMainWindow):
    def __init__(self, parent=None, mode='sex'):
        super(AdvancedResultsWindow, self).__init__(parent)
        uic.loadUi('UI/advanced_results.ui', self)
        
        #set window size and position
        x, y, w, h = MainWindow.adjust_ui_window(self)
        self.setGeometry(x, y, w, h)
        
        self.mode = 1 if 'sex' in mode.lower() else 2
        self.results = operations.advanced('students.db', self.mode)
        
        #buttons
        self.report_button = self.findChild(QPushButton, 'pushButton')
        self.report_button.clicked.connect(self.generate_report)
        

        self.labels = [QLabel() for _ in range(len(self.results))]
        self.tabs = [QWidget() for _ in range(len(self.results))]
        self.figures = [MplCanvas() for _ in range(len(self.results))]

        self.create_graphs()

        self.tab_box = self.findChild(QTabWidget, "tabWidget")

        for i in range(len(self.results) - 1):
            self.tab_box.addTab(self.figures[i], f"Graph {i+1}")

    
    def create_graphs(self):
        properties = {1: ['Students number', 'pie', None],
                      2: ['Average test points', 'bar', 'Points'],
                      3: ['Average work points', 'bar', 'Points'],
                      4: ['Average total points', 'bar', 'Points']}

        for i in range(len(self.results)):
            if i == 0:
                continue

            values = [item[1] for item in self.results[i]]
            names1 = [item[0] for item in self.results[i]]

            if properties[i][1] == 'pie':
                self.figures[i-1].axes.pie(values, labels=names1,
                                           autopct=AdvancedResultsWindow.make_autopct(values))
            else:
                self.figures[i-1].axes.bar(names1, values)

            self.figures[i-1].axes.set_title(properties[i][0])
            self.figures[i-1].axes.set_ylabel(properties[i][2])

    def generate_report(self):
        self.report_window = ReportWindow()
        self.report_window.show()
        
    
    @staticmethod
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.1f}%  ({v:d})'.format(p=pct, v=val)
        return my_autopct


class EditStudent(QMainWindow):
    def __init__(self, parent=None, row=None):
        super(EditStudent, self).__init__(parent)
        uic.loadUi('UI/edit_student.ui', self)
        
        #set window size and position
        x, y, w, h = MainWindow.adjust_ui_window(self)
        self.setGeometry(x, y, w, h)
        
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
        # Radiobuttons
        self.man_rbutton = self.findChild(QRadioButton, "radioButton")
        self.man_rbutton.setChecked(True)
        self.woman_rbutton = self.findChild(QRadioButton, "radioButton_2")
        # Spinboxes
        self.test_spinbox = self.findChild(QSpinBox, "spinBox")
        self.work_spinbox = self.findChild(QSpinBox, "spinBox_2")

        if self.row or self.row == 0:
            current_info = EditDatabase.students_list[row]
            if getattr(current_info, "sex") == 'm':
                self.man_rbutton.setChecked(True)
            else:
                self.woman_rbutton.setChecked(True)
            self.name_entry.setText(getattr(current_info, "name"))
            self.last_name_entry.setText(getattr(current_info, "last_name"))
            self.city_entry.setText(getattr(current_info, "city"))
            self.test_spinbox.setValue(
                int(getattr(current_info, "test_points")))
            self.work_spinbox.setValue(
                int(getattr(current_info, "work_points")))

    def save_student(self):
        global w

        sex = 'f' if self.woman_rbutton.isChecked() else 'm'
        new_info = [None,
                    sex,
                    self.name_entry.text(),
                    self.last_name_entry.text(),
                    self.city_entry.text(),
                    str(self.test_spinbox.value()),
                    str(self.work_spinbox.value())]

        if self.row or self.row == 0:
            EditDatabase.students_list[self.row].edit(new_info[1:])
        else:
            EditDatabase.students_list.append(generator.Student(new_info))

        w.start_edit_database_window(new=False)
        self.close()

    def clear_data(self):
        self.self.man_rbutton.setChecked(True)
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

        # widget vars
        self.welcome_window = None
        self.result_window = None
        self.edit_database = None
        self.advanced_window = None

        self.start_welcome_window()

    # set proper widget
    def start_welcome_window(self):      
        self.welcome_window = WelcomeWindow(self)
        
        #set window size and position
        x, y, w, h = self.adjust_ui_window(self.welcome_window)
        self.setGeometry(x, y, w, h)
        
        self.setWindowTitle("Student Analyser")
        self.setCentralWidget(self.welcome_window)
        self.welcome_window.run_button.clicked.connect(
            self.start_result_window)
        self.welcome_window.edit_button.clicked.connect(
            lambda: self.start_edit_database_window(True))
        self.welcome_window.exit_button.clicked.connect(exit)
        self.show()

    def start_result_window(self):
        self.result_window = ResultWindow(self)
        
        #set window size and position
        x, y, w, h = self.adjust_ui_window(self.result_window)
        self.setGeometry(x, y, w, h)
        
        self.setWindowTitle("Results")
        self.setCentralWidget(self.result_window)
        self.result_window.new_button.clicked.connect(
            self.start_welcome_window)
        self.result_window.advanced_button.clicked.connect(
            self.start_advanced_window)
        self.show()

    def start_advanced_window(self):
        self.advanced_window = AdvancedWindow(self)
        
        #set window size and position
        x, y, w, h = self.adjust_ui_window(self.advanced_window)
        self.setGeometry(x, y, w, h)
        
        self.setWindowTitle("Advanced Analysis")
        self.setCentralWidget(self.advanced_window)
        self.advanced_window.return_button.clicked.connect(self.start_result_window)
        self.show()

    def start_edit_database_window(self, new=True):
        
        global w
        if new:
            option = QMessageBox.question(self, "Question", "Do you want to create new database?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if option == QMessageBox.Yes:
                os.remove('students.db')
                path = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),
                                                    'CSV files (*.csv);;All files(*.*)')
                operations.create_from_csv(path[0])
                QMessageBox.information(
                    self, 'Success', 'Database created successfully!')
                w.load_database_info('students.db')
            EditDatabase.load_database()
            
        self.edit_database = EditDatabase(self)
        
        #set window size and position (function doesn't work)
        # x, y, w, h = self.adjust_ui_window(self.edit_database)
        self.setGeometry(474, 236, 462, 323)
        
        self.setWindowTitle("Edit database")
        self.setCentralWidget(self.edit_database)
        self.edit_database.return_button.clicked.connect(self.start_welcome_window)
        self.show()
    
    @staticmethod
    def adjust_ui_window(object):
        cp = QDesktopWidget().availableGeometry().center()
        
        current_width = object.width()
        current_height = object.height()
        current_x_pos = cp.x() - (current_width // 2)
        current_y_pos = cp.y() - (current_height // 2)
        
        return current_x_pos, current_y_pos, current_width, current_height
    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MainWindow()
    w.load_database_info('students.db')    
    sys.exit(app.exec_())
