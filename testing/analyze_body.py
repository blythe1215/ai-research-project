import numpy as np
import cv2
from right_wrist import detection
import os
import cv2

# read video
print("Working Directory: " + os.getcwd())
video = os.path.join(os.getcwd(), 'videos', 'result.avi') #https://stackoverflow.com/questions/2953834/windows-path-in-python
print("Video file: " + video)
cap = cv2.VideoCapture(video)

counter = 0

def show_values(json_file):
    column_names = ['x', 'y', 'acc']
    body_keypoints_df = pd.DataFrame()
    body_part1_df = pd.DataFrame()
    right_shoulder_df = pd.DataFrame()

    width = 640
    height = 480

wrist_pd = detection()[0]
shoulder_pd = detection()[1]
print(wrist_pd)

while(cap.isOpened()):
    ret, frame = cap.read()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    #drawing on x and y values
    cv2.putText(
        frame, #numpy array on which text is written
        "right wrist x: "+str(wrist_pd.loc[counter,'x']), #text
        (100, 50), #position at which writing has to start
        cv2.FONT_HERSHEY_SIMPLEX, #font family
        0.5, #font size
        (255,255,255), #font color
        3) #font stroke

    cv2.putText(
        frame, #numpy array on which text is written
        "y: "+str(wrist_pd.loc[counter,'y']), #text
        (100,100), #position at which writing has to start
        cv2.FONT_HERSHEY_SIMPLEX, #font family
        0.5, #font size
        (255,255,255), #font color
        3) #font stroke

    cv2.putText(
        frame, #numpy array on which text is written
        "right shoulder x: "+str(shoulder_pd.loc[counter,'x']), #text
        (500, 50), #position at which writing has to start
        cv2.FONT_HERSHEY_SIMPLEX, #font family
        0.5, #font size
        (255,255,255), #font color
        3) #font stroke

    cv2.putText(
        frame, #numpy array on which text is written
        "y: "+str(shoulder_pd.loc[counter,'y']), #text
        (500,100), #position at which writing has to start
        cv2.FONT_HERSHEY_SIMPLEX, #font family
        0.5, #font size
        (255,255,255), #font color
        3) #font stroke

    #printing indicators
    wrist = wrist_pd.loc[counter,'y']
    shoulder = shoulder_pd.loc[counter,'y']
    if wrist > shoulder:
        a = "raised"
        cv2.putText(frame, "position: "+a, (300,400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 3)
    elif wrist < shoulder:
        a = 'down'
        cv2.putText(frame, "position: "+a, (300,400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 3)
    else:
        a = "??"
        cv2.putText(frame, "position: "+a, (300,400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 3)

    cv2.imshow('frame', frame)
    cv2.waitKey(500)
    print(wrist_pd.loc[counter])
    counter += 1


    #cv2.imwrite('output.png', frame)

cap.release()
cv2.destroyAllWindows()

  
