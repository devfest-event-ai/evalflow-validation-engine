# FMR Validation Logic (False Match Rate)

## Goal
Calculate confidence score for LLM extraction.

## Scoring Rules (0.0 - 1.0)
1. **Completeness (40%)**: Did we extract all required fields? (Medication, Dosage, Vitals)
2. **Format (30%)**: Is the output valid JSON? Does it match Pydantic schema?
3. **Consistency (30%)**: 
   - If "BP" is present, systolic must be > diastolic.
   - If "Medication" is present, "Dosage" must be present.

## Fallback Logic
- If Score < 0.7 → Flag for Human Review.
- If Score >= 0.7 → Auto-approve.