EMPTY_SCHEMA = {
    "project_summary": [],
    "stakeholders": [],
    "deliverables": [],
    "functional_requirements": [],
    "non_functional_requirements": [],
    "constraints": [],
    "open_questions": []
}


def normalize_schema(data):
    """
    Guarantee the result is always a dict
    matching the expected schema shape.
    """

    if isinstance(data, list):
        return {
            **EMPTY_SCHEMA,
            "functional_requirements": data   
        }

    normalized = {**EMPTY_SCHEMA}

    for key in normalized.keys():
        if key in data and isinstance(data[key], list):
            normalized[key] = data[key]

    return normalized
