import os
import random
from multiprocessing.pool import ThreadPool as Pool
from tkinter import filedialog

import customtkinter as ctk
import cv2
import yaml
from PIL import Image
from tqdm import tqdm

from dialogs.group_query_dialog import GroupQueryDialog
from dialogs.loading_dialog import LoadingDialog
from utils.annotation import Annotation
from utils.image_processing import hash_thread, group_similar_images
from utils.image_to_label_path import image_to_label_path


def eliminate_similar_images(image_paths):
    chunk_size = len(image_paths) // 20
    chunks = [image_paths[i:i + chunk_size] for i in range(0, len(image_paths), chunk_size)]
    pool = Pool(20)

    print("Computing hashes for each image")

    results = pool.map(hash_thread, chunks)
    results = [item for sublist in results for item in sublist]
    pool.close()
    pool.join()

    print("Comparing hashes")

    groups = group_similar_images(results)

    non_similar_images = [group[0] for group in groups]

    similar_images = [group[1:] for group in groups if len(group) > 1]

    print(f"Eliminated {len(similar_images)} similar images")
    print(f"Remaining images: {len(non_similar_images)}")

    return non_similar_images, similar_images


def load_yolo_dataset(button_frame):
    dataset_path = filedialog.askdirectory(title="Select Dataset Folder")
    start_location = button_frame.parent_window.get_center()
    progress = LoadingDialog("Loading Dataset", start_location=start_location)
    if dataset_path:
        images = []
        labels = []

        # Walk through dataset to find images, labels, and 'data.yaml'
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith((".jpg", ".jpeg", ".png")):
                    images.append(os.path.join(root, file))
                elif file.endswith(".txt"):
                    labels.append(os.path.join(root, file))
                elif file == "data.yaml":
                    with open(os.path.join(root, file), "r") as f:
                        data = yaml.load(f, Loader=yaml.FullLoader)

        all_images = images.copy()

        progress.close()
        progress = LoadingDialog("Eliminating Similar Images", start_location=start_location)

        # Eliminate similar images based on perceptual hashing
        images, removed_groups = eliminate_similar_images(images)

        progress.close()

        # Query dialog to confirm removal of similar images
        dialog = GroupQueryDialog(button_frame.master, removed_groups, button_frame.parent_window, start_location=start_location)
        button_frame.master.wait_window(dialog)

        if dialog.result:
            print("User confirmed removal of similar images.")
        else:
            print("User kept similar images.")
            images = all_images

        progress = LoadingDialog("Loading Dataset Into Memory", start_location=start_location)

        # Load dataset with unique images
        for image in tqdm(images, desc="Loading images to dataset"):
            image_name = os.path.basename(image)
            corresponding_label = next(
                (label for label in labels if image_to_label_path(image_name) in label), None
            )
            image = Image.open(image)

            annotations = []
            if corresponding_label:
                with open(corresponding_label, "r") as f:
                    for line in f:
                        try:
                            annotations.append(Annotation(line, data["names"]))
                        except ValueError:
                            print(f"Invalid annotation in {corresponding_label}")
                            continue
            else:
                annotations = None
            if annotations is not None and len(annotations) == 0:
                annotations = None

            # take off the extension from image name and put txt extension
            label_name = os.path.splitext(image_name)[0] + ".txt"

            button_frame.parent_window.data.append({"image": image, "annotations": annotations, "image_name": image_name, "label_name": os.path.basename(corresponding_label) if corresponding_label else label_name})

        # sort through data and find duplicate names, rename them
        image_names = [d["image_name"] for d in button_frame.parent_window.data]
        for i, d in enumerate(button_frame.parent_window.data):
            if image_names.count(d["image_name"]) > 1:
                d["image_name"] = f"{i}_{d['image_name']}"
                d["label_name"] = f"{i}_{d['label_name']}" if d["label_name"] else None

        print(f"Loaded {len(button_frame.parent_window.data)} images")

        # Load class names and colors from 'data.yaml'
        button_frame.parent_window.class_names = data["names"]
        button_frame.parent_window.class_colors = [
            "#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(button_frame.parent_window.class_names))
        ]

        print(f"Loaded {len(button_frame.parent_window.class_names)} class names")
        print(button_frame.parent_window.class_names)

        button_frame.next_button.configure(state="normal")
        button_frame.previous_button.configure(state="normal")
        button_frame.parent_window.next_image()
        button_frame.parent_window.image_frame.class_menu.configure(values=button_frame.parent_window.class_names)
        button_frame.parent_window.image_frame.class_menu.set(button_frame.parent_window.class_names[0])

        progress.close()


def load_raw_data(button_frame):
    start_location = button_frame.parent_window.get_center()
    data_paths = filedialog.askopenfiles(title="Select Raw Data File/s (image / video)")
    if data_paths:
        progress = LoadingDialog("Loading Raw Data...", start_location=start_location)
        for data_path in data_paths:
            if data_path.name.endswith((".jpg", ".jpeg", ".png")):
                image = Image.open(data_path.name)
                button_frame.parent_window.data.append({"image": image, "annotations": None})
            elif data_path.name.endswith((".mp4", ".avi", ".mov")):
                progress.close()
                images_per_second = float(ctk.CTkInputDialog(title="Images per second",
                                                             text="How many images per second should be extracted from the video?"
                                                             ).get_input())
                progress = LoadingDialog("Loading Video...", start_location=start_location)
                video = cv2.VideoCapture(data_path.name)
                # Get the frames per second (fps) of the video
                fps = video.get(cv2.CAP_PROP_FPS)

                # Calculate the frame interval for the desired images per second
                frame_interval = int(fps / images_per_second)

                success, image = video.read()
                count = 0
                while success:
                    if count % frame_interval == 0:
                        button_frame.parent_window.data.append(
                            {"image": Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), "annotations": None, "image_name": f"{count}.jpg", "label_name": f"{count}.txt"})
                    success, image = video.read()
                    count += 1
                progress.close()
                progress = LoadingDialog("Loading Raw Data...", start_location=start_location)
            else:
                print(f"Unsupported file type: {data_path.name}")

        image_names = [d["image_name"] for d in button_frame.parent_window.data]
        for i, d in enumerate(button_frame.parent_window.data):
            if image_names.count(d["image_name"]) > 1:
                d["image_name"] = f"{i}_{d['image_name']}"
                d["label_name"] = f"{i}_{d['label_name']}" if d["label_name"] else None

        progress.close()

        button_frame.next_button.configure(state="normal")
        button_frame.previous_button.configure(state="normal")
        button_frame.parent_window.next_image()
        button_frame.parent_window.image_frame.class_menu.configure(values=["None"])
        button_frame.parent_window.image_frame.class_menu.set("None")