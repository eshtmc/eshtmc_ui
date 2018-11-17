# -*- coding: utf-8 -*-
from PIL import Image
import face_recognition
import numpy as np
import os


def generate_images(path):
    image = face_recognition.load_image_file(path)
    face_locations = face_recognition.face_locations(image)
    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    if not os.path.exists(os.path.join(os.path.dirname(path), "images")):
        os.makedirs(os.path.join(os.path.dirname(path), "images"))
    for i, face_location in enumerate(face_locations):

        top, right, bottom, left = face_location

        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.thumbnail(face_image.shape * np.array(2), Image.ANTIALIAS)
        # pil_image.show()

        pil_image.save(os.path.join(
            os.path.dirname(path), 'images', str(i) + ".jpg"))


if __name__ == '__main__':
    basedir = os.path.dirname(__file__)
    path = os.path.join(
        basedir, "../../", "static/meeting_images/save_test/107/107.jpg")
    print(path)
    generate_images(path)