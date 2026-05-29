from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

# ============================================
# 1. FASTAPI APP INITIALIZATION
# ============================================
app = FastAPI(
    title="EvalFlow - Clinical Validation Engine",
    description="AI-powered validation framework for healthcare documentation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================
# 2. PYDANTIC SCHEMAS (Data Models)
# ============================================

class ClinicalNoteInput(BaseModel):
    """Input schema untuk clinical note"""
    note_id: str = Field(..., description="Unique identifier for the note")
    text: str = Field(..., description="Clinical note text content")
    category: str = Field(default="nursing", description="Note category: nursing, discharge, physician")
    timestamp: Optional[str] = None

class VitalSigns(BaseModel):
    """Schema untuk vital signs"""
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    temperature: Optional[float] = None

class Medication(BaseModel):
    """Schema untuk medication extraction"""
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None

class ExtractionResult(BaseModel):
    """Output schema untuk hasil extraction"""
    note_id: str
    medications: List[Medication] = []
    vital_signs: Optional[VitalSigns] = None
    diagnosis: Optional[str] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    validation_status: str = Field(..., description="pending, approved, review_required")
    processed_at: str
    # TAMBAHKAN BARIS INI
    fallback_action: Optional[dict] = None

class HealthCheck(BaseModel):
    """Schema untuk health check endpoint"""
    status: str
    version: str
    timestamp: str

# ============================================
# 3. API ENDPOINTS
# ============================================

@app.get("/", response_model=HealthCheck, tags=["Health"])
async def health_check():
    """
    Health check endpoint - memastikan API berjalan
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }
    
# ============================================
# 5. FMR CONFIDENCE SCORING ENGINE
# ============================================

def calculate_fmr_score(extracted_data: dict, note_text: str) -> dict:
    """
    Calculate False Match Rate (FMR) based confidence score
    
    Scoring Components:
    1. Completeness (40%): Apakah semua field penting ada?
    2. Pattern Match Quality (35%): Seberapa kuat pattern yang ditemukan?
    3. Cross-Field Consistency (25%): Apakah data konsisten?
    
    Returns:
        dict: {
            "overall_score": float (0.0-1.0),
            "completeness_score": float,
            "pattern_quality": float,
            "consistency_score": float,
            "issues": List[str]
        }
    """
    import re
    
    issues = []
    
    # ============================================
    # COMPONENT 1: COMPLETENESS (40%)
    # ============================================
    completeness_checks = {
        "has_medications": len(extracted_data.get("medications", [])) > 0,
        "has_vital_signs": extracted_data.get("vital_signs") is not None,
        "has_diagnosis": extracted_data.get("diagnosis") is not None,
    }
    
    completeness_score = sum(completeness_checks.values()) / len(completeness_checks)
    
    if not completeness_checks["has_medications"]:
        issues.append("No medications extracted")
    if not completeness_checks["has_vital_signs"]:
        issues.append("No vital signs extracted")
    
    # ============================================
    # COMPONENT 2: PATTERN MATCH QUALITY (35%)
    # ============================================
    pattern_score = 0.0
    pattern_count = 0
    
    # Check BP pattern strength
    bp_pattern = r'BP\s*(\d{2,3})/(\d{2,3})'
    if re.search(bp_pattern, note_text, re.IGNORECASE):
        pattern_score += 1.0
        pattern_count += 1
    
    # Check medication pattern strength
    med_pattern = r'(\w+)\s+(\d+mg)'
    med_matches = re.findall(med_pattern, note_text, re.IGNORECASE)
    if len(med_matches) > 0:
        # Bonus jika ada frequency
        freq_pattern = r'(daily|twice daily|as needed|every \d+ hours)'
        if re.search(freq_pattern, note_text, re.IGNORECASE):
            pattern_score += 1.0
        else:
            pattern_score += 0.5
        pattern_count += 1
    
    pattern_quality = pattern_score / max(pattern_count, 1)
    
    # ============================================
    # COMPONENT 3: CROSS-FIELD CONSISTENCY (25%)
    # ============================================
    consistency_score = 1.0
    
    # Rule: Jika ada diagnosis hypertension, harus ada BP tinggi
    vitals = extracted_data.get("vital_signs")
    diagnosis = extracted_data.get("diagnosis")
    
    if diagnosis == "Hypertension" and vitals:
        if vitals.get("bp_systolic", 0) < 130 and vitals.get("bp_diastolic", 0) < 80:
            consistency_score -= 0.3
            issues.append("Diagnosis hypertension but BP is normal")
    
    # Rule: BP systolic harus > diastolic
    if vitals:
        if vitals.get("bp_systolic", 0) <= vitals.get("bp_diastolic", 0):
            consistency_score -= 0.5
            issues.append("BP systolic <= diastolic (invalid)")
    
    # ============================================
    # CALCULATE OVERALL SCORE
    # ============================================
    overall_score = (
        completeness_score * 0.40 +
        pattern_quality * 0.35 +
        consistency_score * 0.25
    )
    
    return {
        "overall_score": round(overall_score, 2),
        "completeness_score": round(completeness_score, 2),
        "pattern_quality": round(pattern_quality, 2),
        "consistency_score": round(consistency_score, 2),
        "issues": issues
    }    

@app.post("/extract", response_model=ExtractionResult, tags=["Extraction"])
async def extract_clinical_data(note: ClinicalNoteInput):
    """
    Endpoint utama dengan FMR validation
    """
    import re
    from datetime import datetime
    
    # ... (kode extraction yang sudah ada tetap sama) ...
    # [Bagian extraction medication & BP tetap sama seperti sebelumnya]
    
    text = note.text
    meds_found = []
    vitals = None
    
    # 1. Extract Medications
    med_pattern = r'(\w+)\s+(\d+mg)'
    matches = re.findall(med_pattern, text, re.IGNORECASE)
    
    for match in matches:
        meds_found.append({
            "name": match[0],
            "dosage": match[1],
            "frequency": "daily"
        })
    
    # 2. Extract Blood Pressure
    bp_pattern = r'BP\s*(\d{2,3})/(\d{2,3})'
    bp_match = re.search(bp_pattern, text, re.IGNORECASE)
    
    if bp_match:
        vitals = {
            "bp_systolic": int(bp_match.group(1)),
            "bp_diastolic": int(bp_match.group(2)),
            "heart_rate": None,
            "temperature": None
        }
    
    # 3. Build extracted data dict
    extracted_data = {
        "medications": meds_found,
        "vital_signs": vitals,
        "diagnosis": "Hypertension" if vitals and vitals.get("bp_systolic", 0) > 130 else None
    }
    
        # ... (kode extraction sebelumnya tetap sama) ...

    # 4. CALL FMR SCORING ENGINE
    fmr_result = calculate_fmr_score(extracted_data, text)

    # 5. Determine validation status & Fallback Action
    fallback_action = None
    validation_status = "pending" # Default

    if fmr_result["overall_score"] >= 0.7:
        validation_status = "approved"
        # Tidak perlu action, langsung approved

    elif fmr_result["overall_score"] >= 0.4:
        validation_status = "review_required"
        # FALLBACK: Score sedang -> Minta review manusia
        fallback_action = {
            "action": "route_to_human_review",
            "reason": "Confidence score moderate. Data partially extracted.",
            "priority": "medium"
        }
    
    else:
        validation_status = "rejected"
        # FALLBACK: Score rendah -> Tolak / Minta input ulang
        fallback_action = {
            "action": "request_re_submission",
            "reason": "Data too incomplete or inconsistent for extraction.",
            "priority": "high"
        }

    # 6. Return Result (Jangan lupa sertakan fallback_action!)
    return {
        "note_id": note.note_id,
        "medications": meds_found,
        "vital_signs": vitals,
        "diagnosis": extracted_data["diagnosis"],
        "confidence_score": fmr_result["overall_score"],
        "validation_status": validation_status,
        "fallback_action": fallback_action, # <--- PENTING
        "processed_at": datetime.now().isoformat()
    }


@app.get("/docs-info", tags=["Documentation"])
async def docs_info():
    """Informasi dokumentasi API"""
    return {
        "message": "EvalFlow API Documentation",
        "swagger_ui": "/docs",
        "redoc": "/redoc",
        "health_check": "/",
        "extract_endpoint": "/extract"
    }

# ============================================
# 4. RUN SERVER
# ============================================

if __name__ == "__main__":
    print("🚀 Starting EvalFlow API Server...")
    print("📚 Docs available at: http://localhost:8000/docs")
    print("❤️  Health check at: http://localhost:8000/")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )