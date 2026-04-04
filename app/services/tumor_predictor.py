import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from app.utils.image_preprocessing import preprocess_image

def build_tumor_model():
    base_model = ResNet50(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation="relu")(x)
    x = Dropout(0.6)(x)
    x = Dense(128, activation="relu")(x)
    outputs = Dense(4, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    return model


# build + load weights
model = build_tumor_model()
model.load_weights("app/models/brain_tumor.weights.h5")


CLASSES = ['glioma', 'meningioma', 'notumor', 'pituitary']


def predict_tumor(file):
    img = preprocess_image(file)

    prediction = model.predict(img)[0]
    class_index = np.argmax(prediction)

    return {
        "tumor_type": CLASSES[class_index],
        "confidence": float(prediction[class_index])
    }