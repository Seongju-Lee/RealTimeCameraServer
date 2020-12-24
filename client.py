import socket # client
import sys

# 서버 IP & port
ip = '192.168.137.59'
port = 9190

# 클라이언트 소켓 준비 
client = socket.socket()

i = 1 # 파일 번호

# 서버 접속
client.connect((ip, port))

f = open('C:/Users/lsj40/Desktop/pi (1)/pi/numOfPeople.csv', 'wb')

l = 1
while(l):
  l = client.recv(1024)
  print('Data --> {0}'.format(l))
  print(l)
  while(l):
    f.write(l)
    l = client.recv(1024)
  f.close()
client.close()


