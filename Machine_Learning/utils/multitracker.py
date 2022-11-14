import cv2
import numpy as np

class multitracker():
    def __init__(self):
        self.multitrackers = cv2.MultiTracker_create()
        self.prev = [] #이전 추적기 위치를 저장할 리스트
        self.id = 0 #인덱스를 통해 현재 추적된 위치와 이전 추적된 위치 비교
        self.isFirst = True #사람을 처음 감지했는지 boolean 변수로 표현 -> settings or updates
        self.warning = False #월담 추적 boolean 변수
        self.peopleNum = 0 #사람 수를 비교할 변수

    def settings(self, coord, frame):
        #사람이 한동안 감지되지 않았다가 다시 감지될 때, 추적기 초기화
        if not self.isFirst:
            self.multitrackers = cv2.MultiTracker_create()
        else:
            self.isFirst = False
        self.prev = []
        self.id = 0
        self.peopleNum = len(coord) #사람 수
        for i in coord:
            i0, i2 = abs(int(i[0] * 640)), abs(int(i[2] * 640))
            i1, i3 = abs(int(i[1] * 360)), abs(int(i[3] * 360))
            window = (i0, i1, i2, i3) #추적 상자
            print(window)
            self.prev.append(window)
            csrt = cv2.TrackerCSRT_create()

            self.multitrackers.add(csrt, frame, window) #추적기 세팅

    def updatebox(self, frame):
        self.id = 0
        (success, boxes) = self.multitrackers.update(frame) #업데이트 된 추적 상자
        temp = []
        for box in boxes:
            [x, y, w, h] = [abs(int(v)) for v in box]
            temp.append([x, y, w, h])
            if self.id < len(self.prev):
                # 이전 상자와의 y축 변화가 위로 수직이며 30픽셀 이상일 때
                if self.prev[self.id][1] - y > 30:
                    print("******침입 감지 ! ! ! ! !*******")
                    self.warning = True
            self.id += 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        self.prev = temp # 이전 윈도우 업데이트