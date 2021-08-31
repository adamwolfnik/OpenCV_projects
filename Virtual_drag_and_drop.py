import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.8)
colorR=(255,0,255)
cx,cy,w,h=100,100,200,200

class DragRect():
  def __init__(self,posCenter,size=[200,200]):
    self.posCenter=posCenter
    self.size=size
  def update(self,cursor):
    cx,cy=self.posCenter
    if cx-w//2<cursor[0]<cx+w//2 and cy-h/2<cursor[1]<cy+h//2:
      self.posCenter=cursor
      

rectlist=[]
for x in range(4):
  rectlist.append(DragRect([250*x+250,150]))

while True:
  success,img=cap.read()
  img=cv2.flip(img,1)
  img=detector.findHands(img)
  lmlist, _ =detector.findPosition(img)
  if lmlist:
    l,_,_=detector.findDistance(8,12,img,draw=False)
    if l<25:
      cursor=lmlist[8]
      for rect in rectlist:
        rect.update(cursor)  
  #Draw Solid
  #for rect in rectlist:
    #cx,cy=rect.posCenter
    #w,h=rect.size    
    #cv2.rectangle(img, (cx-w//2,cy-h//2),(cx+w//2,cy+h//2),colorR,cv2.FILLED)
    #cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),20,rt=0)
  #Draw transparent
  imgNew=np.zeros_like(img,np.uint8)
  for rect in rectlist:
    cx,cy=rect.posCenter
    w,h=rect.size    
    cv2.rectangle(imgNew, (cx-w//2,cy-h//2),(cx+w//2,cy+h//2),colorR,cv2.FILLED)
    cvzone.cornerRect(imgNew,(cx-w//2,cy-h//2,w,h),20,rt=0)
  out=img.copy()
  alpha=0.1
  mask=imgNew.astype(bool)
  out[mask]=cv2.addWeighted(img, alpha, imgNew,1-alpha, 0)[mask]

  cv2.imshow("Image",out)
  cv2.waitKey(1)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break 