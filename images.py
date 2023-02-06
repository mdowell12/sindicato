import os
import sys

from PIL import Image


ARTICLE_IMAGE_WIDTH = 2240
ARTICLE_IMAGE_HEIGHT = 1260
RESIZED_FILENAME_SUFFIX = "-resized"


def run():
    images_folder = sys.argv[1] if len(sys.argv) > 1 else None
    if images_folder is None or not os.path.isdir(images_folder):
        print("Must supply image folder")
        return
    images_folder_full_path = os.path.abspath(images_folder)
    files = os.listdir(images_folder_full_path)
    for file in files:
        filename = file.lower()
        if not (filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg")):
            print(f"Skipping file {file}")
            continue
        with Image.open(os.path.join(images_folder_full_path, file)) as im:
            (width, height) = (ARTICLE_IMAGE_WIDTH, int(im.height * (ARTICLE_IMAGE_WIDTH / im.width)))
            im_resized = im.resize((width, height))
        new_filename = "".join(file.split('.')[:-1]) + RESIZED_FILENAME_SUFFIX + "." + file.split('.')[-1]
        im_resized.save(os.path.join(images_folder_full_path, new_filename))
        print(f"Resized {file} and saved as {new_filename}")


if __name__ == "__main__":
    run()
