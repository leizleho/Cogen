import os
from PIL import Image
from flask import url_for, current_app


def save_image(image, name):

    filename = image.filename
    # Grab extension type .jpg or .png
    ext_type = filename.split('.')[-1]
    storage_filename = str(name) + '.' + ext_type

    filepath = os.path.join(current_app.root_path,
                            'static\img', storage_filename)

    # Play Around with this size.
    output_size = (200, 200)

    # Open the picture and save it
    img = Image.open(image)
    img.thumbnail(output_size)
    img.save(filepath)

    return storage_filename
