from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 🔥 Upload ONCE and reuse if possible
uploaded_file = client.files.upload(file="image/VishalJha.pdf")

prompt = """
Analyze the resume strictly for the role of engineers.

Return ONLY valid JSON. No markdown. No explanation.

{
  "goodPoints": [],
  "badPoints": [],
  "improvements": [],
  "jdMatch": {
    "score": 0,
    "missingSkills": [],
    "suggestedKeywords": []
  }
}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[prompt, uploaded_file],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.2
    )
)

print(response.text)

client.close()
