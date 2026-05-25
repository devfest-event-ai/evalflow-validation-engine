import json
import random

# Template Clinical Notes
NOTES = [
    "Patient P{id} admitted on {date}. Meds: {med1} {dose1} {freq1}. Vitals: BP {bp}/80, HR {hr}. Assessment: stable. Plan: discharge.",
    "Nursing note: Patient reports {symptom}. Administered {med2} {dose2}. Vitals stable. Monitoring.",
    "Discharge summary for P{id}. Diagnosis: {diag}. Discharge meds: {med3} {dose3}. Follow up in {days} days."
]

MEDS = ["Lisinopril", "Metformin", "Aspirin", "Atorvastatin"]
DOSES = ["10mg", "500mg", "81mg", "20mg"]
FREQS = ["once daily", "twice daily", "as needed"]
DIAGS = ["Hypertension", "Diabetes Type 2", "Hyperlipidemia"]
SYMPTOMS = ["dizziness", "fatigue", "chest pain", "headache"]

dataset = []
for i in range(100):
    note_text = random.choice(NOTES).format(
        id=random.randint(1000, 9999),
        date=f"2024-05-{random.randint(1,28):02d}",
        med1=random.choice(MEDS), dose1=random.choice(DOSES), freq1=random.choice(FREQS),
        bp=random.randint(110, 150), hr=random.randint(60, 100),
        med2=random.choice(MEDS), dose2=random.choice(DOSES),
        med3=random.choice(MEDS), dose3=random.choice(DOSES),
        days=random.choice([7, 14, 30]),
        diag=random.choice(DIAGS),
        symptom=random.choice(SYMPTOMS)
    )
    
    # Ground Truth (Jawaban Benar)
    ground_truth = {
        "medications": [m for m in MEDS if m in note_text],
        "dosages": [d for d in DOSES if d in note_text],
        "vitals": {"bp": int(note_text.split("BP ")[1].split("/")[0]) if "BP" in note_text else None}
    }
    
    dataset.append({
        "id": i,
        "text": note_text,
        "ground_truth": ground_truth
    })

# Split & Save
train, val, test = dataset[:70], dataset[70:85], dataset[85:]

for name, data in [("train", train), ("val", val), ("test", test)]:
    with open(f"data_{name}.json", "w") as f:
        json.dump(data, f, indent=2)

print("✅ Dataset generated: data_train.json, data_val.json, data_test.json")