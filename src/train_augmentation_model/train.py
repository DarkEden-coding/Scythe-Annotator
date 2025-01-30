from ultralytics import YOLO


if __name__ == '__main__':
    # Load a model
    # r"E:\Ceph-Mirror\Python-Files\Projects\image-annotater\train_augmentation_model\runs\detect\train7\weights\best.pt"
    model = YOLO(r"yolo11s.pt")  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data=r"C:\Users\darke\Downloads\resrtfyrguil\data.yaml", epochs=500, imgsz=640, device=0, patience=20)