# Resume Analyzer (Django + Gemini)

A Django-based Resume Analyzer web application that analyzes resumes using
Google Gemini AI and compares them against Job Descriptions to provide
ATS-style insights.

---

## 🚀 Features

- 📄 Upload PDF resumes (Drag & Drop)
- 🔍 Resume text extraction with OCR fallback
- 🧠 AI-powered resume analysis using Google Gemini
- 📝 Job Description comparison
- 🎯 Missing skills & ATS keyword detection
- 📊 Dynamic resume score
- 🌙 Light / Dark mode UI
- 💻 Clean Django architecture

---

## 🛠 Tech Stack

- **Backend**: Django
- **AI**: Google Gemini (`google.genai`)
- **PDF Parsing**: pdfplumber, pytesseract
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (default, not yet used)

---

## 📂 Project Structure
resume_analyser/
├── analyzer/
│ ├── utils/
│ │ ├── resume_parser.py
│ │ ├── text_cleaner.py
│ │ └── gemini_client.py
│ ├── templates/
│ ├── static/
│ ├── views.py
│ └── urls.py
├── resume_analyser/
├── manage.py
├── requirements.txt
├── README.md
└── .env
