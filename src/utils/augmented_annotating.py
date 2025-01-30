from utils.annotation import Annotation


class AugmentedAnnotating:
    def __init__(self, yolo_model_path):
        from ultralytics import YOLO
        self.yolo_model = YOLO(yolo_model_path)

    def detect_objects(self, image, class_names, confidence):
        results = self.yolo_model(image, conf=confidence)

        annotations = []
        for box in results[0].boxes:
            box_class = int(box.cls[0])
            box_x = box.xywh.tolist()[0][0]
            box_y = box.xywh.tolist()[0][1]
            box_w = box.xywh.tolist()[0][2]
            box_h = box.xywh.tolist()[0][3]

            # convert to percentages from 0 to 1
            box_x /= image.width
            box_y /= image.height
            box_w /= image.width
            box_h /= image.height

            annotations.append(Annotation(f"{box_class} {box_x} {box_y} {box_w} {box_h}", class_names))
        return annotations