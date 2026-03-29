from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import pandas as pd
import io

from services.extractor import extract_requirements
from services.risk_analyzer import analyze_risks
from services.task_planner import plan_tasks
from services.parser import parse_pdf_upload
from services.jira_client import export_plan_to_jira

router = APIRouter()

# -----------------------------
# 📌 RAW TEXT ANALYSIS (API)
# -----------------------------
@router.post("/analyze-text")
async def analyze_text_api(text: str = Form(...)):
    try:
        requirements = extract_requirements(text)
        risks = analyze_risks(text)
        tasks = plan_tasks(requirements, risks)

        return {
            "requirements": requirements,
            "risks": risks,
            "task_plan": tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 📌 PDF ANALYSIS (API)
# -----------------------------
@router.post("/analyze-pdf")
async def analyze_pdf_api(file: UploadFile = File(...)):
    try:
        pdf_text = await parse_pdf_upload(file)

        requirements = extract_requirements(pdf_text)
        risks = analyze_risks(pdf_text)
        tasks = plan_tasks(requirements, risks)

        return {
            "requirements": requirements,
            "risks": risks,
            "task_plan": tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/ui/analyze-text")
async def analyze_text_ui(text: str = Form(...)):
    try:
        requirements = extract_requirements(text)
        risks = analyze_risks(text)
        tasks = plan_tasks(requirements, risks)

        return {
            "status": "success",
            "source": "ui",
            "requirements": requirements,
            "risks": risks,
            "task_plan": tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/ui/analyze-pdf")
async def analyze_pdf_ui(file: UploadFile = File(...)):
    try:
        pdf_text = await parse_pdf_upload(file)

        requirements = extract_requirements(pdf_text)
        risks = analyze_risks(pdf_text)
        tasks = plan_tasks(requirements, risks)

        return {
            "status": "success",
            "source": "ui",
            "requirements": requirements,
            "risks": risks,
            "task_plan": tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 📊 EXCEL EXPORT
# -----------------------------
class ExportData(BaseModel):
    requirements: dict
    risks: dict
    task_plan: dict

@router.post("/ui/export-excel")
async def export_excel(data: ExportData):
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Requirements
            func_req = data.requirements.get("functional_requirements", [])
            non_func_req = data.requirements.get("non_functional_requirements", [])
            req_df = pd.DataFrame(func_req + non_func_req)
            if not req_df.empty:
                req_df.to_excel(writer, sheet_name='Requirements', index=False)
            else:
                pd.DataFrame({"value": ["No requirements"]}).to_excel(writer, sheet_name='Requirements', index=False)

            # Risks
            risk_df = pd.DataFrame(data.risks.get("risks", []))
            if not risk_df.empty:
                risk_df.to_excel(writer, sheet_name='Risks', index=False)
            else:
                pd.DataFrame({"type": ["No risks"]}).to_excel(writer, sheet_name='Risks', index=False)

            # Tasks
            task_rows = []
            for epic in data.task_plan.get("epics", []):
                epic_title = epic.get("title", "")
                for story in epic.get("stories", []):
                    story_title = story.get("story", "")
                    for task in story.get("tasks", []):
                        task_rows.append({
                            "Epic": epic_title,
                            "Story": story_title,
                            "Task": task.get("task"),
                            "Type": task.get("type"),
                            "Priority": task.get("priority"),
                            "Effort": task.get("effort")
                        })
            task_df = pd.DataFrame(task_rows)
            if not task_df.empty:
                task_df.to_excel(writer, sheet_name='Task Plan', index=False)
            else:
                pd.DataFrame({"Task": ["No tasks"]}).to_excel(writer, sheet_name='Task Plan', index=False)
                
        output.seek(0)
        headers = {'Content-Disposition': 'attachment; filename="analysis_export.xlsx"'}
        return Response(content=output.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 📋 JIRA EXPORT
# -----------------------------
class JiraConfig(BaseModel):
    jira_url: str
    email: str
    api_token: str
    project_key: str

class JiraExportRequest(BaseModel):
    config: JiraConfig
    task_plan: dict

@router.post("/ui/export-jira")
async def export_jira(req: JiraExportRequest):
    try:
        results = export_plan_to_jira(
            jira_url=req.config.jira_url,
            email=req.config.email,
            api_token=req.config.api_token,
            project_key=req.config.project_key,
            plan_data=req.task_plan
        )
        return {"status": "success", "issues_created": len(results), "details": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

