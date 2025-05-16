#-*- coding: utf-8 -*-

from flask import Flask, redirect, request, session, jsonify
import os
import requests
import uuid  # uuid 모듈 임포트

app = Flask(__name__)
app.secret_key = os.urandom(24)

DISCORD_CLIENT_ID = '1239752553009512458'
DISCORD_CLIENT_SECRET = 'FchRgNP4xpwYF5MCpH71HCYL8Y-fduxX'
DISCORD_REDIRECT_URI = 'http://35.216.101.141:5000/callback'
API_BASE_URL = 'https://discord.com/api'

logged_in_users = {}

@app.route('/')
def home():
    return 'Welcome to the Discord OAuth App'

@app.route('/login')
def login():
    return redirect(f"https://discord.com/oauth2/authorize?client_id=1239752553009512458&response_type=code&redirect_uri=http%3A%2F%2F35.216.101.141%3A5000%2Fcallback&scope=identify+guilds")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': DISCORD_CLIENT_ID,  
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(f"{API_BASE_URL}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    tokens = r.json()
    
    # 세션 ID 생성
    session_id = str(uuid.uuid4())
    
    # 각 클라이언트의 세션에 토큰 저장
    session[session_id] = tokens['access_token']
    
    # 콜백 완료 후 응답
    return '<html><body><script type="text/javascript">window.close();</script>Logged in successfully. You can close this window.</body></html>'
    
@app.route('/verify_token', methods=['POST'])
def verify_token():
    # 클라이언트로부터 전달된 세션 ID와 토큰을 가져옴
    data = request.json
    session_id = data.get('session_id')
    token = data.get('access_token')

    # 세션 ID를 이용하여 해당 클라이언트의 토큰을 가져옴
    session_token = session.get(session_id)
    
    # 토큰을 검증하여 유효한지 확인
    if token == session_token:
        return jsonify({"message": "Token is valid"}), 200
    else:
        return jsonify({"message": "Token is invalid"}), 401
        

def get_auth_token(session_id):
    return session.get(session_id)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
