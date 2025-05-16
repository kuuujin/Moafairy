import socket
import pickle
import select
import struct
Modulevariable = None
Serverip = '35.216.101.141'
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

 

# 클라이언트 측 코드
    def Recv(self):
        if not self.connected:
            raise Exception("서버에 연결되지 않았습니다")
        try:
            # 서버로부터 데이터 크기 정보 수신
            data_size_bytes = self.socket.recv(struct.calcsize('I'))
            self.expected_data_size = struct.unpack('I', data_size_bytes)[0]
            print(f"Expected data size: {self.expected_data_size}")

            data = b''
            total_size = 0
            while True:
                chunk = self.socket.recv(65536)
                if not chunk:
                    print("데이터 수신 완료")
                    break
                data += chunk
                total_size += len(chunk)
                print(f"수신한 데이터 크기: {total_size}")
            
            # 수신한 데이터 크기가 서버가 보낸 데이터 크기와 같으면 break
                if total_size == self.expected_data_size:
                    print("데이터 수신 완료")
                    break
            Data = pickle.loads(data)
            print("데이터 수신 성공")
            return Data
        except Exception as e:
            print("데이터 수신 실패:", e)
            return None
    #연결확인함수
    def IsConnected(self):
        return self.connected
    