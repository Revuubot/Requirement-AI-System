from pydantic import BaseModel
from typing import Any, Dict


class RequirementRequest(BaseModel):
    text: str


class PipelineResponse(BaseModel):
    requirements: dict
    risks: dict
    task_plan: dict
