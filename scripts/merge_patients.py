#!/usr/bin/env python3
"""Merge all 7 patient analysis.json files into processed/all_patients.json."""

import json
from pathlib import Path

BASE = Path("/home/liker/projects/ai-research/HyperbolicField-BloodPlasma-Study")
PROCESSED = BASE / "processed" / "all_patients.json"
PATIENT_IDS = [f"{i:02d}" for i in range(1, 8)]

# Top-level fields to preserve from existing all_patients.json
TOP_LEVEL_KEYS = ["project", "description", "sample_id_format", "sample_types", "camera", "timezone"]


def main():
    # Read existing all_patients.json for top-level metadata
    with open(PROCESSED, "r", encoding="utf-8") as f:
        existing = json.load(f)

    # Build result with preserved top-level fields
    result = {k: existing[k] for k in TOP_LEVEL_KEYS if k in existing}

    # Read all analysis.json files and index by patient_id
    analyses = {}
    for pid in PATIENT_IDS:
        path = BASE / "data" / f"patient-{pid}" / "analysis.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["patient_id"] == pid, f"patient_id mismatch in {path}"
        analyses[pid] = data

    # Build patients array: use analysis.json data entirely for each patient
    patients = []
    for pid in PATIENT_IDS:
        patients.append(analyses[pid])

    result["patients"] = patients

    # Write output
    with open(PROCESSED, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Summary
    total_photos = 0
    with_desc = 0
    for patient in patients:
        for photo in patient.get("photos", []):
            total_photos += 1
            if "visual_description" in photo:
                with_desc += 1

    print(f"Patients: {len(patients)}")
    print(f"Total photos: {total_photos}")
    print(f"With visual_description: {with_desc}")
    print(f"Without visual_description: {total_photos - with_desc}")
    print(f"Output: {PROCESSED}")


if __name__ == "__main__":
    main()
