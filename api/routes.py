from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from services.extractor import extract_requirements
from services.risk_analyzer import analyze_risks
from services.task_planner import plan_tasks
from services.parser import parse_pdf_upload

router = APIRouter()


@router.post("/api/analyze-text")
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



@router.post("/api/analyze-pdf")
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
