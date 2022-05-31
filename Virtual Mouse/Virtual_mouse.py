import cv2
import mediapipe
import autopy
import numpy
import time

cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands  
mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils  
wScr, hScr = autopy.screen.size()  
pX, pY = 0, 0  
cX, cY = 0, 0  

def hand_landmarks(colorImg):
    landmarks_list = []  

    landmarkPositions = mainHand.process(colorImg)  
    landmarkCheck = landmarkPositions.multi_hand_landmarks  
    if landmarkCheck:  
        for hand in landmarkCheck:  
            for index, landmark in enumerate(hand.landmark):  
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS) 
                h, w, c = img.shape  
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)  
                landmarks_list.append([index, centerX, centerY])          
    return landmarks_list

def fingers(landmarks):
    finger_tips = []  
    finger_tips_ids = [4, 8, 12, 16, 20] 
    
    if landmarks[finger_tips_ids[0]][1] > lmList[finger_tips_ids[0] - 1][1]:
        finger_tips.append(1)
    else:
        finger_tips.append(0)
    
    for id in range(1, 5):
        if landmarks[finger_tips_ids[id]][2] < landmarks[finger_tips_ids[id] - 3][2]:  
            finger_tips.append(1)
        else:
            finger_tips.append(0)
    return finger_tips

while True:
    check, img = cap.read()  
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
    lmList = hand_landmarks(imgRGB)
    
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  
        x2, y2 = lmList[12][1:]  
        finger = fingers(lmList) 
        
        if finger[1] == 1 and finger[2] == 0:  # Checks pointing index finger
            x3 = numpy.interp(x1, (75, 640 - 75), (0, wScr))  
            y3 = numpy.interp(y1, (75, 480 - 75), (0, hScr))  
            
            cX = pX + (x3 - pX) / 7  
            cY = pY + (y3 - pY) / 7  
            
            autopy.mouse.move(wScr-cX, cY)  # Moves the cursor inversely
            pX, pY = cX, cY  

        if finger[1] == 0 and finger[0] == 1:  # Checks thumbs-up sign
            autopy.mouse.click() 
            time.sleep(1)
            
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# ccto The Assembly for the tutorial