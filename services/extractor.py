from groq import Groq
import os
os.environ["GROQ_API_KEY"] = "[REDACTED_GROK_KEY]"

import json


client = Groq()

def extract_requirements(text):
    prompt = f"""
Classify extracted information into the correct category.

Follow these rules:
Functional Requirements = system capabilities / actions
Non-Functional Requirements = performance, scale, reliability, security
Constraints & Assumptions = external limits, dependencies, scope boundaries
Business Objectives = goals, motivations, outcomes

Do NOT infer or assume.
Extract only what appears in the text.

Constraints & Assumptions include:
technology limitations
operational assumptions
environment constraints
scope exclusions
dependencies on external parties
language or region restrictions
data ownership or responsibility
anything marked “assumption”

If an item begins with "Assumption", "Client assumption",
or appears in an assumption section — classify it under constraints_and_assumptions.

For source_quote:
-It must contain the exact sentence or phrase that expresses the requirement.
-Do NOT use section headers, labels, or titles as source quotes.
-The quote must come from the same sentence as the requirement value.
If a requirement value cannot be directly matched to a sentence,
do NOT include it.



Return STRICT JSON in this structure:

{{
  "business_objectives": [],
  "functional_requirements": [],
  "non_functional_requirements": [],
  "constraints_and_assumptions": [],
  "open_questions": []
}}

For each item include:
"value" and "source_quote".

Text:
{text}
"""


    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You extract strictly factual requirements from text."},
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content

    # convert JSON string → python dict
    return json.loads(output)



