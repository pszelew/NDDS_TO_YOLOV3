Designed to create training data for: https://github.com/AlexeyAB/darknet.git

1) Put it python script in a folder. Let's name it "NDDS_data". You can of course name it as you want :)

2) Add yolov3.cfg to a folder (you can find it in darknet/cfg folder)

3) Rename "yolov3.cfg" to "yolo-obj.cfg"

4) Put train images to /NDDS_data/data_train folder

5) Put validation images to /NDDS/data_valid folder

6) Put "darknet" compiled file in NDDS_data folder

7) Put "data/labels" folders from darknet to NDDS_data folder

8) Type in terminal: python create_dataset.py

9) Wait till it's done. There might be some warnings during this process. Don't worry :D

10) Now you can just run_training.sh script to start training your model

11) To modify parameters of training just edit yolo-obj.cfg file

12) To run training you can use run_training.sh script. Just put it in NDDS_data folder and run it!

13) Wait till you learn your network

14) Enjoy!
