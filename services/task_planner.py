import json
from groq import Groq
import os
os.environ["GROQ_API_KEY"] = "[REDACTED_GROK_KEY]"
client = Groq()

def plan_tasks(requirements, risks):
    """
    Converts requirements into:
    - epics
    - user stories
    - engineering tasks
    - acceptance criteria
    - risk dependencies
    """

    prompt = f"""
You are a software engineering planning assistant.
Generate ONLY tasks based on explicitly given requirements and risks.

Do NOT invent features.
Do NOT assume business goals beyond the text.

Inputs are requirement lists:

FUNCTIONAL REQUIREMENTS:
{json.dumps(requirements.get("functional_requirements", []), indent=2)}

NON FUNCTIONAL REQUIREMENTS:
{json.dumps(requirements.get("non_functional_requirements", []), indent=2)}

RISKS:
{json.dumps(risks.get("risks", []), indent=2)}

Create structured sprint-ready output.

Rules:
- each task must be traceable to a requirement or risk
- include source_quote
- include dependency if related to a risk
- do not duplicate tasks
- no vague wording

Return ONLY valid JSON.
Do not add explanations, notes, or markdown.
Do not wrap inside code blocks.


Return STRICT JSON:

{{
  "epics": [
    {{
      "title": "",
      "description": "",
      "related_requirements": [],
      "stories": [
        {{
          "story": "",
          "acceptance_criteria": [],
          "tasks": [
            {{
              "task": "",
              "type": "backend | frontend | api | devops | testing",
              "priority": "low | medium | high",
              "effort": "S | M | L",
              "dependency_risk": "",
              "source_quote": ""
            }}
          ]
        }}
      ]
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You generate software engineering epics and sprint tasks only from provided text."},
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content

    return json.loads(output)