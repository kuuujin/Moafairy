

import sys
from PyQt5.QtWidgets import *


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        

        # for i in range(10):
        #     for j in range(5):
        #         self.tableWidget.setItem(i, i, QTableWidgetItem(str(i+j)))
                
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('SearchResult')
        self.setGeometry(300, 100, 600, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())