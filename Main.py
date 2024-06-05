from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QTableWidgetItem , QAbstractItemView
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
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
        
    



# class ResultFrame(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = uic.loadUi("ResultFrame.ui", self)
#         self.setupTable()
#         self.display_results()

#     def setupTable(self):
#         # 테이블 위젯 설정: 10행 5열
#         self.ui.tableWidget.setRowCount(10)
#         self.ui.tableWidget.setColumnCount(5)
#         self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

#         # 열 제목 설정 (예시)
#         self.ui.tableWidget.setHorizontalHeaderLabels(["상품명", "가격", "카테고리", "주소링크", "등록시간"])


#     def display_results(self):
#         Recv_data=Clientsocket.Recv()
#         # while not self.isHidden():
#         titles = Recv_data["titles"]
#         prices = Recv_data["prices"]
#         categories = Recv_data["categories"]
#         links = Recv_data["links"]
#         timestamps = Recv_data["timestamps"]
#         print(titles)



#         for i in range(len(titles)): 
#     # 제목, 가격, 카테고리, 타임스탬프 열 설정
#             self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(titles[i]))
#             self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(prices[i]))
#             self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(categories[i]))
#             self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(links[i]))
#             self.ui.tableWidget.setItem(i, 4, QTableWidgetItem(timestamps[i]))



class ResultFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ResultFrame.ui", self)
        self.setupTable()
        self.current_page = 1
        self.total_pages = 1
        self.display_results()

        # 페이지 이동 버튼 클릭 이벤트 연결
        self.ui.prevBtn.clicked.connect(self.prev_page)
        self.ui.nextBtn.clicked.connect(self.next_page)

    def setupTable(self):
        # 테이블 위젯 설정: 10행 5열
        self.ui.tableWidget.setRowCount(10)
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 열 제목 설정 (예시)
        self.ui.tableWidget.setHorizontalHeaderLabels(["상품명", "가격", "카테고리", "주소링크", "등록시간"])

    def display_results(self):
        Recv_data = Clientsocket.Recv()
        titles = Recv_data["titles"]
        prices = Recv_data["prices"]
        categories = Recv_data["categories"]
        links = Recv_data["links"]
        timestamps = Recv_data["timestamps"]
        print(titles)

        self.total_pages = (len(titles) + 9) // 10  # 총 페이지 수 계산
        start_idx = (self.current_page - 1) * 10
        end_idx = min(start_idx + 10, len(titles))

        # 페이지 번호 표시
        self.ui.pageLabel.setText(f"Page {self.current_page}/{self.total_pages}")

        for i in range(start_idx, end_idx):
            self.ui.tableWidget.setItem(i - start_idx, 0, QTableWidgetItem(titles[i]))
            self.ui.tableWidget.setItem(i - start_idx, 1, QTableWidgetItem(prices[i]))
            self.ui.tableWidget.setItem(i - start_idx, 2, QTableWidgetItem(categories[i]))
            self.ui.tableWidget.setItem(i - start_idx, 3, QTableWidgetItem(links[i]))
            self.ui.tableWidget.setItem(i - start_idx, 4, QTableWidgetItem(timestamps[i]))

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_results()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_results()





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


