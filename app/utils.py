import re
import os
from PIL import Image
from flask import url_for, current_app


def save_image(image, img_prefix):
    filename = image.filename
    print(filename)
    # Grab extension type .jpg or .png
    # ext_type = filename.split('.')[-1]
    # storage_filename = str(img_prefix) + '.' + ext_type
    storage_filename = str(img_prefix) + filename

    filepath = os.path.join(current_app.root_path,
                            'static', 'img', storage_filename)

    # Thumbnail size.
    output_size = (200, 200)

    # Open the picture and save it
    img = Image.open(image)
    img.thumbnail(output_size)
    img.save(filepath)

    return storage_filename


def snake_case(name):
    """Function to convert CamelCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_case(name):
    words = name.split('_')
    return ''.join((w.capitalize() for w in words))


def title_case(name):
    return name.replace("_", " ").title()
