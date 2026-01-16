# Resume Analyzer (Django + Gemini)

A Django-based Resume Analyzer web application that analyzes resumes using
Google Gemini AI and compares them against Job Descriptions to provide
ATS-style insights.

---

##  Features

-  Upload PDF resumes (Drag & Drop)
-  Resume text extraction with OCR fallback
-  AI-powered resume analysis using Google Gemini
-  Job Description comparison
-  Missing skills & ATS keyword detection
-  Dynamic resume score
-  Light / Dark mode UI
-  Clean Django architecture

---

##  Tech Stack

- **Backend**: Django
- **AI**: Google Gemini (`google.genai`)
- **PDF Parsing**: pdfplumber, pytesseract
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (default, not yet used)

---

##  Project Structure
Folder / File,Description
analyzer/,              The main Django app containing the logic for processing resumes.
├── utils/,             "Contains helper scripts: resume_parser.py, text_cleaner.py, and gemini_client.py."
├── templates/,         "HTML files, including your layout.html and index.html."
├── static/,            CSS and JavaScript for the drag-and-drop UI and Bootstrap styling.
resume_analyser/,       The Django project configuration folder (settings and main URLs).
manage.py,              The command-line utility for running the server and migrations.
.env,                   Stores sensitive information like your Gemini API keys.
├── requirements.txt
├── README.md
└── .env
