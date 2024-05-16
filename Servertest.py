import socket
import pickle
import threading

# 서버 소켓 생성
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 소켓을 특정 포트에 바인딩
host = '127.0.0.1'
port = 12345
ServerSocket.bind((host, port))

# 클라이언트 연결 대기
ServerSocket.listen()

print("서버가동중")

def handle_client(client_socket, addr):
    try:
        while True:
            # 클라이언트로부터 데이터를 받음
            Data = client_socket.recv(1024)

            # 데이터가 없으면 연결 종료
            if not Data:
                break

            # 데이터를 복호화하고 키워드와 카테고리 추출
            Keyword, Category = pickle.loads(Data)

            # 키워드가 비어 있으면 "all"로 설정
            if Keyword == "":
                Keyword = "all"

            # 추출된 키워드와 카테고리를 출력
            print(f"클라이언트 {addr}: Keyword: {Keyword}, Category: {Category}")

    except ConnectionResetError:
        print(f"클라이언트 {addr} 연결 종료!")
    except Exception as e:
        print(f"클라이언트 {addr} 처리 중 오류 발생: {e}")
    finally:
        # 클라이언트 소켓 종료
        client_socket.close()

while True:
    # 새로운 클라이언트 연결 수락
    client_socket, addr = ServerSocket.accept()
    print(f"새로운 클라이언트 연결: {addr}")

    # 새로운 스레드 생성하여 클라이언트 처리
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()