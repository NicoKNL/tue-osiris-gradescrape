import sys
import os
import json
from PyQt5.QtCore import QEventLoop, QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bs4 import BeautifulSoup
from browser import Render
from pprint import pprint

this_folder = os.path.dirname(os.path.realpath(__file__))
data_file = f"{this_folder}/gradescrape.json"
config_file = f"{this_folder}/config.json"

if not os.path.isfile(config_file):
    raise FileNotFoundError("Missing 'config.json' in the root directory.")

# Load user login from config file
with open(config_file, 'r') as f:
    osiris_login = json.load(f)

# Open or create and open data file
try:
    file = open(data_file, 'r')
except IOError:
    file = open(data_file, 'w')

osiris_url = r"https://osiris.tue.nl/osiris_student_tueprd/ToonResultaten.do"

# Fetch HTML data through headless browser
app = QApplication(sys.argv)
browser = Render(osiris_url, app, osiris_login)
html_data = browser.html

soup = BeautifulSoup(html_data, 'html.parser')
grades_for = " ".join(soup.find_all('span', {'class' : 'psbToonTekst'})[0].get_text().split(" ")[1:])
grade_table = soup.find_all('table', {'class': 'OraTableContent'})[0]
# print(grade_table)

table_headers = grade_table.findChildren('th')
print(table_headers)

header_data = []
for header in table_headers:
    header_text = header.get_text()
    header_data.append(header_text)

print(header_data)

rows = grade_table.findChildren('tr')

grade_data = [[header] for header in header_data] # Nest the header entries

for i, row in enumerate(rows):
    cols = row.findChildren('td')
    # row_data = []
    for column_idx, col in enumerate(cols):
        grade_data[column_idx].append(col.get_text())
        # row_data.append(col.get_text())

    # if row_data:
    #     grade_data.append(row_data) #append(" - ".join([d for d in row_data if d]))

try:
    previous_data = json.load(open(data_file))
except Exception as e:
    previous_data = []

new_grades = []

for gd in grade_data:
    old_news = False
    for pd in previous_data:
        if gd == pd:
            old_news = True
            break
    if not old_news:
        new_grades.append(gd)

def all_to_string(input_list):
    for i, column in enumerate(input_list):
        for j, row in enumerate(input_list[i]):
            input_list[i][j] = str(input_list[i][j])
    return input_list

def is_list_rectangular(input_list):
    column_length = None

    for row_idx in range(len(input_list)):
        if row_idx == 0:
            column_length = len(input_list[row_idx])
            continue

        if len(input_list[row_idx]) != column_length:
            return False

    return True


def remove_empty_columns(input_list):
    import numpy as np
    print(np.matrix(input_list))
    print("\n")
    empty_columns = []

    for column_idx in range(len(input_list)):
        is_empty = True
        for row_idx in range(len(input_list[column_idx])):
            print(f"- {input_list[column_idx][row_idx]}")
            if input_list[column_idx][row_idx]:
                is_empty = False
                # break

        if is_empty:
            empty_columns.append(column_idx)

    for column_idx in reversed(empty_columns):
        input_list.pop(column_idx)

    print(np.matrix(input_list))
    return input_list

grade_data = all_to_string(grade_data)
grade_data = remove_empty_columns(grade_data)

# Export the grades to a local datafile for future use
with open(data_file, 'w') as f:
    f.write(json.dumps(grade_data, indent=4))

# TODO: always load when directly run, only pop up when a new grade comes in
# if new_grades:
if True:
    import sys
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QMainWindow, QLabel
    from PyQt5.QtCore import QSize
    from PyQt5.uic import loadUi
    from grades_model import GradesModel

    ui_file = f"{this_folder}/gradescrape.ui"
    css_file = f"{this_folder}/gradescrape.css"
    # ui = compileUi(ui_file)

    class MainWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            loadUi(ui_file, self)

            self.setMinimumSize(QSize(300, 200))
            self.setWindowTitle("Osiris Gradescrape")
            self.setWindowModality(QtCore.Qt.ApplicationModal)
            # self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #TODO: to be implemented via custom titlebar

            with open(css_file, 'r') as f:
                css_as_string = "".join(f.readlines())
            # print(css_as_string)
            self.setStyleSheet(css_as_string)

            print(dir(self))
            self.grades_data = json.load(open(data_file))
            self.grades_model = GradesModel(self.grades_data)
            self.grades_view.setModel(self.grades_model)


    if __name__ == "__main__":
        # app = QtWidgets.QApplication(sys.argv)
        mainWin = MainWindow()
        mainWin.show()
        sys.exit(app.exec_())
