1)Put it in a folder. Let's name it (NDDS_data)
2)Add yolov3.cfg to a folder (you can find it in darknet/cfg folder)
3)Rename yolov3.cfg to yolo-obj.cfg
4)Put train images to /NDDS_data/data folder
5)Put validation images to /NDDS/data_valid folder
6)Put "darknet" compiled file in NDDS_data folder
7)type in terminal: python create_dataset.py
8)Wait till it's done. There might be some warnings during this process. Don't worry :D
9)Now you can just run_training.sh script to start training your model
10)To modify parameters of training just edit yolo-obj.cfg file
11)Enjoy!
