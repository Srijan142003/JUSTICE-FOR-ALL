# JUSTICE-FOR-ALL

# Legal AI Verdict Web App

This project is a Flask-based web application that allows users to submit legal case descriptions or upload documents (PDF, DOCX, TXT) for unbiased AI-driven verdict analysis. The backend uses Gemini AI and Indian Kanoon APIs for legal document processing and verdict generation.

## Features
- Submit case details or upload legal documents
- Automatic text extraction from PDF, DOCX, and TXT files
- AI-powered verdict generation (summary, findings, order)
- Clean, modern Bootstrap UI

## Technologies Used
- Python (Flask, PyPDF2, python-docx, requests, python-dotenv)
- Gemini AI API
- Indian Kanoon API
- Bootstrap (frontend styling)

## Setup & Installation
1. **Clone the repository:**
   ```
   git clone https://github.com/Srijan142003/srija.git
   cd srija/legal_ai_model
   ```
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   - Create a `.env` file in the project root with your API keys:
     ```
     INDIAN_KANOON_API_KEY=your_kanoon_api_key
     GEMINI_API_KEY=your_gemini_api_key
     ```

## Running Locally
1. **Start the Flask server:**
   ```
   python app.py
   ```
2. **Open your browser:**
   - Go to `http://127.0.0.1:5000`

## Deployment (Render)
1. **Push your code to GitHub.**
2. **Create a new Web Service on Render:**
   - Set the start command to `python app.py`
   - Add your environment variables in the Render dashboard
3. **Access your deployed app via the Render URL.**

## File Structure
```
legal_ai_model/
├── app.py
├── main_clean.py
├── requirements.txt
├── .env
├── templates/
│   ├── index.html
│   └── result.html
└── README.md
```

## License
MIT

---
**Note:** Do not commit your `.env` file or API keys to public repositories. Add them securely in your deployment platform.
