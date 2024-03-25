import sys
import Scan
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow



class Scanframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Scan.ui",self)
        self.show()

class Mainframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Mainframe.ui",self)
        self.Scanbtn.clicked.connect(self.btnClick)
        self.show()
        #self.setupUi(self)
        

    def btnClick(self):
        Main_frame.hide()
        Scan_frame=Scanframe()
        
        Scan_frame.show()

                  
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main_frame = Mainframe()
    Main_frame.show()
    app.exec_()






