RISK_SCHEMA = {
    "risks": [],
    "clarifications_needed": []
}

def normalize_risk_result(data):
    if not isinstance(data, dict):
        return RISK_SCHEMA.copy()

    result = RISK_SCHEMA.copy()

    if "risks" in data and isinstance(data["risks"], list):
        result["risks"] = data["risks"]

    if "clarifications_needed" in data and isinstance(data["clarifications_needed"], list):
        result["clarifications_needed"] = data["clarifications_needed"]

    return result
