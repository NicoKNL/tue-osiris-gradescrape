from PyQt5.QtCore import QAbstractTableModel, Qt


class GradesModel(QAbstractTableModel):
    def __init__(self, grades_data, header_data):
        super(QAbstractTableModel, self).__init__()
        self.grades_data = grades_data
        self.header_data = header_data

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.grades_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.grades_data[0])
        #return len(self.header_data)

    def data(self, index, role=Qt.DisplayRole):
        return self.grades_data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == 1:
            return self.header_data[section]
            #return self.header_data[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)