import numpy as np
import os
import json
import pandas as pd
import cv2 
 

# Load keypoint data from JSON output
column_names = ['x', 'y', 'acc']

# Paths - should be the folder where Open Pose JSON output was stored
path_to_json = "C:/Users/nmart/Desktop/openpose/video_output_folder/"

# Import Json files, pos_json = position JSON
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print('Found: ',len(json_files),'json keypoint frame files')
count = 0


# instanciate dataframes 
body_keypoints_df = pd.DataFrame()
right_wrist_df = pd.DataFrame()
right_shoulder_df = pd.DataFrame()

print('json files: ',json_files[0])

width = 640
height = 480

# Loop through all json files in output directory
# Each file is a frame in the video
# If multiple people are detected - choose the most centered high confidence points
for file in json_files:

    temp_df = json.load(open(path_to_json+file))
    temp = []
    for k,v in temp_df['part_candidates'][0].items():
        
        # Single point detected
        if len(v) < 4:
            temp.append(v)
            #print('Extracted highest confidence points: ',v)
            
        # Multiple points detected
        elif len(v) > 4: 
            near_middle = width
            np_v = np.array(v)
            
            # Reshape to x,y,confidence
            np_v_reshape = np_v.reshape(int(len(np_v)/3),3)
            np_v_temp = []
            # compare x values
            for pt in np_v_reshape:
                if(np.absolute(pt[0]-width/2)<near_middle):
                    near_middle = np.absolute(pt[0]-width/2)
                    np_v_temp = list(pt)
         
            temp.append(np_v_temp)
            #print('Extracted highest confidence points: ',v[index_highest_confidence-2:index_highest_confidence+1])
        else:
            # No detection - record zeros
            temp.append([0,0,0])
            
    temp_df = pd.DataFrame(temp)
    temp_df = temp_df.fillna(0)
    #print(temp_df)

    try:
        prev_temp_df = temp_df
        body_keypoints_df= body_keypoints_df.append(temp_df)
        right_wrist_df = right_wrist_df.append(temp_df.iloc[4].astype(int))
        right_shoulder_df = right_shoulder_df.append(temp_df.iloc[2].astype(int))

    except:
        print('bad point set at: ', file)
        
body_keypoints_df.columns = column_names
right_wrist_df.columns = column_names
right_shoulder_df.columns = column_names

body_keypoints_df.reset_index()
right_wrist_df = right_wrist_df.reset_index(drop = True)
right_shoulder_df = right_shoulder_df.reset_index(drop = True)


#print('length of merged keypoint set: ',body_keypoints_df.size)

#print(right_wrist_df)
#print(right_shoulder_df)

#comparing y values of shoulder and wrist to determine if hand is raised

wrist = right_wrist_df['y']
shoulder = right_shoulder_df['y']
arr = []
for w in wrist:
        if w > 150:
            arr.append("up")
        else:
            arr.append("down")

#references: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
#https://medium.com/@sduxbury/how-you-can-build-practical-applications-by-quantifying-observations-from-video-e266b945eea0

#vidcap = cv2.VideoCapture('examples\media/driving_clip.mp4')
#success,image = vidcap.read()
#count = 0
"""while success:
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1"""
"""while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for val in arr:
        
        cv2.putText(gray,val,(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
    
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""
print(temp_df)

def draw_bar_box(img, heel_pt, toe_pt, color_select = (255,255,255)):
    fudge_fact = 20
    heel_x = int(np.mean(heel_pt[0]))-15
    toe_x = int(np.mean(toe_pt[1]))+1 5
    top = 0
    base = height
    
    # call the open cv rectangle function
    cv2.rectangle(img, (heel_x,top), (toe_x, base), color_select, -1)

draw_bar_box('frame147.jpg', temp_df, temp_df)

def draw_poly_line(img, pts, color_select = (255,255,255), thick = 2):
    poly_line_thickness = thick
    poly_closed = False
    pts = pts[:,0:2]
    pts = pts.reshape((-1,1,2))
    
    # call the open cv poly line function
    cv2.polylines(img, np.int32([pts]), poly_closed, color_select, thickness=poly_line_thickness)

"""directory = 'frames'
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        print(os.path.join(directory, filename))
        draw_bar_box(img, heel_pt, toe_pt)
    else:
        continue"""


#cv2.imshow(vidcap, 'frame113.jpg')



