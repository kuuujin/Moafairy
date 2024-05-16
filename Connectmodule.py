import socket

Modulevariable = None
Serverip = '34.47.77.2'
Serverport = 8888


class ClientSocket():
    #생성자에서 중복접속인지체크
    def __init__(self):
        global Modulevariable
        if Modulevariable is not None:
            raise Exception("중복")
        Modulevariable = self

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    #연결함수
    def Connect(self):
        if self.connected:
            return
        try:
            self.socket.connect((Serverip, Serverport))
            print("연결성공")
            self.connected = True
        except Exception as e:
            print("서버 연결 실패:", e)

    #연결해제함수
    def Disconnect(self):
        if not self.connected:
            return
        self.socket.close()
        print("연결해제")
        self.connected = False
    
    #서버전송함수
    def Send(self, Data):
        if not self.connected:
            raise Exception("서버에 연결되지 않았습니다")
        try:
            self.socket.sendall(Data)
            print("데이터 전송 성공")
        except Exception as e:
            print("데이터 전송 실패:", e)

    #연결확인함수
    def IsConnected(self):
        return self.connected