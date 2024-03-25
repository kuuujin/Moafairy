import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("scan.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #이벤트 함수
        #self.변수명.clicked.connect(self.함수)
        
        self.Fm.clicked.connect(self.Send)
        self.Bbu.clicked.connect(self.Send)
        self.Quasar.clicked.connect(self.Send)
        self.Sendbtn.clicked.connect(self.Send)

    def Send(self):
        Keyword = self.Keyword.toPlainText()
        print(Keyword)
        Selectsite = ""
        if self.Fm.isChecked():
            Selectsite = "fm"
        elif self.Bbu.isChecked():
            Selectsite = "bbu"
        elif self.Quasar.isChecked():
            Selectsite = "quasar"
        print(Selectsite)


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
