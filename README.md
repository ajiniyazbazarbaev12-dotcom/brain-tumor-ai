# Brain Tumor Detection AI

A full-stack AI-powered medical imaging web application for automated **brain MRI validation** and **brain tumor classification** using deep learning.

The platform helps users upload MRI scans and receive AI-assisted predictions through an interactive web interface.

## Core System Components

- **FastAPI Backend** – Handles REST API requests and model inference
- **React Frontend** – Provides a modern user interface for image upload and prediction results
- **TensorFlow / Keras Models** – Performs medical image analysis using deep learning

## AI Pipeline

Two separate models are used:

1. **MRI Detector Model** – Verifies whether the uploaded image is a valid brain MRI scan  
2. **Tumor Classification Model** – Predicts tumor type from valid MRI images


# Features

## Frontend
- Modern React-based user interface
- Easy MRI image upload system
- Real-time prediction results display
- Confidence score visualization
- Clean and user-friendly experience

## Backend
- FastAPI REST API architecture
- Real-time model inference
- Feedback collection system
- SQLite database integration
- Modular backend structure

## AI Capabilities
- Brain MRI image validation
- Multi-class tumor classification
- Confidence score generation
- Automated image preprocessing
- Fast prediction response time


# Tumor Classes

The classification model predicts one of the following categories:

- **Glioma** – Tumor that develops in the glial cells of the brain  
- **Meningioma** – Tumor that forms in the meninges surrounding the brain and spinal cord  
- **Pituitary** – Tumor located in the pituitary gland region  
- **No Tumor** – No detectable tumor pattern found in the MRI scan


# Tech Stack

## Frontend
- React.js
- JavaScript
- HTML5
- CSS3
- Axios / Fetch API

## Backend
- FastAPI
- Uvicorn
- Python

## Deep Learning / AI
- TensorFlow
- Keras
- ResNet50 (Transfer Learning)
- NumPy
- OpenCV
- Pillow

## Database
- SQLite

## Tools / Deployment
- GitHub
- Git
- Virtual Environment (venv)
- Cloud Deployment Ready


# Project Structure

```text
brain-tumor-ai/
│
├── app/                        # FastAPI backend
│   ├── main.py                 # Main API entry point
│   ├── services/              # Prediction and business logic
│   ├── utils/                 # Image preprocessing utilities
│   ├── models/                # AI model files / loaders
│   ├── database/             # SQLite database logic
│   └── feedback/             # Feedback handling system
│
├── frontend/                  # React frontend
│   ├── src/                  # Frontend source code
│   ├── public/               # Static assets
│   └── build/                # Production build files
│
├── requirements.txt          # Python dependencies
├── package.json              # Frontend dependencies
├── package-lock.json         # Locked npm versions
├── runtime.txt               # Deployment runtime version
├── .gitignore                # Ignored files/folders
└── README.md
``` 
# Installation & Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/ajiniyaz-dev/brain-tumor-ai.git
cd brain-tumor-ai
```

## 2. Backend Setup (FastApi)
``` bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 3. Frontend Setup (React)
``` bash
cd frontend
npm install
npm start
```

## 4. How to Use
  1. Open the frontend in your browser
  2. Upload a brain MRI image
  3. The system validates whether the image is a brain MRI
  4. If valid, the tumor classifier predicts the tumor type
  5. Confidence scores are displayed to the user

# API Endpoints
## Base URL
http://127.0.0.1:8000

## Available Routes
### GET /
Checks whether the API server is running.

Response:
{
  "message": "API running"
}

### POST /predict
Uploads an MRI image and returns prediction results.
Input: image file
Possible Responses:
{
  "status": "not_brain",
  "message": "Not a brain MRI",
  "confidence": 0.94
}

{
  "status": "uncertain",
  "message": "Model uncertain",
  "confidence": 0.61
}

{
  "status": "success",
  "prediction": "Glioma",
  "confidence": 0.97
}

### POST /feedback
Stores user correction feedback for future model improvement.
Form Data:
- file
- predicted
- actual

Response:

{
  "status": "saved"
}

### GET /feedback
Returns all stored feedback records.

### DELETE /feedback/{id}
Deletes feedback record by ID.

Response:
{
  "status": "deleted"
}

## Interactive API Docs
http://127.0.0.1:8000/docs


# Model Information & Performance

## AI Architecture

The project uses two separate deep learning models based on **ResNet50 transfer learning** with TensorFlow / Keras.

### 1. MRI Detector Model

A binary classification model used to verify whether the uploaded image is a valid **brain MRI scan** before tumor prediction.

Classes:

- Brain MRI
- Other / Non-brain image

### 2. Tumor Classification Model

A multi-class classification model used after MRI validation.

Classes:

- Glioma
- Meningioma
- Pituitary
- No Tumor

---

## Dataset Sources

### MRI Detector Model

Built using a combination of:

- Kaggle Brain Tumor MRI dataset
- Additional collected brain MRI images
- Other MRI / medical image datasets (non-brain scans)

### Tumor Classification Model

Built by combining two public Kaggle brain tumor MRI datasets.

---

## Preprocessing & Data Augmentation

The models were trained using image preprocessing and augmentation techniques such as:

- Image resizing to 224x224
- ResNet50 preprocessing pipeline
- CLAHE contrast enhancement
- Rotation augmentation
- Zoom augmentation
- Width / height shifting
- Brightness adjustment
- Shear transformation
- Horizontal flipping (MRI detector model)

---

## Training Strategy

- Transfer learning with pretrained ResNet50 weights
- Fine-tuning last layers of the network
- Adam optimizer
- Early stopping
- Model checkpoint saving
- Class weighting for imbalanced classes
- Validation split and test evaluation

---

## Performance

### MRI Detector Model

- Near 100% test accuracy  
- Binary classification task with strong separation between classes

### Tumor Classification Model

- Approximately **97% test accuracy**

---

## Notes

The MRI validation model helps prevent invalid uploads and improves reliability by ensuring only brain MRI scans are passed to the tumor classifier.

