import importlib
import os
import traceback

import yaml
from tqdm import tqdm

from dialogs.augment_selector_dialog import AugmentSelectorDialog
from dialogs.image_separation_dialog import ImageSeparationDialog
from dialogs.loading_dialog import LoadingDialog

import random


def copy_images(data_list, destination_path, description):
    """
    Copies images and their corresponding annotations to the specified directory.

    :param data_list: List of data dictionaries containing image and annotation details.
    :param destination_path: Base path where images and labels will be stored.
    :param description: Description for the tqdm progress bar.
    """
    for data in tqdm(data_list, desc=f"Copying {description} images"):
        try:
            # Handle annotations
            if data["annotations"] is not None:
                label_name = data["label_name"]
                if data.get("augment_value", None) is not None:
                    label_name = f"{data['label_name'][:-4]}_{data['augment_value']}.txt"
                label_path = os.path.join(destination_path, "labels", label_name)

                # print error if path already exists
                if os.path.exists(label_path):
                    print(f"Error: {label_path} already exists")
                    continue

                with open(label_path, "w") as f:
                    for annotation in data["annotations"]:
                        f.write(annotation.to_yolo_format() + "\n")

            # Handle image names
            image_name = data["image_name"]
            if data.get("augment_value", None) is not None:
                image_extension = image_name.split(".")[-1]
                image_name_no_extension = ".".join(image_name.split(".")[:-1])
                image_name = f"{image_name_no_extension}_{data['augment_value']}.{image_extension}"

            if os.path.exists(os.path.join(destination_path, "images", image_name)):
                print(f"Error: {os.path.join(destination_path, 'images', image_name)} already exists")
                continue

            # Save image
            image_path = os.path.join(destination_path, "images", image_name)
            data["image"].save(image_path)
        except Exception:
            print(f"Error processing label: {data.get('label_name', 'Unknown')}")
            traceback.print_exc()


def export_dataset(parent_window, ctk):
    if len(parent_window.data) == 0:
        ctk.messagebox.showerror("Error", "No dataset loaded.")
        return

    data_copy = parent_window.data.copy()

    # randomize the data order
    random.shuffle(parent_window.data)

    # get the export location that the dataset folder will be saved to
    export_location = ctk.filedialog.askdirectory(title="Select export location")

    dataset_name = ctk.CTkInputDialog(text="Enter dataset name", title="Dataset Name").get_input()

    augment_options = []
    for root, dirs, files in os.walk("augments"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                augment_options.append(file[:-3])

    augments = AugmentSelectorDialog(parent_window, augment_options, parent_window.get_center())
    parent_window.wait_window(augments)
    augments = augments.selected_augments

    for augment in augments:
        try:
            dialog = LoadingDialog(f"Applying {augment} augment", parent_window.get_center())
            augment_module = importlib.import_module(f"augments.{augment}")
            augment_function = getattr(augment_module, augment)
            parent_window.data = augment_function(parent_window.data)
            dialog.close()
        except Exception as e:
            print(f"Error applying {augment} augment: {e}")
            try:
                dialog.close()
            except NameError:
                pass

    if export_location == "":
        return
    else:
        os.mkdir(os.path.join(export_location, dataset_name))

        # make readme.dataset.txt file
        with open(os.path.join(export_location, dataset_name, "README.dataset.txt"), "w") as f:
            f.write("Dataset created with Scythe Engineering Dataset Annotator and Viewer\n")
            f.write("Number of images: {}\n".format(len(parent_window.data)))
            f.write("Classes: {}\n".format(", ".join(parent_window.class_names)))

        # make data.yaml file
        with open(os.path.join(export_location, dataset_name, "data.yaml"), "w") as f:
            yaml.dump({"train": "../train/images",
                       "val": "../validate/images",
                       "test": "../test/images",
                       "nc": len(parent_window.class_names),
                       "names": parent_window.class_names}, f)

        image_separation_dialog = ImageSeparationDialog(parent_window, parent_window.get_center())
        parent_window.wait_window(image_separation_dialog)

        train_percentage = image_separation_dialog.train_percentage
        test_percentage = image_separation_dialog.test_percentage

        number_of_train_images = int(len(parent_window.data) * train_percentage / 100)
        number_of_test_images = int(len(parent_window.data) * test_percentage / 100)

        train_data = parent_window.data[:number_of_train_images]
        test_data = parent_window.data[number_of_train_images:number_of_train_images + number_of_test_images]
        validate_data = parent_window.data[number_of_train_images + number_of_test_images:]

        # make the train, test, and validate directories
        os.mkdir(os.path.join(export_location, dataset_name, "train"))
        os.mkdir(os.path.join(export_location, dataset_name, "train", "images"))
        os.mkdir(os.path.join(export_location, dataset_name, "train", "labels"))

        os.mkdir(os.path.join(export_location, dataset_name, "test"))
        os.mkdir(os.path.join(export_location, dataset_name, "test", "images"))
        os.mkdir(os.path.join(export_location, dataset_name, "test", "labels"))

        os.mkdir(os.path.join(export_location, dataset_name, "validate"))
        os.mkdir(os.path.join(export_location, dataset_name, "validate", "images"))
        os.mkdir(os.path.join(export_location, dataset_name, "validate", "labels"))

        train_path = os.path.join(export_location, dataset_name, "train")
        test_path = os.path.join(export_location, dataset_name, "test")
        validate_path = os.path.join(export_location, dataset_name, "validate")

        dialog = LoadingDialog("Copying Images", parent_window.get_center())

        copy_images(train_data, train_path, "train")
        copy_images(test_data, test_path, "test")
        copy_images(validate_data, validate_path, "validate")

        dialog.close()

    parent_window.data = data_copy
