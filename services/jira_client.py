import requests

def create_issue(jira_url, auth, headers, payload):
    url = f"{jira_url.rstrip('/')}/rest/api/2/issue"
    resp = requests.post(url, auth=auth, headers=headers, json=payload)
    if resp.status_code == 201:
        return resp.json().get("key")
    else:
        print(f"Failed to create issue: {resp.status_code} - {resp.text}")
        return None

def get_epic_name_field(jira_url, auth, headers):
    url = f"{jira_url.rstrip('/')}/rest/api/2/field"
    resp = requests.get(url, auth=auth, headers=headers)
    if resp.status_code == 200:
        for f in resp.json():
            if f['name'] == 'Epic Name':
                return f['id']
    return None

def export_plan_to_jira(jira_url, email, api_token, project_key, plan_data):
    """
    Exports a generated software engineering plan to Jira.
    Reads Epics -> Stories -> Tasks from plan_data and pushes sequentially.
    """
    auth = (email, api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    results = []
    
    epic_name_field = get_epic_name_field(jira_url, auth, headers)
    
    for epic in plan_data.get("epics", []):
        epic_title = epic.get("title", "Untitled Epic")
        epic_payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": epic_title,
                "description": epic.get("description", ""),
                "issuetype": {"name": "Epic"}
            }
        }
        if epic_name_field:
            epic_payload["fields"][epic_name_field] = epic_title
            
        epic_key = create_issue(jira_url, auth, headers, epic_payload)
        
        if epic_key:
            results.append({"type": "Epic", "key": epic_key, "title": epic_title})
            
            for story in epic.get("stories", []):
                story_payload = {
                    "fields": {
                        "project": {"key": project_key},
                        "summary": story.get("story", "Untitled Story"),
                        "description": "Acceptance Criteria:\n" + "\n".join("- " + ac for ac in story.get("acceptance_criteria", [])),
                        "issuetype": {"name": "Story"},
                        "parent": {"key": epic_key}  # Jira Cloud parent link architecture
                    }
                }
                
                story_key = create_issue(jira_url, auth, headers, story_payload)
                
                if story_key:
                    results.append({"type": "Story", "key": story_key, "title": story.get("story")})
                    
                    for task in story.get("tasks", []):
                        task_desc = f"Type: {task.get('type')}\nPriority: {task.get('priority')}\nEffort: {task.get('effort')}\nRisk/Dependency: {task.get('dependency_risk')}\n\nSource: {task.get('source_quote')}"
                        task_payload = {
                            "fields": {
                                "project": {"key": project_key},
                                "summary": task.get("task", "Untitled Task"),
                                "description": task_desc,
                                "issuetype": {"name": "Sub-task"},
                                "parent": {"key": story_key}
                            }
                        }
                        task_key = create_issue(jira_url, auth, headers, task_payload)
                        if task_key:
                            results.append({"type": "Sub-task", "key": task_key, "title": task.get("task")})
                            
    return results
