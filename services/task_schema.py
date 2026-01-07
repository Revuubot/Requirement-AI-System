TASK_SCHEMA = {
    "epics": []
}

def normalize_task_result(data):
    if not isinstance(data, dict):
        return TASK_SCHEMA.copy()

    result = TASK_SCHEMA.copy()

    if "epics" in data and isinstance(data["epics"], list):
        result["epics"] = data["epics"]

    return result
