import socket

Modulevariable = None
Serverip = 'localhost'
Serverport = 12345

class ClientSocket():
    def __init__(self):
        global Modulevariable
        if Modulevariable is not None:
            raise Exception("중복")
        Modulevariable = self

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def Connect(self):
        if self.connected:
            return
        try:
            self.socket.connect((Serverip, Serverport))
            print("연결성공")
            self.connected = True
        except Exception as e:
            print("서버 연결 실패:", e)

    def Disconnect(self):
        if not self.connected:
            return
        self.socket.close()
        print("연결해제")
        self.connected = False

    def IsConnected(self):
        return self.connected