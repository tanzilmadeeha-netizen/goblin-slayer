import os
from cvzone.PoseModule import PoseDetector
import cv2
import time

       

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("Posture Coach", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Posture Coach", 1280, 720)



detector = PoseDetector()

last_alert = 0
roast_index = 0
status = "NO HUMAN DETECTED"
status_color = (255,255,255)

roasts = [
    "warningwave1.mp3",
    "warningwave2.mp3",
    "warningwave3.mp3",
    "warningwave4.mp3",
    "warningwave5.mp3",
    "warningwave6.mp3"
]

while True:
    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)
    img = detector.findPose(img, draw=False)
    cv2.rectangle(
    img,
    (0,0),
    (1280,50),
    (20,20,20),
    -1
)
    cv2.rectangle(
    img,
    (10,55),
    (320,105),
    (20,20,20),
    -1
)
    cv2.putText(
                img,
                status,
                (20,85),
                cv2.FONT_HERSHEY_DUPLEX,
                0.8,
                status_color,
                2)
    cv2.putText(
    img,
    "GOBLIN SLAYER",
    (470,35),
    cv2.FONT_HERSHEY_DUPLEX,
    1,
    (255,255,255),
    2
)

    lmList, bboxInfo = detector.findPosition(img, draw=True)

    if lmList:
        skeleton_color = (0,255,0)

        nose_x = lmList[0][0]
        nose_y = lmList[0][1]

        left_eye_x = lmList[2][0]
        left_eye_y = lmList[2][1]

        right_eye_x = lmList[5][0]
        right_eye_y = lmList[5][1]
        
        
        

        

        left_shoulder_x = lmList[11][0]
        left_shoulder_y = lmList[11][1]
        right_shoulder_x = lmList[12][0]
        right_shoulder_y = lmList[12][1]
        chest_x = (left_shoulder_x + right_shoulder_x) // 2 - 100
        chest_y = (left_shoulder_y + right_shoulder_y) // 2 + 40
        chest_center_x = (left_shoulder_x + right_shoulder_x) // 2
        chest_center_y = (left_shoulder_y + right_shoulder_y) // 2


        shoulder_center = (left_shoulder_x + right_shoulder_x) // 2

        
        
        status = "HUMAN DETECTED"
        status_color = (0,255,0)
        


        difference = nose_y

        if difference > 390:    
            skeleton_color = (0,0,255)
            status = "GOBLIN DETECTED"
            status_color = (0,0,255)

            current_time = time.time()

            if current_time - last_alert > 10:

                os.startfile(
                    roasts[min(roast_index, len(roasts)-1)])

                roast_index += 1

                
                last_alert = current_time
        else:
            roast_index = 0
            skeleton_color = (0,255,0)

        cv2.line(
            img,
            (left_eye_x, left_eye_y),
            (nose_x, nose_y),
            skeleton_color,
            2
        )

        cv2.line(
            img,
            (right_eye_x, right_eye_y),
            (nose_x, nose_y),
            skeleton_color,
            2
        )
        
        cv2.line(
        img,
        (left_shoulder_x, left_shoulder_y),
        (right_shoulder_x, right_shoulder_y),
        skeleton_color,4)
        cv2.circle( img, (left_shoulder_x, left_shoulder_y),8,(0,0,0),-1)
        
        

        cv2.circle(img, (right_shoulder_x, right_shoulder_y), 8,(0,0,0),-1 )
        
        spine_end_y = chest_center_y + 120

        left_hip_x = lmList[23][0]
        left_hip_y = lmList[23][1]

        right_hip_x = lmList[24][0]
        right_hip_y = lmList[24][1]

        cv2.line(
            img,
            (left_hip_x, left_hip_y),
            (right_hip_x, right_hip_y),
            skeleton_color,
            4
        )

        cv2.circle( img,(left_hip_x, left_hip_y), 8,(0,0,0), -1)

        cv2.circle(img,(right_hip_x, right_hip_y),8, (0,0,0), -1 )

        cv2.line(
            img,
            (chest_center_x, chest_center_y),
            (chest_center_x, spine_end_y),
            skeleton_color,4 )
        hip_center_x = (left_hip_x + right_hip_x) // 2
        hip_center_y = (left_hip_y + right_hip_y) // 2
        left_elbow_x = lmList[13][0]
        left_elbow_y = lmList[13][1]

        right_elbow_x = lmList[14][0]
        right_elbow_y = lmList[14][1]

        left_wrist_x = lmList[15][0]
        left_wrist_y = lmList[15][1]

        right_wrist_x = lmList[16][0]
        right_wrist_y = lmList[16][1]

        cv2.circle(img,(left_wrist_x, left_wrist_y),8,(0,0,0),-1)

        cv2.circle(img,(right_wrist_x, right_wrist_y), 8,(0,0,0), -1 )

        cv2.line(img,(left_elbow_x, left_elbow_y),(left_wrist_x, left_wrist_y),skeleton_color,4)

        cv2.line(img, (right_elbow_x, right_elbow_y),  (right_wrist_x, right_wrist_y), skeleton_color,4 )

        cv2.line( img, (left_shoulder_x, left_shoulder_y), (left_elbow_x, left_elbow_y), skeleton_color, 4 )
        
        cv2.line( img, (right_shoulder_x, right_shoulder_y), (right_elbow_x, right_elbow_y), skeleton_color, 4 )
        
        cv2.circle(img,(left_elbow_x, left_elbow_y),8,(0,0,0), -1 )

        cv2.circle(
            img,
            (right_elbow_x, right_elbow_y),
            8,
            (0,0,0),
            -1 )

    

        cv2.line( img, (chest_center_x, chest_center_y), (hip_center_x, hip_center_y), skeleton_color,  4)

        cv2.circle(img,(chest_center_x, chest_center_y), 8,(0,0,0),-1)
        

        shoulder_center = (left_shoulder_x + right_shoulder_x) // 2
        
        
    
    cv2.putText(
    img,
    "Press Q to Exit",
    (1050, 700),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (0,0,0),
    1
)    
        
    cv2.imshow("Posture Coach", img)

    if cv2.waitKey(1) == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
