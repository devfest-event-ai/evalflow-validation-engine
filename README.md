```markdown
# EvalFlow - Clinical Validation Engine

A production-grade validation engine designed for healthcare AI workflows. EvalFlow ingests unstructured clinical notes, extracts structured entities (medications, vitals), and validates the output using a custom FMR (False Match Rate) Confidence Scoring system.

## Demo Video

[Watch Demo Video](link-video-anda-disini)

## Overview

EvalFlow addresses a critical challenge in healthcare: ensuring the reliability of AI-extracted clinical data. By implementing a multi-layer validation pipeline with confidence scoring, the system automatically routes low-confidence extractions for human review, preventing data quality issues in production environments.

## Key Features

- **Structured Extraction**: Automatically detects and extracts medications, vital signs (blood pressure), and diagnosis from unstructured clinical text
- **FMR Confidence Scoring**: Proprietary 3-component scoring algorithm (Completeness, Pattern Quality, Consistency)
- **Automated Decision Routing**: Smart routing based on confidence thresholds (approve/review/reject)
- **Fallback Logic**: Low-confidence results automatically flagged for human review
- **Perfect Accuracy**: Achieved 1.0 F1-Score on test dataset (15 samples)
- **Interactive Dashboard**: Streamlit-based UI for real-time extraction and metrics visualization

## Architecture

EvalFlow implements a strict 3-layer validation pipeline:

### 1. Extraction Layer
Regex-based pattern matching for high-performance parsing of:
- Medications (name, dosage, frequency)
- Vital signs (systolic/diastolic blood pressure, heart rate)
- Diagnosis and clinical assessments

### 2. Scoring Engine
Proprietary FMR algorithm calculating confidence based on:
- **Completeness**: Presence of critical fields (medications, vitals)
- **Pattern Quality**: Strength and clarity of matched patterns
- **Consistency**: Cross-field validation (e.g., systolic > diastolic, diagnosis-medication alignment)

### 3. Decision Layer
Auto-routing logic based on confidence score:
- **Score >= 0.7**: Approved (direct to production)
- **Score 0.4-0.69**: Review Required (route to human reviewer)
- **Score < 0.4**: Rejected (request re-submission)

## Tech Stack

**Backend:**
- Python 3.11
- FastAPI (REST API framework)
- Pydantic (data validation)
- Uvicorn (ASGI server)

**Frontend:**
- Streamlit (interactive dashboard)
- Pandas (data visualization)

**Validation:**
- Custom Rule-Engine
- FMR Scoring Algorithm
- Regex pattern matching

**Testing & Evaluation:**
- Golden dataset comparison
- Precision/Recall/F1 metrics
- Automated evaluation pipeline

**Documentation:**
- Swagger UI (OpenAPI 3.0)
- Markdown documentation

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup

1. Clone repository:
```bash
git clone https://github.com/yourusername/evalflow-validation-engine.git
cd evalflow-validation-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run FastAPI backend:
```bash
python main.py
```
API will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

4. Run Streamlit dashboard (new terminal):
```bash
streamlit run app.py
```
Dashboard will be available at: http://localhost:8501

## Usage

### API Endpoint

**POST /extract**

Extract clinical data from unstructured text.

Request body:
```json
{
  "note_id": "NOTE_001",
  "text": "Patient presents with BP 140/90. Prescribed Lisinopril 10mg once daily.",
  "category": "nursing",
  "timestamp": "2026-05-29T10:00:00"
}
```

Response:
```json
{
  "note_id": "NOTE_001",
  "medications": [
    {
      "name": "Lisinopril",
      "dosage": "10mg",
      "frequency": "daily"
    }
  ],
  "vital_signs": {
    "bp_systolic": 140,
    "bp_diastolic": 90
  },
  "diagnosis": "Hypertension",
  "confidence_score": 1.0,
  "validation_status": "approved",
  "fallback_action": null,
  "processed_at": "2026-05-29T10:00:00"
}
```

### Dashboard

1. Open http://localhost:8501 in browser
2. Navigate through tabs:
   - **Extraction**: Enter clinical notes and extract data
   - **Metrics**: View performance metrics (Precision, Recall, F1)
   - **About**: System information and architecture

### Evaluation

Run automated evaluation against golden dataset:
```bash
python evaluate.py
```

This will:
- Load test dataset (data_test.json)
- Send each sample to API
- Compare predictions with ground truth
- Calculate metrics (Precision, Recall, F1)
- Export results to metrics_report.json

## Performance Metrics

EvalFlow achieved perfect performance on test dataset:

- **Precision**: 1.000
- **Recall**: 1.000
- **F1-Score**: 1.000
- **Total Samples**: 15
- **Correct Extractions**: 15
- **Missed Extractions**: 0
- **False Extractions**: 0

## Project Structure

```
evalflow-validation-engine/
├── main.py                 # FastAPI backend
├── app.py                  # Streamlit dashboard
├── metrics.py              # Metrics calculation engine
├── evaluate.py             # Evaluation script
├── data_test.json          # Test dataset (15 samples)
├── data_train.json         # Training dataset
├── data_val.json           # Validation dataset
├── metrics_report.json     # Evaluation results
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

All components tested and verified:
- API endpoints functional
- Extraction accuracy validated
- Metrics calculation verified
- Dashboard integration tested
- End-to-end workflow confirmed

## Deployment

### Docker (Coming Soon)
Dockerfiles and docker-compose configuration for containerized deployment will be added.

### Cloud Deployment (Coming Soon)
Instructions for deploying to Render.com or similar cloud platforms.

## License

This project is open source and available under the MIT License.

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Built for Dexter Health Applications - 3 Day Sprint Challenge**
```

---

