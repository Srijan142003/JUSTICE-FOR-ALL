import re
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def fetch_kanoon_data(endpoint: str, params=None):
    base_url = "https://api.indiankanoon.org"
    url = f"{base_url}{endpoint}"
    headers = {"Authorization": f"Token {os.getenv('INDIAN_KANOON_API_KEY', '')}"}
    if endpoint == "/search/":
        response = requests.post(url, headers=headers, data=params)
    else:
        response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def fetch_document_by_id(docid: str, maxcites: int = 5, maxcitedby: int = 5):
    base_url = "https://api.indiankanoon.org"
    endpoint = f"/doc/{docid}/"
    params = {"maxcites": str(maxcites), "maxcitedby": str(maxcitedby)}
    headers = {"Authorization": f"Token {os.getenv('INDIAN_KANOON_API_KEY', '')}"}
    url = f"{base_url}{endpoint}"
    response = requests.post(url, headers=headers, data=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def process_with_gemini(text: str, prompt: str = "Summarize and analyze this legal document.") -> str:
    api_key = os.getenv('GEMINI_API_KEY', '')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt + "\n" + text}]}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print(f"Gemini API Error: {response.status_code} - {response.text}")
        return ""

def build_knowledge_base(queries, max_docs=5, filename="knowledge_base.json"):
    def parse_gemini_verdict(verdict_text):
        # Extract sections using regex
        summary = findings = order = ""
        summary_match = re.search(r'(Summary|Analysis|Case Summary|I\. Summary)[\s\S]*?(?=Findings|Order|Verdict|II\.|III\.|$)', verdict_text, re.IGNORECASE)
        findings_match = re.search(r'(Findings|Analysis|II\. Analysis)[\s\S]*?(?=Order|Verdict|III\.|$)', verdict_text, re.IGNORECASE)
        order_match = re.search(r'(Order|Verdict|III\. Verdict|Directive)[\s\S]*', verdict_text, re.IGNORECASE)
        if summary_match:
            summary = summary_match.group(0).strip()
        if findings_match:
            findings = findings_match.group(0).strip()
        if order_match:
            order = order_match.group(0).strip()
        return summary, findings, order
    kb = []
    # Expanded queries for broader knowledge base
    expanded_queries = queries + [
        "right to equality", "article 14", "article 19", "article 32", "directive principles", "judicial review", "writs in India", "constitutional amendments", "right to property", "basic structure doctrine", "emergency provisions", "fundamental duties", "public interest litigation", "separation of powers", "rule of law", "natural justice"
    ]
    for query in expanded_queries:
        print(f"Fetching docs for query: {query}")
        result = fetch_kanoon_data("/search/", params={"formInput": query})
        if result and "docs" in result:
            for doc in result["docs"][:max_docs]:
                docid = doc["tid"]
                doc_data = fetch_document_by_id(str(docid))
                if doc_data:
                    # Get Gemini summary/verdict
                    gemini_output = process_with_gemini(doc_data.get("doc", ""), prompt="Summarize and analyze this legal document. Provide a structured verdict as a judge would, with clear sections for summary, findings, and order.")
                    summary, findings, order = parse_gemini_verdict(gemini_output)
                    kb.append({
                        "query": query,
                        "docid": docid,
                        "title": doc_data.get("title"),
                        "publishdate": doc_data.get("publishdate"),
                        "docsource": doc_data.get("docsource"),
                        "text": doc_data.get("doc"),
                        "numcites": doc_data.get("numcites"),
                        "numcitedby": doc_data.get("numcitedby"),
                        "covers": doc_data.get("covers"),
                        "relatedqs": doc_data.get("relatedqs"),
                        "gemini_summary": gemini_output,
                        "verdict_summary": summary,
                        "verdict_findings": findings,
                        "verdict_order": order
                    })
    save_path = os.path.join(os.path.expanduser("~"), "Documents", "maj1", "legal_ai_model", "knowledge_base.json")
    parent_dir = os.path.dirname(save_path)
    print(f"[DEBUG] Attempting to write knowledge base to: {save_path}")
    try:
        # Ensure parent directory exists right before writing
        os.makedirs(parent_dir, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(kb, f, ensure_ascii=False, indent=2)
        print(f"[DEBUG] Knowledge base successfully saved to {save_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save knowledge base: {e}")
    print("[DEBUG] build_knowledge_base function completed.")
    sample_docid = None
    doc_result = None
    if result and "docs" in result and len(result["docs"]) > 0:
        sample_docid = result["docs"][0]["tid"]
        print(f"\nFetching document by ID: {sample_docid}")
        doc_result = fetch_document_by_id(sample_docid)
        if doc_result:
            print("Document result:")
            print(doc_result)
        else:
            print("No document result or error occurred.")
    # Test: Process document text with Gemini
    if doc_result and "doc" in doc_result:
        print("\nProcessing document text with Gemini...")
        gemini_output = process_with_gemini(doc_result["doc"], prompt="Summarize and analyze this legal document. Provide a structured verdict as a judge would.")
        print("Gemini output:")
        print(gemini_output)

if __name__ == "__main__":
    print("[DEBUG] Script started. If you see this, the script is running.")
    try:
        sample_queries = ["constitution", "article 21", "fundamental rights"]
        build_knowledge_base(sample_queries, max_docs=2)
    except Exception as e:
        print(f"[ERROR] Exception in main: {e}")
