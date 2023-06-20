import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar = 150

while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img,draw=False)

    if(len(lmList)!=0):
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2-x1,y2-y1)
        # // interpolating
        vol = np.interp(length,[50,240],[minVol,maxVol])
        volBar = np.interp(length, [50, 240], [400, 150])
        volume.SetMasterVolumeLevel(vol,None)
    else:
        volume.SetMasterVolumeLevel(maxVol, None)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    tempimg = cv2.flip(img, 1)
    cv2.putText(tempimg, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Img", tempimg)
    if cv2.waitKey(1) == 13:  # 13 is the Enter Key
        break

    # cap.release()
    # cv2.destroyAllWindows()