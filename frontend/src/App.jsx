import React, { useMemo, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const humanReadableApiBase = useMemo(() => API_BASE.replace(/\/$/, ''), [])

  const handleFileChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    setSelectedFile(file)
    setError('')
    setResult(null)
    setPreviewUrl(URL.createObjectURL(file))
  }

  const handlePredict = async () => {
    if (!selectedFile) {
      setError('Please choose an image first.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch(`${humanReadableApiBase}/predict`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Prediction failed.')
      }

      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong during prediction.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <div className="card">
        <div className="hero">
          <span className="badge">Production-ready UI</span>
          <h1>Dog Breed Predictor</h1>
          <p>Upload a dog image to classify the breed through the FastAPI backend.</p>
        </div>

        <div className="panel">
          <label className="upload-box">
            <input type="file" accept="image/png,image/jpeg,image/jpg" onChange={handleFileChange} />
            <span>{selectedFile ? selectedFile.name : 'Choose JPG or PNG image'}</span>
          </label>

          {previewUrl && (
            <div className="preview-wrap">
              <img className="preview-image" src={previewUrl} alt="Preview" />
            </div>
          )}

          <button className="predict-button" onClick={handlePredict} disabled={loading || !selectedFile}>
            {loading ? 'Predicting...' : 'Predict Breed'}
          </button>
        </div>

        {error && <div className="message error">{error}</div>}

        {result && (
          <div className="result-panel">
            <h2>Prediction Result</h2>
            <div className="result-row">
              <span>Predicted Breed</span>
              <strong>{result.predicted_breed}</strong>
            </div>
            <div className="result-row">
              <span>Confidence</span>
              <strong>{result.confidence}%</strong>
            </div>

            <div className="probability-list">
              {Object.entries(result.all_probabilities || {}).slice(0, 5).map(([breed, score]) => (
                <div key={breed} className="probability-item">
                  <span>{breed}</span>
                  <span>{score}%</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
