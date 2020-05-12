# ai-research-project
This project allows for the user to run OpenPose detection on any video file. The final.py file can be modified to detect different types of motions. It can currently only detect wrist and shoulder movements. However, we are using part-candidates with openpose so we can easily detect another body part by calling a different key.
SetUp:
1. Download OpenPost on your computer
2. Generate the json files with the command:
./build/examples/openpose/openpose.bin --video examples/media/video.avi --write_json output/ --display 0 --render_pose 0 --part_candidates
3. replace the video examples flag with the path of your video file, the redered json files should appear in a new folder called output
4. Generate a video with the saved drawings with the command:
./build/examples/openpose/openpose.bin --video examples/media/video.avi --write_video output/result.avi --write_json output/
This command will output a new video with the saved drawings as result.avi
5. Run the file final.py. A video window should pop up showing the input video with the saved OpenPose drawings as well as the x and y values for the wrist and shoulder. The body part detection can be easily changed by changing the body part candidate key used in the code.
