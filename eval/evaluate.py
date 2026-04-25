import json
import os
import sys

sys.path.append(os.path.abspath("."))

from app.profiler import generate_profile

with open("data/nevup_seed_dataset.json", "r") as f:
    data = json.load(f)

total = 0
correct = 0
results = []

for trader in data["groundTruthLabels"]:
    uid = trader["userId"]
    truth = trader["pathologies"][0] if trader["pathologies"] else "control"

    pred_list = generate_profile(uid)["detectedPathologies"]
    pred = pred_list[0] if pred_list else "control"

    match = truth == pred
    if match:
        correct += 1
    total += 1

    results.append({
        "userId": uid,
        "truth": truth,
        "predicted": pred,
        "match": match
    })

accuracy = round((correct / total) * 100, 2)

report = {
    "total_profiles": total,
    "correct_predictions": correct,
    "accuracy_percent": accuracy,
    "detailed_results": results
}

os.makedirs("reports", exist_ok=True)

with open("reports/classification_report.json", "w") as f:
    json.dump(report, f, indent=4)

print(report)