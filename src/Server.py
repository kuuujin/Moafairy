import socket
import pickle
import threading
import redis
import sys
import struct
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 서버 소켓 생성
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 소켓을 특정 포트에 바인딩
host = '0.0.0.0'
port = 8888
ServerSocket.bind((host, port))

print("서버가동중")
ServerSocket.listen()

def handle_client(client_socket, addr):
    try:
        while True:
            # 클라이언트로부터 데이터를 받음
            Data = client_socket.recv(1024)

            # 데이터가 없으면 연결 종료
            if not Data:
                break

            # 데이터를 복호화하고 키워드와 카테고리 추출
            Keyword,Category,Funcs = pickle.loads(Data)
            if Keyword == "":
              Keyword = "all"
            print("호출기능:"+Funcs)
            print("키워드:"+Keyword)
            print("카테고리:"+Category)
            
            if Funcs == 'search':
                print("search_func() 함수 실행")
    # 결과를 전역 변수가 아닌 지역 변수로 처리
                titles, prices, categories ,links, timestamps = search_func(Keyword)
    
                data_to_send = {"titles": titles, "prices": prices, "categories": categories ,"links": links, "timestamps": timestamps}
                send_data = pickle.dumps(data_to_send)
                data_size = len(send_data)
    # 데이터 크기 정보를 클라이언트에게 전송
                client_socket.sendall(struct.pack('I', data_size))  
    # 실제 데이터 전송
                chunk_size = 4096
                for i in range(0, data_size, chunk_size):
                  client_socket.sendall(send_data[i:i+chunk_size])
    
                print("전송 성공")

            
                
            elif Funcs == 'scan':
                print("scan_func() 함수 실행")
                # 결과를 전역 변수가 아닌 지역 변수로 처리
                titles, prices, categories, links, timestamps = scan_func(Keyword)
                
                data_to_send = {"titles": titles, "prices": prices, "categories": categories,"links": links, "timestamps": timestamps}
                send_data = pickle.dumps(data_to_send)
                data_size = len(send_data)
    # 데이터 크기 정보를 클라이언트에게 전송
                client_socket.sendall(struct.pack('I', data_size))  
    # 실제 데이터 전송
                chunk_size = 4096
                for i in range(0, data_size, chunk_size):
                  client_socket.sendall(send_data[i:i+chunk_size])
                print("전송성공")            


    except ConnectionResetError:
        print(f"클라이언트 {addr} 연결 종료!")
    except Exception as e:
        print(f"클라이언트 {addr} 처리 중 오류 발생: {e}")
    finally:
        client_socket.close()

def scan_func(Keyword):
    rd = redis.StrictRedis(host='localhost', port=6379, db=0)
    titles, prices, categories, links, timestamps = [], [], [], [], []
    keys = rd.keys('product:*')
    for key in keys:
        title = rd.hget(key, 'title').decode('utf-8')
        price = rd.hget(key, 'price').decode('utf-8')
        category = rd.hget(key, 'category').decode('utf-8')
        link = rd.hget(key, 'link').decode('utf-8')
        timestamp = rd.hget(key, 'timestamp').decode('utf-8')
        if Keyword == "all":
            titles.append(title)
            prices.append(price)
            categories.append(category)
            links.append(link)
            timestamps.append(timestamp)
        elif Keyword in title:
            titles.append(title)
            prices.append(price)
            categories.append(category)
            links.append(link)
            timestamps.append(timestamp)
            
    return titles, prices, categories, links, timestamps


def search_func(Keyword):
    titles, prices, categories, links, timestamps, = [], [], [], [], []
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("headless")
    browser = webdriver.Chrome(options=options)
    
    url = 'https://www.algumon.com/search/' + Keyword
    browser.get(url)
    
    actions = browser.find_element(By.CSS_SELECTOR , 'body')
    
    
    
    titleselector = "/html/body/div[6]/div[2]/ul/li/div[1]/div[2]/div/p[2]/span/a"
    priceselector = "/html/body/div[6]/div[2]/ul/li/div[1]/div[2]/p[1]"
    linkselector = "/html/body/div[6]/div[2]/ul/li/div[1]/div[2]/div/p[2]/span/a"
    timestampselector = "/html/body/div[6]/div[2]/ul/li/div[1]/div[2]/p[2]/small"
    last_count = 0
    
    for _ in range(5):
    
        time.sleep(3)
        
        # 현재 페이지의 모든 항목을 가져옴
        current_titles = browser.find_elements(By.XPATH, titleselector)
        current_prices = browser.find_elements(By.XPATH, priceselector)
        current_links = browser.find_elements(By.XPATH, linkselector)
        current_timestamps = browser.find_elements(By.XPATH, timestampselector)
        
        for i in range(last_count, len(current_titles)):
            titles.append(current_titles[i].text)
            prices.append(current_prices[i].text)
            links.append(current_links[i].get_attribute("href"))
            timestamps.append(current_timestamps[i].text)
            categories.append('')
        # 이번에 처리한 항목의 수를 업데이트
        last_count = len(current_titles)

        # 페이지 끝으로 스크롤
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    browser.quit()
        
    return titles, prices, categories ,links, timestamps



while True:
    client_socket, addr = ServerSocket.accept()
    print(f"새로운 클라이언트 연결: {addr}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
