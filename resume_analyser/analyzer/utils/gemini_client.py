import os
import json
from google import genai
from google.genai import types

# Gemini client (uses environment variable)
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def gemini_analyze_resume(text: str, job_description: str = "") -> dict:
    prompt = f"""
You are an AI resume analyzer.

Compare the resume against the given job description.
Identify missing skills and keywords that are required in the job description
but NOT present in the resume.

Return ONLY valid JSON.
No markdown.
No backticks.
No explanations.

JSON format:

{{
  "goodPoints": [],
  "badPoints": [],
  "improvements": [],
  "jdMatch": {{
    "missingSkills": [],
    "suggestedKeywords": []
  }}
}}

Resume:
{text}

Job Description:
{job_description if job_description else "No job description provided."}
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2
        )
    )

    raw_output = response.text.strip()

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON")

    return {
        "goodPoints": parsed.get("goodPoints", []),
        "badPoints": parsed.get("badPoints", []),
        "improvements": parsed.get("improvements", []),
        "jdMatch": {
            "score": parsed.get("jdMatch", {}).get("score", 0),
            "missingSkills": parsed.get("jdMatch", {}).get("missingSkills", []),
            "suggestedKeywords": parsed.get("jdMatch", {}).get("suggestedKeywords", [])
        }
    }
