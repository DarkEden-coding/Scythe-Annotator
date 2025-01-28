# load yolo model and video and display
from ultralytics import YOLO


# Load a pretrained YOLO11n model
model = YOLO(r"E:\Ceph-Mirror\Python-Files\Projects\image-annotater\train_augmentation_model\runs\detect\train11\weights\best.pt")

# Define path to video file
source = r"C:\Users\darke\Downloads\videoplayback (1).mp4"

# Run inference on the source
results = model.predict(source, show=True)  # generator of Results objects
