import json
from groq import Groq
import os
os.environ["GROQ_API_KEY"] = "[REDACTED_GROK_KEY]"
client = Groq()

def analyze_risks(text: str):
    """
    Risk & Dependency Analyzer
    Returns grounded, structured risk insights.
    """

    prompt = f"""
You are a risk & ambiguity analysis assistant for software requirement documents.

Analyze ONLY the information explicitly present in the text.
Do NOT infer, assume, or speculate.

Identify:
- ambiguity risks
- dependency risks
- scope risks
- technical risks
- operational risks
- missing acceptance criteria
- undefined responsibilities
- vague requirement wording

For each risk, include:
- type  (business | technical | operational | dependency | scope | UX | security)
- description  (short + factual)
- source_quote  (exact phrase from text — not a section heading)
- impact  (low | medium | high)
- recommended_action  (what clarification or follow-up is needed)

If no risks exist, return an empty list.

Return STRICT JSON in this format:

{{
  "risks": [
    {{
      "type": "",
      "description": "",
      "source_quote": "",
      "impact": "",
      "recommended_action": ""
    }}
  ],
  "clarifications_needed": []
}}

Text to analyze:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You analyze requirement risks with evidence-grounded reasoning only."},
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content

    # Convert JSON text → Python object
    return json.loads(output)
