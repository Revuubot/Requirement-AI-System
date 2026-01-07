from services.extractor import extract_requirements
from services.risk_analyzer import analyze_risks
from services.task_planner import plan_tasks

from services.pdf_reader import read_pdf_text
from services.chunker import chunk_text


def run_pipeline(text: str = None, pdf_path: str = None):
    """
    Unified orchestrator for:
    - plain text input
    - pdf input (chunked)
    """

    if pdf_path:
        full_text = read_pdf_text(pdf_path)
        chunks = chunk_text(full_text)
    else:
        chunks = [text]

    all_requirements = []
    all_risks = []
    all_tasks = []

    for chunk in chunks:

        req = extract_requirements(chunk)
        risk = analyze_risks(chunk)
        task = plan_tasks(req, risk)

        all_requirements.append(req)
        all_risks.append(risk)
        all_tasks.append(task)

    return {
        "chunks_processed": len(chunks),
        "requirements": all_requirements,
        "risks": all_risks,
        "task_plan": all_tasks
    }

