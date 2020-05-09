import numpy as np
import os
import json
import pandas as pd

# Load keypoint data from JSON output
column_names = ['x', 'y', 'acc']

# Paths - should be the folder where Open Pose JSON output was stored
path_to_json = "C:/Users/nmart/Desktop/openpose/output_folder_path/"

# Import Json files, pos_json = position JSON
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print('Found: ',len(json_files),'json keypoint frame files')
count = 0


# instanciate dataframes 
body_keypoints_df = pd.DataFrame()
left_knee_df = pd.DataFrame()

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
        left_knee_df = left_knee_df.append(temp_df.iloc[13].astype(int))

    except:
        print('bad point set at: ', file)
        
body_keypoints_df.columns = column_names
left_knee_df.columns = column_names

body_keypoints_df.reset_index()
left_knee_df = left_knee_df.reset_index(drop = True)

print('length of merged keypoint set: ',body_keypoints_df.size)

print(left_knee_df.head())