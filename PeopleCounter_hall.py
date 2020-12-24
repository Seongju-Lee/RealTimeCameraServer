import numpy as np
import cv2 as cv
import Person
import time
import socket
import csv
from datetime import datetime

try:
    log = open('log.txt',"w")
except:
    print( "No se puede abrir el archivo log")

#사람 출입 체크 - 방향
cnt_up   = 0
cnt_down = 0

#카메라 모듈 설정
cap = cv.VideoCapture(0)


#콘솔 창에 캡처 속성을 출력한다.
for i in range(19):
    print( i, cap.get(i))

h = 480
w = 640
frameArea = h*w
areaTH = frameArea/250
print( 'Area Threshold', areaTH)

#입구와 출구/ 라인 설정
line_up = int(0.5*(h/5))
line_down   = int(4.2*(h/5))

up_limit =   int(0.1*(h/5))
down_limit = int(4.8*(h/5))


line_down_color = (0,0,255)
line_up_color = (255,0,0)
pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up]
pt4 =  [w, line_up]
pts_L2 = np.array([pt4,pt3], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

#배경
fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

#필터 요소들 적용
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

#변수 선언
font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

slot = [] # 타임슬롯 리스트
number_person_IN = []
number_person_OUT = []

start = time.time() # 시간 체크 변수 선언

now = datetime.now() # 현재 날짜 변수 선언

# 사람 인원 수 체크할 리스트 초기화
for i in range(len(slot)):
	number_person_IN.append(0)
	number_person_OUT.append(0)
number_person_IN[0] = 'IN'
number_person_OUT[0] = 'OUT'

while(cap.isOpened()):

    # 카메라가 켜지변 30분 단위로 체크
    timeChk = time.time() - start
    slot.append(str(now.hour) + ':' + str(now.minute))

    if round(timeChk) == 1800:
        slot.append(str(now.hour) + ':' + str(now.minute))
    if round(timeChk) == 3600:
        slot.append(str(now.hour) + ':' + str(now.minute))
    
    slot.append('all')

    # 카메라 읽어옴
    ret, frame = cap.read()
    for i in persons:
        i.age_one() 
   ####
   ##  전처리
   ##### 

    #마스킹을 위한 배경 제거
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    #이진화
    try:
        ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
        ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)
        
        # 마스킹
        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
        
        mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
        mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print( 'UP:',cnt_up)
        print ('DOWN:',cnt_down)
        break
    #################
    ###   윤곽
    #################
    
    # 외부 flag만 리턴, 모든 하위 윤곽이 남음.
    contours0, hierarchy = cv.findContours(mask2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv.contourArea(cnt)
        if area > areaTH:
            #################
            #   움직임 트랙킹 부분
            #################
            
            # 여러 사람, 화면 출력에 대한 조건들 추가..
            
            M = cv.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv.boundingRect(cnt)

            new = True
            if cy in range(up_limit,down_limit):
                for i in persons:
                    if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                        # 개체가 이전에 감지된 개체와 가까울 때
                        new = False
                        i.updateCoords(cx,cy)   #객체의 좌표를 계속하여 update
                        if i.going_UP(line_down,line_up) == True:
                            cnt_up += 1
                            print( "ID:",i.getId(),'crossed going up at',time.strftime("%c"))
                            log.write("ID: "+str(i.getId())+' crossed going up at ' + time.strftime("%c") + '\n')
                        elif i.going_DOWN(line_down,line_up) == True:
                            cnt_down += 1
                            print( "ID:",i.getId(),'crossed going down at',time.strftime("%c"))
                            log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c") + '\n')
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        #리스트에서 요소 제거부분
                        index = persons.index(i)
                        persons.pop(index)
                        del i     #메모리를 확보한다..
                if new == True:
                    p = Person.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1     
            #################
            #   도면
            #################
            cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            
    #############
    #   전처리  
    #############  
    for i in persons:

        cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)
        
    ##################
    #    csv 파일 생성 => 임의로 10초 간격 마다 30초까지 인원 파악 하도록 설정 
    #                     시간대별로 체크 가능하도록 시간 설정 가능

    str_up = 'OUT: '+ str(cnt_up)
    str_down = 'IN: '+ str(cnt_down)

    _time = time.time() - start
    
    cnt_out = cnt_up
    cnt_in = cnt_down


    if round(_time) == 1800:
    	number_person_IN[1] = cnt_in
    	number_person_OUT[1] = cnt_out
    elif round(_time) == 3600:
    	
    	number_person_IN[2] = cnt_in - number_person_IN[1] 
    	number_person_OUT[2] = cnt_out - number_person_OUT[1]
   

    number_person_IN[3] = (cnt_in)
    number_person_OUT[3] = (cnt_out)
    f = open('./numberOfPerson.csv','w',newline='')
    writer = csv.writer(f)
    writer.writerow(slot)
    writer.writerow(number_person_IN)
    writer.writerow(number_person_OUT)

    f.close()
    ##################  ==> csv파일 종료

    # 현재 프레임에 text ,line 표시
    frame = cv.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    frame = cv.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
    frame = cv.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    frame = cv.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
    cv.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv.LINE_AA)
    cv.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv.LINE_AA)
    cv.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv.LINE_AA)

    cv.imshow('Frame',frame)
    cv.imshow('Mask',mask)    
    
    #ESC키로 설정
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

log.flush()
log.close()
cap.release()
cv.destroyAllWindows()

