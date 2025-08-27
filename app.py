import PyPDF2
import docx
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "maj1", "legal_ai_model", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Helper to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = findings = order = ''
    case_text = ''
    file_text = ''
    if request.method == 'POST':
        case_text = request.form.get('case_text', '')
        file = request.files.get('case_file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Extract text from file
            if filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_text = f.read()
            elif filename.endswith('.pdf'):
                try:
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        file_text = "\n".join(page.extract_text() or '' for page in reader.pages)
                except Exception as e:
                    file_text = f'[PDF extraction error: {e}]'
            elif filename.endswith('.docx'):
                try:
                    doc = docx.Document(file_path)
                    file_text = "\n".join([para.text for para in doc.paragraphs])
                except Exception as e:
                    file_text = f'[DOCX extraction error: {e}]'
        # Combine user text and file text
        user_input = case_text + '\n' + file_text
        # AI processing logic
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from main_clean import process_with_gemini
        import re
        verdict_output = process_with_gemini(user_input, prompt="Summarize and analyze this legal document. Provide a structured verdict as a judge would, with clear sections for summary, findings, and order.")
        summary_match = re.search(r'(Summary|Analysis|Case Summary|I\. Summary)[\s\S]*?(?=Findings|Order|Verdict|II\.|III\.|$)', verdict_output, re.IGNORECASE)
        findings_match = re.search(r'(Findings|Analysis|II\. Analysis)[\s\S]*?(?=Order|Verdict|III\.|$)', verdict_output, re.IGNORECASE)
        order_match = re.search(r'(Order|Verdict|III\. Verdict|Directive)[\s\S]*', verdict_output, re.IGNORECASE)
        if summary_match:
            summary = summary_match.group(0).strip()
        if findings_match:
            findings = findings_match.group(0).strip()
        if order_match:
            order = order_match.group(0).strip()
        return render_template('result.html', case_description=case_text, file_text=file_text, summary=summary, findings=findings, order=order)
    return render_template('index.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
