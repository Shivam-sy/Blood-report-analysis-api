import re

def extract_value(pattern, text):
    match = re.search(pattern, text)
    return float(match.group(1)) if match else None


def analyze_report(text):
    # Extract values
    hemoglobin = extract_value(r"hemoglobin.*?(\d+\.?\d*)", text)
    wbc = extract_value(r"wbc.*?(\d+)", text)
    platelets = extract_value(r"platelet.*?(\d+)", text)
    hba1c = extract_value(r"hba1c.*?(\d+\.?\d*)", text)
    glucose = extract_value(r"blood sugar.*?(\d+)", text)
    vitamin_d = extract_value(r"vitamin d.*?(\d+\.?\d*)", text)
    b12 = extract_value(r"vitamin b12.*?(\d+\.?\d*)", text)

    conditions = []
    advice = []

    # 🔴 Diabetes
    if hba1c and hba1c > 6.5:
        conditions.append({
            "title": "Diabetes Risk",
            "severity": "High",
            "color": "red",
            "description": f"HbA1c level is {hba1c}, which is above normal."
        })
        advice.append("Consult a doctor for diabetes management")

    # 🟠 Infection
    if wbc and wbc > 10000:
        conditions.append({
            "title": "Possible Infection",
            "severity": "Moderate",
            "color": "orange",
            "description": f"WBC count is {wbc}, indicating possible infection."
        })
        advice.append("Check for infection or inflammation")

    # 🟠 Platelets
    if platelets and platelets < 150000:
        conditions.append({
            "title": "Low Platelets",
            "severity": "Moderate",
            "color": "orange",
            "description": f"Platelet count is {platelets}, slightly low."
        })
        advice.append("Monitor platelet levels regularly")

    # 🔴 Vitamin D
    if vitamin_d and vitamin_d < 20:
        conditions.append({
            "title": "Vitamin D Deficiency",
            "severity": "High" if vitamin_d < 10 else "Moderate",
            "color": "red" if vitamin_d < 10 else "orange",
            "description": f"Vitamin D level is {vitamin_d}, which is low."
        })
        advice.append("Increase Vitamin D intake")

    # 🟠 Vitamin B12
    if b12 and b12 < 200:
        conditions.append({
            "title": "Vitamin B12 Deficiency",
            "severity": "Moderate",
            "color": "orange",
            "description": f"Vitamin B12 level is {b12}, below normal."
        })
        advice.append("Consider Vitamin B12 supplements")

    # 🟢 Normal case
    if not conditions:
        conditions.append({
            "title": "All Parameters Normal",
            "severity": "Normal",
            "color": "green",
            "description": "All key health indicators are within normal range."
        })

    # Sort by severity priority
    priority = {"High": 3, "Moderate": 2, "Normal": 1}
    conditions = sorted(conditions, key=lambda x: priority[x["severity"]], reverse=True)

    return {
        "status": "success",
        "summary": conditions[0]["title"],   # 🔥 main highlight
        "conditions": conditions,
        "recommendations": list(set(advice))
    }