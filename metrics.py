"""
Metrics Engine - Calculate Precision, Recall, F1-Score
for evaluating extraction performance against ground truth.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import json
import re


@dataclass
class MetricResult:
    """Result dari perhitungan metrics"""
    precision: float
    recall: float
    f1_score: float
    total_samples: int
    correct_extractions: int
    missed_extractions: int
    false_extractions: int


def normalize_medication_name(med_str: str) -> str:
    """
    Normalize medication name untuk matching yang lebih baik.
    Contoh: "Lisinopril 10mg" -> "lisinopril 10mg"
    """
    return med_str.lower().strip()


def extract_meds_from_prediction(pred: Dict) -> set:
    """Extract medications dari prediction result"""
    meds = set()
    for med in pred.get("medications", []):
        name = med.get("name", "").strip()
        dosage = med.get("dosage", "").strip()
        if name:
            meds.add(normalize_medication_name(f"{name} {dosage}"))
    return meds

def extract_meds_from_ground_truth(truth: Dict) -> set:
    """
    Extract medications dari ground truth.
    Menangani struktur data_test.json di mana nama obat dan dosis terpisah.
    """
    meds = set()
    gt_data = truth.get("ground_truth", truth)
    
    # Ambil list nama obat dan list dosis
    names = gt_data.get("medications", [])
    dosages = gt_data.get("dosages", [])
    
    # Gabungkan secara berpasangan (index 0 dengan 0, 1 dengan 1)
    for i in range(len(names)):
        name = names[i].lower().strip() if i < len(names) else ""
        dosage = dosages[i].lower().strip() if i < len(dosages) else ""
        
        if name:
            # Gabungkan menjadi format yang sama dengan output API (misal: "lisinopril 10mg")
            meds.add(f"{name} {dosage}".strip())
            
    return meds

def calculate_metrics(predictions: List[Dict], ground_truth: List[Dict]) -> MetricResult:
    """
    Calculate precision, recall, dan F1-score
    
    Args:
        predictions: List of extraction results dari API
        ground_truth: List of ground truth data
    
    Returns:
        MetricResult dengan semua metrics
    """
    total_true_positives = 0
    total_false_positives = 0
    total_false_negatives = 0
    
    for pred, truth in zip(predictions, ground_truth):
        # Extract medications
        pred_meds = extract_meds_from_prediction(pred)
        truth_meds = extract_meds_from_ground_truth(truth)
        
        # Calculate untuk sample ini
        true_positives = len(pred_meds.intersection(truth_meds))
        false_positives = len(pred_meds - truth_meds)
        false_negatives = len(truth_meds - pred_meds)
        
        total_true_positives += true_positives
        total_false_positives += false_positives
        total_false_negatives += false_negatives
    
    # Calculate precision, recall, F1
    precision = total_true_positives / (total_true_positives + total_false_positives) if (total_true_positives + total_false_positives) > 0 else 0.0
    recall = total_true_positives / (total_true_positives + total_false_negatives) if (total_true_positives + total_false_negatives) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return MetricResult(
        precision=round(precision, 3),
        recall=round(recall, 3),
        f1_score=round(f1_score, 3),
        total_samples=len(predictions),
        correct_extractions=total_true_positives,
        missed_extractions=total_false_negatives,
        false_extractions=total_false_positives
    )


def export_metrics_to_json(metrics: MetricResult, filename: str = "metrics_report.json"):
    """Export metrics ke JSON file"""
    metrics_dict = {
        "precision": metrics.precision,
        "recall": metrics.recall,
        "f1_score": metrics.f1_score,
        "total_samples": metrics.total_samples,
        "correct_extractions": metrics.correct_extractions,
        "missed_extractions": metrics.missed_extractions,
        "false_extractions": metrics.false_extractions,
        "performance_rating": "Excellent" if metrics.f1_score >= 0.9 else 
                             "Good" if metrics.f1_score >= 0.7 else 
                             "Fair" if metrics.f1_score >= 0.5 else "Poor"
    }
    
    with open(filename, 'w') as f:
        json.dump(metrics_dict, f, indent=2)
    
    print(f"Metrics exported to {filename}")
    return metrics_dict


if __name__ == "__main__":
    # Test metrics engine dengan sample data
    sample_predictions = [
        {
            "medications": [
                {"name": "Lisinopril", "dosage": "10mg"},
                {"name": "Metformin", "dosage": "500mg"}
            ]
        }
    ]
    
    sample_ground_truth = [
        {
            "ground_truth": {
                "medications": ["Lisinopril 10mg", "Metformin 500mg"]
            }
        }
    ]
    
    result = calculate_metrics(sample_predictions, sample_ground_truth)
    print(f"Precision: {result.precision}")
    print(f"Recall: {result.recall}")
    print(f"F1-Score: {result.f1_score}")