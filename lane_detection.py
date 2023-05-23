import cv2
import numpy as np
import matplotlib.pyplot as plt

def roi(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    return cv2.bitwise_and(img,mask) #masked image

def draw_lane(img, lines):

    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    lineLeft = False; lineRight = False

    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(blank_image, (x1,y1), (x2,y2), (0,255,0), 2)

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

def process(img):
    
    #---------------------Lanes-----------------------
    height = img.shape[0]
    width = img.shape[1]

    roiVertices = [(0,height), (width/2,height/2), (width, height)] #adjusted for hood of car to be masked

    grayImg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    canny = cv2.Canny(grayImg, 100, 150) #adjust upper threshold if lanes are not being detected

    croppedImage = roi(canny, np.array([roiVertices],np.int32))

    lines = cv2.HoughLinesP(croppedImage, 
                            rho=1, #adjust 
                            theta=np.pi/180,
                            threshold=50, #adjust  
                            lines=np.array([]), 
                            minLineLength=100, #adjust
                            maxLineGap=50)

    #----------------------Objects---------------------

    if lines is not None: #if HoughLinesP couldn't find any lines in a given frame, don't bother trying to draw
        
        filtered_lines = [] #filtering out horizontal-ish lines to improve HoughLinesP accuracy

        for line in lines:
            x1,y1,x2,y2 = line[0]
            slope = (y2-y1)/(x2-x1)

            if abs(slope) > 0.3:
                filtered_lines.append(line)
        
        img = draw_lane(img, filtered_lines)
    return img

cap = cv2.VideoCapture('test3.mp4') #change src video here

while cap.isOpened():
    ret, frame = cap.read()
    #ret, frame2 = cap.read()

    targetWidth = 1920; targetHeight = 1080
    
    if ret:
        frame = cv2.resize(frame, (targetWidth, targetHeight))
        #frame2 = cv2.resize(frame2, (targetWidth, targetHeight))

    processedFrame = process(frame)

    cv2.imshow("video", processedFrame)
    if cv2.waitKey(10) == 27: #esc key
        break

cv2.destroyAllWindows()
cap.release()