import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets

#메인프레임
class Mainframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Mainframe.ui",self)
        self.Scanbtn.clicked.connect(self.Scanbtnclick)
        self.show()
        
    #프레임전환함수
    def Scanbtnclick(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

#스캔프레임
class Scanframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Scanframe.ui",self)
        
        #이벤트 함수
        #self.변수명.clicked.connect(self.함수)
        
        #스캔프레임 변수
        self.Fm.clicked.connect(self.SelectSite)
        self.Bbu.clicked.connect(self.SelectSite)
        self.Quasar.clicked.connect(self.SelectSite)
        self.Sendbtn.clicked.connect(self.Sendserver)

        # 선택된 사이트 저장 변수
        self.selected_site = None

# 사이트 선택 함수
    def SelectSite(self):
        if self.Fm.isChecked():
            self.selected_site = "fm"
        elif self.Bbu.isChecked():
            self.selected_site = "bbu"
        elif self.Quasar.isChecked():
            self.selected_site = "quasar"
    

    #서버로전송함수
    def Sendserver(self):
        if self.selected_site is None:
            print("사이트를 선택하세요.")
            return
        
        Keyword = self.Keyword.toPlainText()
        print(Keyword)
        Selectsite = self.selected_site
        print(Selectsite)
    

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    app.setStyleSheet("QWidget { background-color: #e6e6fa; }")
    
    #화면 전환용 widget
    widget = QtWidgets.QStackedWidget()

    #레이아웃 인스턴스
    Mainframelayout = Mainframe()
    Scanframelayout = Scanframe()

    #위젯에 추가
    widget.addWidget(Mainframelayout)
    widget.addWidget(Scanframelayout)

    widget.setFixedWidth(800)
    widget.setFixedHeight(1000)
    widget.show()

    #프로그램 실행
    app.exec_()






