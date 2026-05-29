import json
import requests
from metrics import calculate_metrics, export_metrics_to_json

# 1. Load Test Dataset (File yang dibuat di Day 0)
try:
    with open('data_test.json', 'r') as f:
        test_data = json.load(f)
except FileNotFoundError:
    print("Error: data_test.json tidak ditemukan. Pastikan sudah generate dataset.")
    exit()

predictions = []
ground_truths = []

# 2. Loop through data dan kirim ke API
print(" Running evaluation on test dataset...")
for item in test_data:
    text = item['text']
    truth = item['ground_truth']
    
    # Payload untuk dikirim ke FastAPI
    payload = {
        "note_id": str(item['id']),
        "text": text,
        "category": "nursing" 
    }
    
    try:
        # Panggil API lokal
        response = requests.post("http://localhost:8000/extract", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            predictions.append(result)
            # Kita simpan ground truth sesuai format yang diharapkan metrics.py
            ground_truths.append({"ground_truth": truth})
        else:
            print(f"️ Gagal memproses item {item['id']}: Status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(" Error: Tidak bisa connect ke API. Pastikan 'python main.py' sedang berjalan!")
        break

# 3. Hitung Metrics
if predictions:
    print(f"\n Selesai mengevaluasi {len(predictions)} sampel data.")
    
    # Panggil fungsi calculate_metrics dari file metrics.py
    final_metrics = calculate_metrics(predictions, ground_truths)
    
    print("\n --- HASIL EVALUASI ---")
    print(f"Precision: {final_metrics.precision}")
    print(f"Recall:    {final_metrics.recall}")
    print(f"F1-Score:  {final_metrics.f1_score}")
    
    # Export ke file JSON
    report = export_metrics_to_json(final_metrics)
    print("\nLaporan tersimpan di: metrics_report.json")

else:
    print(" Tidak ada data yang berhasil diproses.")