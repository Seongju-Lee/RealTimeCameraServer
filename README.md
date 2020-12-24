# RealTimeCameraServer

PeopleCounter_hall.py: opencv와 캠 이용한 인원 수 체크, 체크한 내용들 30분 주기로 csv파일 최신화
Person.py: 객체 인식 python 코드(오픈소스 참고 출처:  )
client.py: 로컬 pc에 담긴 코드 ( csv 파일 받아 옴)
net_client.js: nodejs 이용하여 웹 에서 파로 csv 파일 받아올 수 있도록 설정
server_.py: 라즈베리파이 또는 카메라 쪽에 있는 파일 ( csv 파일 송신)
stream.js: nodejs 통신 이용하여 실시간 카메라 웹에서 스트리밍 가능하도록 구현
또는, mjpg-streamer툴 이용
