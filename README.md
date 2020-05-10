# ai-research-project
SetUp:
1. Download OpenPost on your computer
2. Generate the json files with the command:
./build/examples/openpose/openpose.bin --video examples/media/video.avi --write_json output/ --display 0 --render_pose 0 --part_candidates
3. replace the video examples flag with the path of your video file, the redered json files should appear in a new folder called output
4. Generate a video with the saved drawings with the command:
