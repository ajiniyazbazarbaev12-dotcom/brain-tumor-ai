import numpy as np
from PIL import Image
from io import BytesIO
from tensorflow.keras.applications.resnet50 import preprocess_input

def preprocess_image(file_bytes):
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    image = image.resize((224, 224))

    image = np.array(image)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    return image