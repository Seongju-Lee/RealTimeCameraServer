import socket # server
import threading
import argparse
import time
import sys

ip = ''
port = 9191

def thread(client, address) : #쓰레드 
  print("client connected")

  f = open('/Users/gwanpil/Desktop/test/test.csv', 'rb') # b - binary. // 라즈베리파잉 csv 파일 생성위치로 주소 변경할 것.
  l = f.read(1024)
  while(l):
    client.send(l)
    l = f.read(1024)
  client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ip, port))

server.listen(5) #최대 5개의 클라이언트 접속 허용 
#2. bind to a address and port

while 1 :
  try:
    client, address = server.accept()

  except socket.error as msg: #일단 임시
    server.close()
    sys.exit()

  t = threading.Thread(target=thread, args=(client, address))
  t.start()
 
server.close()
