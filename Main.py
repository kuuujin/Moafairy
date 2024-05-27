import pickle
import sys
import PyQt5.uic as uic
from Connectmodule import ClientSocket
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow , QComboBox , QTextEdit
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import requests
import webbrowser



#서버와 연결
Clientsocket = ClientSocket()
Clientsocket.Connect()


class Loginframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Loginframe.ui",self)
        self.Loginbtn.clicked.connect(self.login)
        self.setMinimumSize(640, 480)
        self.setMaximumSize(800, 600)
        


    def login(self):
        webbrowser.open('http://35.216.101.141:5000/login')
    

#메인프레임
class Mainframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Mainframe.ui",self)
        self.Scanbtn.clicked.connect(self.Scanbtnclick)
        self.Searchbtn.clicked.connect(self.Searchbtnclick)
        self.show()
        
    #스캔프레임전환함수
    def Scanbtnclick(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    #검색프레임전환함수
    def Searchbtnclick(self):
        widget.setCurrentIndex(widget.currentIndex()+2)


#스캔프레임
class Scanframe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Scanframe.ui",self)
        
        #이벤트 함수
        #self.변수명.clicked.connect(self.함수)
        
        #콤보박스
        self.Combo_category=QComboBox(self)
        self.Combo_category.addItems(['전체','의류','음식','전자','서적','게임'])
        self.Combo_category.setStyleSheet("background-color:white")
        self.Combo_category.setGeometry(120,210,91,35)
        #키워드

        #스캔프레임 변수
        self.Sendbtn.clicked.connect(self.Sendserver)
        self.Homebtn.clicked.connect(self.Homebtnclick)




#메인프레임으로 이동 함수
    def Homebtnclick(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    #서버로전송함수
    def Sendserver(self):
        Keyword = self.Keyword.toPlainText()
        Category= self.Combo_category.currentText()
        Msg_source='scan'
        
        Data = pickle.dumps((Msg_source,Keyword,Category))
        Clientsocket = getattr(sys.modules[__name__], "Clientsocket")
        Clientsocket.Send(Data)

#검색프레임(스캔프레임 상속으로 코드 간결화)
class Searchframe(Scanframe):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Searchframe.ui", self)

        self.Sendbtn.clicked.connect(self.Sendserver)
        self.Homebtn.clicked.connect(self.Homebtnclick)
        self.Combo_category=QComboBox(self)
        self.Combo_category.addItems(['전체','의류','음식','전자','서적','게임'])
        self.Combo_category.setStyleSheet("background-color:white")
        self.Combo_category.setGeometry(120,210,91,35)
    # 메인프레임으로 이동 함수 (재정의)
    def Homebtnclick(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)
    

    #서버로전송함수
    def Sendserver(self):
        Keyword = self.Keyword.toPlainText()
        Category= self.Combo_category.currentText()
        Msg_source='search'
        
        Data = pickle.dumps((Msg_source,Keyword,Category))
        Clientsocket = getattr(sys.modules[__name__], "Clientsocket")
        Clientsocket.Send(Data)


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    #app.setStyleSheet("QWidget { background-color: #e6e6fa; }")
    #화면 전환용 widget
    widget = QtWidgets.QStackedWidget()

    #레이아웃 인스턴스
    Loginframelayout = Loginframe()
    Mainframelayout = Mainframe()
    Scanframelayout = Scanframe()
    Searchframelayout = Searchframe()

    #위젯에 추가
    widget.addWidget(Loginframelayout)
    widget.addWidget(Mainframelayout)
    widget.addWidget(Scanframelayout)
    widget.addWidget(Searchframelayout)
    widget.setFixedWidth(800)
    widget.setFixedHeight(1000)
    widget.show()
    def Close_socket():
        if Clientsocket:
            Clientsocket.Disconnect()
        
    app.aboutToQuit.connect(Close_socket)
    #프로그램 실행
    app.exec_()







