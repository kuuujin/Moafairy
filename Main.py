from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTableWidgetItem
#from PyQt5.QtWebEngineWidgets import QWebEngineView
import requests
import sys
import threading
import webbrowser
import pickle
from Connectmodule import ClientSocket
import asyncio
#서버와 연결
Clientsocket = ClientSocket()
Clientsocket.Connect()





        
       

# 메인 프레임
class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("MainFrame.ui", self)
        self.Scanbtn.clicked.connect(self.Scanbtnclick)
        self.Searchbtn.clicked.connect(self.Searchbtnclick)
        self.show()

   

    def Scanbtnclick(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Searchbtnclick(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)

# 스캔 프레임
class ScanFrame(QMainWindow):
    Funcs='scan'
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
        Funcs = self.Funcs
        Data = pickle.dumps((Keyword, Category, Funcs))
        Clientsocket = getattr(sys.modules[__name__], "Clientsocket")
        Clientsocket.Send(Data)
        result_frame = ResultFrame()
        result_frame.show()
        

        


# 검색 프레임
class SearchFrame(ScanFrame):
    Funcs='search'
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
    
    def Sendserver(self):
        Keyword = self.Keyword.toPlainText()
        Category = self.Combo_category.currentText()
        Funcs = self.Funcs
        Data = pickle.dumps((Keyword, Category, Funcs))
        Clientsocket = getattr(sys.modules[__name__], "Clientsocket")
        Clientsocket.Send(Data)
        #새로운 창으로 결과프레임(ResultFrame)이 떠야함
        result_frame = ResultFrame()
        result_frame.show()
        
    



class ResultFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ResultFrame.ui", self)
        self.setupTable()
        self.display_results()

    def setupTable(self):
        # 테이블 위젯 설정: 10행 5열
        self.ui.tableWidget.setRowCount(10)
        self.ui.tableWidget.setColumnCount(5)
        # 열 제목 설정 (예시)
        self.ui.tableWidget.setHorizontalHeaderLabels(["상품명", "가격", "카테고리", "주소링크", "등록시간"])


    def display_results(self):
        Recv_data=Clientsocket.Recv()
        titles = Recv_data["titles"]
        prices = Recv_data["prices"]
        categories = Recv_data["categories"]
        links = Recv_data["links"]
        timestamps = Recv_data["timestamps"]
        print(titles)



        # for i in range(10):  # 5행에 대하여
        #     self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(titles[i]))
        #     self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(prices[i]))
        #     self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(categories[i]))
        #     self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(links[i]))
        #     self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(timestamps[i]))
            








if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    
    
    main_frame = MainFrame()
    scan_frame = ScanFrame()
    search_frame = SearchFrame()
    widget.addWidget(main_frame)
    widget.addWidget(scan_frame)
    widget.addWidget(search_frame)
    widget.setFixedWidth(800)
    widget.setFixedHeight(1000)


    widget.show()

    def Close_socket():
        if Clientsocket:
            Clientsocket.Disconnect()

    app.aboutToQuit.connect(Close_socket)
    app.exec_()



