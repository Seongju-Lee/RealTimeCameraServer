# RealTimeCameraServer

__(공공장소(교내) 실시간 인원 수 파악 및 데이터 추출)__

__PeopleCounter_hall.py__: opencv와 캠 이용한 인원 수 체크, 체크한 내용들 30분 주기로 csv파일 최신화<br/>
__Person.py:__ 객체 인식 python 코드(오픈소스 참고 출처:  )<br/>
__client.py:__ 로컬 pc에 담긴 코드 ( csv 파일 받아 옴)<br/>
__net_client.js:__ nodejs 이용하여 웹 에서 파로 csv 파일 받아올 수 있도록 설정<br/>
__server.py:__ 라즈베리파이 또는 카메라 쪽에 있는 파일 ( csv 파일 송신)<br/>
__stream.js:__ nodejs 통신 이용하여 실시간 카메라 웹에서 스트리밍 가능하도록 구현<br/>
또는, mjpg-streamer툴 이용
<br/><br/><br/><br/>
 __시스템 개요 및 하드웨어 구성도__
 <br/><br/>
![image](https://user-images.githubusercontent.com/67941526/103155676-42478b80-47e5-11eb-89bf-217c6d88475b.png)

∙ OpenCV YOLO를 통해 IN/OUT 영역에 감지된 객체 검출<br/>
∙ 실시간 카메라 스트리밍으로 인원 수 데이터 파악 및 cvs 파일 생성<br/>
∙ csv 파일 송신<br/> 
∙ 로컬 pc와 스마트폰 통신을 통해 실시간으로 확인 가능<br/>

<br/><br/><br/>
__소프트웨어 구성 및 알고리즘 구성도__
<br/><br/>
 1. ‘출입 인원변수에 저장’ 상세 알고리즘 순서도<br/><br/>
![image](https://user-images.githubusercontent.com/67941526/103156005-c13dc380-47e7-11eb-8879-f43ef04fb5c6.png)

 2.  라즈베리파이 알고리즘 순서도<br/><br/>
![image](https://user-images.githubusercontent.com/67941526/103155758-f5b08000-47e5-11eb-9601-b691aae1f311.png)

 3.  데이터 파일 송신 과정 및 저장(웹에서 라즈베리파이 직접 접근 가능)<br/><br/>
![image](https://user-images.githubusercontent.com/67941526/103155776-0fea5e00-47e6-11eb-891c-9095b239b167.png)

