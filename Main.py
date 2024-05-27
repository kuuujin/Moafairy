import pickle
import sys
import threading
import webbrowser
import requests
from Connectmodule import ClientSocket
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView

#서버와 연결
Clientsocket = ClientSocket()
Clientsocket.Connect()


class LoginFrame(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("loginframe.ui", self)
        self.ui.Loginbtn.clicked.connect(self.open_login_page)
    
    def open_login_page(self):
        # 외부 브라우저를 열어서 로그인 페이지로 이동
        login_url = "http://35.216.101.141:5000/login"  # 로그인 페이지 URL 설정
        webbrowser.open(login_url)

# 메인 프레임
class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("MainFrame.ui", self)
        self.Scanbtn.clicked.connect(self.Scanbtnclick)
        self.Searchbtn.clicked.connect(self.Searchbtnclick)
        self.show()

    def check_token_validity(self):
        # 서버에서 로그인 토큰의 유효성을 확인하는 요청을 보냅니다.
        token = self.get_saved_token()
        if token:
            response = requests.post("http://35.216.101.141:5000/verify_token", json={"token": token})
            if response.status_code == 200:
                # 토큰이 유효한 경우 메인 프레임으로 전환합니다.
                widget.setCurrentIndex(widget.currentIndex() + 1)
                # 토큰 확인을 더 이상 반복하지 않고 중지합니다.
                self.stop_token_checking()

    def stop_token_checking(self):
        # 토큰 확인 작업을 중지합니다.
        self.token_checking_timer.cancel()
    
    def get_saved_token(self):
        # 클라이언트에서 저장된 로그인 토큰을 반환합니다.
        # 여기서는 임의의 값인 "saved_token"을 반환하도록 설정합니다.
        return "saved_token"

    def Scanbtnclick(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Searchbtnclick(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)

# 스캔 프레임
class ScanFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ScanFrame.ui", self)
        self.Combo_category = QComboBox(self)
        self.Combo_category.addItems(['전체', '의류', '음식', '전자', '서적', '게임'])
        self.Combo_category.setStyleSheet("background-color:white")
        self.Combo_category.setGeometry(120, 210, 91, 35)
        self.Sendbtn.clicked.connect(self.Sendserver)
        self.Homebtn.clicked.connect(self.Homebtnclick)

    def Homebtnclick(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def Sendserver(self):
        Keyword = self.Keyword.toPlainText()
        Category = self.Combo_category.currentText()
        Data = pickle.dumps((Keyword, Category))
        Clientsocket = getattr(sys.modules[__name__], "Clientsocket")
        Clientsocket.Send(Data)

# 검색 프레임
class SearchFrame(ScanFrame):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("SearchFrame.ui", self)
        self.Sendbtn.clicked.connect(self.Sendserver)
        self.Homebtn.clicked.connect(self.Homebtnclick)
        self.Combo_category = QComboBox(self)
        self.Combo_category.addItems(['전체', '의류', '음식', '전자', '서적', '게임'])
        self.Combo_category.setStyleSheet("background-color:white")
        self.Combo_category.setGeometry(120, 210, 91, 35)

    def Homebtnclick(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    login_frame = LoginFrame()
    main_frame = MainFrame()
    scan_frame = ScanFrame()
    search_frame = SearchFrame()

    widget.addWidget(login_frame)
    widget.addWidget(main_frame)
    widget.addWidget(scan_frame)
    widget.addWidget(search_frame)
    widget.setFixedWidth(800)
    widget.setFixedHeight(1000)

    main_frame.token_checking_timer = threading.Timer(20.0, main_frame.check_token_validity)
    main_frame.token_checking_timer.start()

    widget.show()

    def Close_socket():
        if Clientsocket:
            Clientsocket.Disconnect()

    app.aboutToQuit.connect(Close_socket)
    app.exec_()




