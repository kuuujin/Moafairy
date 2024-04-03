import socket
import pickle

# 서버 소켓 생성
Serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 소켓을 특정 포트에 바인딩
host = '127.0.0.1'
port = 12345
Serversocket.bind((host, port))

# 클라이언트의 연결을 기다림
Serversocket.listen()

print("서버가동중")
client_socket, addr = Serversocket.accept()
print(f"클라이언트 연결: {addr}")
while True:
    try:    
    
        
        # 클라이언트로부터 데이터를 받음
        Data = client_socket.recv(1024)

        Keyword, Selectstie = pickle.loads(Data)

        print(f"Keyword: {Keyword}")
        print(f"Selectstie: {Selectstie}")

    except ConnectionResetError:
        print("클라이언트 연결 종료!")
        break

    except Exception as e:
        #print(f"예외 발생: {e}")
        break
    # 클라이언트 소켓 종료