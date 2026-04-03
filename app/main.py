from fastapi import FastAPI, UploadFile, File, Form
from app.services.brain_detector import detect_brain_mri
from app.services.tumor_predictor import predict_tumor
from app.database.db import init_db, get_connection
from enum import Enum

import uuid
import os

app = FastAPI(title="Brain Tumor Detection API")

# create feedback folder
FEEDBACK_DIR = "app/feedback"
os.makedirs(FEEDBACK_DIR, exist_ok=True)

# init DB
init_db()

class TumorType(str, Enum):
    glioma = "glioma"
    meningioma = "meningioma"
    pituitary = "pituitary"
    notumor = "notumor"


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_bytes = await file.read()

    brain_result = detect_brain_mri(file_bytes)

    if brain_result["status"] == "not_brain":
        return {
            "status": "not_brain",
            "message": "Not a brain MRI",
            "confidence": brain_result["confidence"]
        }

    elif brain_result["status"] == "uncertain":
        return {
            "status": "uncertain",
            "message": "Model uncertain",
            "confidence": brain_result["confidence"]
        }

    tumor_result = predict_tumor(file_bytes)

    return {
        "status": "success",
        **tumor_result
    }


@app.post("/feedback")
async def feedback(
    file: UploadFile = File(...),
    predicted: TumorType = Form(...),
    actual: TumorType = Form(...)
):
    file_bytes = await file.read()

    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(FEEDBACK_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (image_path, predicted_label, actual_label)
        VALUES (?, ?, ?)
    """, (file_path, predicted, actual))

    conn.commit()
    conn.close()

    return {"status": "saved"}

@app.delete("/feedback/{id}")
def delete_feedback(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # get image path first
    cursor.execute("SELECT image_path FROM feedback WHERE id=?", (id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return {"status": "error", "message": "Feedback not found"}

    image_path = row[0]

    # delete image if exists
    if os.path.exists(image_path):
        os.remove(image_path)

    # delete DB record
    cursor.execute("DELETE FROM feedback WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return {"status": "deleted"}

@app.get("/feedback")
def get_feedback():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM feedback")
    rows = cursor.fetchall()

    conn.close()

    return {"data": rows}