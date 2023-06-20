import cv2
import time
import HandTrackingModule as htm
import math

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)
flag=True

while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img,draw=False)

    if(len(lmList)!=0):

        lengths=[]
        for x in range(8,21,4):
            length = math.hypot( lmList[x-4][1]- lmList[x][1], lmList[x-4][2]-lmList[x][2])
            lengths.append(length)


        if(lengths[0]>=100 and lengths[0]<=150 and lengths[1]<50 and lengths[2]<50 and lengths[3]<50):
            tempimg=cv2.flip(img,1)
            cv2.imwrite("GetSetPhotoOutput.jpg",tempimg)
            flag = False
            break



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    tempimg = cv2.flip(img, 1)
    cv2.putText(tempimg, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Live Image", tempimg)
    if cv2.waitKey(1) == 13 or flag == False:  # 13 is the Enter Key
        break
