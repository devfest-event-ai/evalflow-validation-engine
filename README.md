# EvalFlow - Clinical Validation Engine

## Overview
A production-grade validation engine designed for healthcare AI workflows. EvalFlow ingests unstructured clinical notes, extracts structured entities (medications, vitals), and validates the output using a custom FMR (False Match Rate) Confidence Scoring system.

## Architecture
Built with FastAPI, EvalFlow implements a strict validation pipeline:

1. Extraction Layer: Regex-based pattern matching for high-performance parsing.
2. Scoring Engine: Proprietary algorithm calculating confidence based on:
   - Completeness: Presence of critical fields (Meds, Vitals).
   - Pattern Quality: Strength of matched signals.
   - Consistency: Cross-field validation (e.g., Systolic > Diastolic).
3. Decision Layer: Auto-routing logic (approved, review_required, rejected).

## Tech Stack
- Backend: Python, FastAPI, Pydantic
- Validation: Custom Rule-Engine, FMR Scoring
- Docs: Swagger UI (OpenAPI 3.0)

## Key Features
- Zero-Config Extraction: Automatically detects BP and Medications from raw text.
- Smart Fallbacks: Low-confidence data is flagged for human review, preventing bad data pollution.
- Production Ready: Strictly typed schemas ensuring data integrity.

## API Usage
Run locally: `python main.py`
Docs: `http://localhost:8000/docs`
