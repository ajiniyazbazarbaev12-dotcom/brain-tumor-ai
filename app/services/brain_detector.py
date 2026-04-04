from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from app.utils.image_preprocessing import preprocess_image

def build_mri_model():
    base_model = ResNet50(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    output = Dense(1, activation="sigmoid")(x)

    model = Model(inputs=base_model.input, outputs=output)
    return model


# build + load weights
model = build_mri_model()
model.load_weights("app/models/mri_detector.weights.h5")

LOW_THRESHOLD = 0.2
HIGH_THRESHOLD = 0.8

def detect_brain_mri(file):
    img = preprocess_image(file)

    prediction = model.predict(img)[0][0]

    if prediction < LOW_THRESHOLD:
        return {
            "status": "brain_mri",
            "confidence": float(1 - prediction),
        }

    elif prediction > HIGH_THRESHOLD:
        return {
            "status": "not_brain",
            "confidence": float(prediction)
        }

    else:
        return {
            "status": "uncertain",
            "confidence": float(max(prediction, 1-prediction))
        }