from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant


class GradesModel(QAbstractTableModel):
    def __init__(self, grades_data):
        super(QAbstractTableModel, self).__init__()
        self.grades_data = grades_data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.grades_data[0]) - 1

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.grades_data)
        # return len(self.header_data)

    def data(self, index, role=Qt.DisplayRole):
        if (role == Qt.DisplayRole):
            return self.grades_data[index.column()][index.row() + 1]
        else:
            return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == 1:
            return self.grades_data[section][0]
            # return self.header_data[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)
