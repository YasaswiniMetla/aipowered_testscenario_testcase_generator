🧪 AI-Powered Test Scenario & Testcase Generator

Generate high-quality QA scenarios and detailed testcases using Google Gemini 2.5 — powered by Streamlit.

🚀 Overview

This project is an intelligent QA assistant that automatically generates:

Professional test scenarios

Detailed testcases (steps + expected results)

Editable scenario inputs

AI-powered “Improve Scenario” rewriting

Multiple export formats (JSON, CSV, Markdown, ZIP)

A modern Streamlit user interface

It helps QA engineers, testers, and developers speed up testcase creation with accurate, structured outputs.

✨ Features

🧠 AI Generation

Generate test scenarios from requirements

Convert scenarios into full testcases

Improve poorly written scenarios

🎨 Modern UI

Clean dark theme

Editable scenario blocks

Real-time generation

Step-by-step testcase viewer

📦 Export

Export as JSON

Export as CSV

Export as Markdown

Export all formats as ZIP

🛠 Architecture

Python 3.11+

Streamlit

Gemini 2.5 API

Modular utils: validations, prompts

🔧 Installation (Local)

Clone the repository
git clone https://github.com/
<your-username>/AI-Testcase-Generator.git
cd AI-Testcase-Generator

Create virtual environment
python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Mac/Linux)

Install dependencies
pip install -r requirements.txt

Create .env file
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=models/gemini-2.5-flash

Run the app
streamlit run app/streamlit_app.py

🌐 Deployment
🟩 Deploy on Streamlit Cloud (Recommended & Free)

Push project to GitHub

Go to https://share.streamlit.io

Click “New App”

Select your repo

Set main file path:
app/streamlit_app.py

Add environment variable:
GEMINI_API_KEY

Deploy

🟪 Deploy on HuggingFace Spaces (Free)

Create a new Space

Choose SDK → Streamlit

Upload:

app/streamlit_app.py (or rename to app.py)

requirements.txt

utils folder

config.py

Deploy

Live web link:

📸 Screenshots

<video controls src="AIPOWERED_TESTSCENARIO_TESTCASE_GENERATOR_RECORDING.mp4" title="Title"></video>
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-5.png)

Scenario Generation

🔐 Environment Variables

GEMINI_API_KEY — your Google Gemini API key

🧠 Improve Scenario with AI

Each scenario block includes an “Improve Scenario” button that:

makes scenarios clearer

adds boundary conditions

rewrites vague scenarios

ensures better testcase quality

📦 Export Formats

JSON — import into automation tools

CSV — Excel, Sheets

Markdown — for documentation

ZIP Bundle — entire set packaged together

📜 License

MIT License © 2025 SAI YASASWINI METLA
