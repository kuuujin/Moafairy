import socket

# 서버에 연결
server_host = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# 서버로 메시지 전송
message = "Hello, server!"
client_socket.sendall(message.encode())

# 서버로부터 데이터를 받음
data = client_socket.recv(1024)

# 받은 데이터 출력
print(f"서버로부터 받은 데이터: {data.decode()}")

# 클라이언트 소켓 종료
client_socket.close()