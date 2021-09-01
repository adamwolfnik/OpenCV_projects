import cv2
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(20,150)
red=[131,191,29,179,255,255]
blue=[82,206,0,133,255,255]
green=[23,255,20,95,255,255]
mycolorvalues=[[0,0,255],
               [255,0,0],
               [0,255,0]]

mycolors=[red,blue,green]
mypoints=[]
def find_color(img,mycolors,mycolorvalues):
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in mycolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHsv, lower, upper)
        x,y=get_contours(mask)
        cv2.circle(img,(x,y),10,mycolorvalues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count+=1
    return newpoints
        #cv2.imshow(str(color),mask)

def get_contours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.05*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y
def draw_on_canvas(mypoints,mycolorvalues):
    for point in mypoints:
        cv2.circle(result,(mypoints[0],mypoints[1]),10,mycolorvalues[mypoints[2]],cv2.FILLED)

while True:
    success, img=cap.read()
    result = img.copy()
    newpoints=find_color(result,mycolors,mycolorvalues)
    if len(newpoints)!=0:
        for nwp in newpoints:
            mypoints.append(nwp)
    if len(mypoints)!=0:
        for point in mypoints:
            draw_on_canvas(point,mycolorvalues)
    cv2.putText(result," Nikhil ",(320,128),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,2,(200,180,200),2)
    cv2.imshow("Result", result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break