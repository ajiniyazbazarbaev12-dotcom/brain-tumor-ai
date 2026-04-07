import React, { useState } from "react";
import { predictTumor, sendFeedback } from "./api";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [actual, setActual] = useState("");
  const [showFeedback, setShowFeedback] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleUpload = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setResult(null);
    setShowFeedback(false);

    if (selectedFile) {
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handlePredict = async () => {
    if (!file) return alert("Upload image first");

    setLoading(true);

    try {
      const res = await predictTumor(file);
      setResult(res.data);
    } catch (error) {
      console.error("FULL ERROR:", error);
      console.error("RESPONSE:", error.response);
      alert("Error predicting");
    }

    setLoading(false);
  };

  const handleFeedback = async () => {
    if (!actual) return alert("Select correct label");

    try {
      await sendFeedback(file, result.tumor_type, actual);
      alert("Feedback saved");
      setShowFeedback(false);
    } catch (err) {
      console.error(err);
      alert("Error saving feedback");
    }
  };

  const getConfidenceClass = (confidence) => {
    if (confidence > 0.85) return "high";
    if (confidence > 0.6) return "medium";
    return "low";
  };

  return (
    <div className="container">
      <h1>Brain Tumor Detection</h1>

      {/* Buttons */}
      <div className="top-actions">
        <label className="upload-btn">
          Upload MRI Image
          <input type="file" onChange={handleUpload} hidden />
        </label>

        <button className="predict-btn" onClick={handlePredict}>
          Predict
        </button>
      </div>

      {file && <p className="file-name">{file.name}</p>}

      {/* Preview */}
      {preview && (
        <div className="preview-container">
          <img src={preview} alt="Preview" />
        </div>
      )}

      {/* Loader */}
      {loading && <div className="loader"></div>}

      {/* Result */}
      {result && !loading && (
        <div className="card">
          <h3>Prediction Result</h3>

          {/* Not brain */}
          {result.status === "not_brain" && (
            <div className="warning">
              <p> Not a brain MRI</p>
              <p>
                Confidence:{" "}
                <strong>{Number(result.confidence).toFixed(3)}</strong>
              </p>
            </div>
          )}

          {/* 🟡 Uncertain */}
          {result.status === "uncertain" && (
            <div className="warning">
              <p>Model is not confident</p>
              <p>Please upload a clearer brain MRI image</p>
            </div>
          )}

          {/* 🟢 Success */}
          {result.status === "success" && (
            <>
              <div className="result-box">
                <div className="result-item">
                  <span>Detected Type</span>
                  <strong className="highlight">
                    {result.tumor_type}
                  </strong>
                </div>

                <div className="result-item">
                  <span>Confidence</span>
                  <strong className={getConfidenceClass(result.confidence)}>
                    {Number(result.confidence).toFixed(3)}
                  </strong>
                </div>
              </div>

              {!showFeedback && (
                <button
                  className="feedback-trigger"
                  onClick={() => setShowFeedback(true)}
                >
                  Not correct? Help us improve
                </button>
              )}

              {showFeedback && (
                <div className="feedback-card">
                  <p className="feedback-title">Select correct label</p>

                  <select
                    className="styled-select"
                    onChange={(e) => setActual(e.target.value)}
                  >
                    <option value="">Choose label</option>
                    <option value="glioma">Glioma</option>
                    <option value="meningioma">Meningioma</option>
                    <option value="pituitary">Pituitary</option>
                    <option value="notumor">No Tumor</option>
                  </select>

                  <button className="submit-btn" onClick={handleFeedback}>
                    Submit Feedback
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;