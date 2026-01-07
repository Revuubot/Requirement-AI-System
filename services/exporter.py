import pandas as pd
import os
from datetime import datetime


def save_pipeline_report(data: dict, output_dir="exports"):

    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    base = f"{output_dir}/requirements_report_{timestamp}"

    # ---- Requirements ----
    req_rows = []

    for chunk in data["requirements"]:
        for item in chunk.get("functional_requirements", []):
            req_rows.append({
                "type": "functional",
                "value": item["value"],
                "source": item.get("source_quote","")
            })

        for item in chunk.get("non_functional_requirements", []):
            req_rows.append({
                "type": "non_functional",
                "value": item["value"],
                "source": item.get("source_quote","")
            })

    req_df = pd.DataFrame(req_rows)
    req_df.to_excel(f"{base}_requirements.xlsx", index=False)

    # ---- Risks ----
    risk_rows = []

    for chunk in data["risks"]:
        for r in chunk.get("risks", []):
            risk_rows.append({
                "type": r.get("type",""),
                "description": r.get("description",""),
                "impact": r.get("impact",""),
                "recommended_action": r.get("recommended_action","")
            })

    pd.DataFrame(risk_rows).to_excel(f"{base}_risks.xlsx", index=False)

    return {
        "requirements_file": f"{base}_requirements.xlsx",
        "risks_file": f"{base}_risks.xlsx"
    }
