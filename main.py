import os
import json
import requests
from dotenv import load_dotenv

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
    kb = []
    for query in queries:
        print(f"Fetching docs for query: {query}")
        result = fetch_kanoon_data("/search/", params={"formInput": query})
        if result and "docs" in result:
            for doc in result["docs"][:max_docs]:
                docid = doc["tid"]
                doc_data = fetch_document_by_id(str(docid))
                if doc_data:
                    kb.append({
                        "query": query,
                        "docid": docid,
                        "title": doc_data.get("title"),
                        "publishdate": doc_data.get("publishdate"),
                        "docsource": doc_data.get("docsource"),
                        "text": doc_data.get("doc")
                    })
    save_path = r"c:\\Users\\srija\\Documents\\maj1\\legal_ai_model\\knowledge_base.json"
    parent_dir = os.path.dirname(save_path)
    print(f"Ensuring directory exists: {parent_dir}")
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    print(f"[DEBUG] Attempting to write knowledge base to: {save_path}")
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(kb, f, ensure_ascii=False, indent=2)
        print(f"[DEBUG] Knowledge base successfully saved to {save_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save knowledge base: {e}")
    print("[DEBUG] build_knowledge_base function completed.")
    sample_docid = None
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
import os
import json

# Use a simpler path for test file write
save_path = r"c:\Users\srija\Documents\test_write.json"
parent_dir = os.path.dirname(save_path)

if not os.path.exists(parent_dir):
    print(f"[DEBUG] Creating missing directory: {parent_dir}")
    os.makedirs(parent_dir, exist_ok=True)
else:
    print(f"[DEBUG] Directory already exists: {parent_dir}")

test_data = {"test": "This is a test file to confirm write access."}
print(f"[DEBUG] Attempting to write test file to: {save_path}")
try:
    with open(save_path, "w", encoding="utf-8") as tf:
        json.dump(test_data, tf, ensure_ascii=False, indent=2)
    print(f"[DEBUG] Test file successfully saved to {save_path}")
except Exception as e:
    print(f"[ERROR] Failed to save test file: {e}")
def build_knowledge_base(queries, max_docs=5, filename="knowledge_base.json"):
    kb = []
    for query in queries:
        print(f"Fetching docs for query: {query}")
        result = fetch_kanoon_data("/search/", params={"formInput": query})
        if result and "docs" in result:
            for doc in result["docs"][:max_docs]:
                docid = doc["tid"]
                doc_data = fetch_document_by_id(str(docid))
                if doc_data:
                    kb.append({
                        "query": query,
                        "docid": docid,
                        "title": doc_data.get("title"),
                        "publishdate": doc_data.get("publishdate"),
                        "docsource": doc_data.get("docsource"),
                        "text": doc_data.get("doc")
                    })
    save_path = r"c:\\Users\\srija\\Documents\\maj1\\legal_ai_model\\knowledge_base.json"
    parent_dir = os.path.dirname(save_path)
    print(f"Ensuring directory exists: {parent_dir}")
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    print(f"[DEBUG] Attempting to write knowledge base to: {save_path}")
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(kb, f, ensure_ascii=False, indent=2)
        print(f"[DEBUG] Knowledge base successfully saved to {save_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save knowledge base: {e}")
    print("[DEBUG] build_knowledge_base function completed.")
    sample_docid = None
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
    if response.status_code == 200:
        result = response.json()
        # Extract the generated text from the response
                "text": doc_data.get("doc")
            })
        print(f"Gemini API Error: {response.status_code} - {response.text}")
        import os
        import json
                        "text": doc_data.get("doc"),
                    })
    import os
    save_path = r"c:\Users\srija\Documents\maj1\legal_ai_model\knowledge_base.json"
    parent_dir = os.path.dirname(save_path)
    print(f"Ensuring directory exists: {parent_dir}")
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
        import os
        save_path = os.path.abspath(r"c:\Users\srija\Documents\maj1\legal_ai_model\knowledge_base.json")
        parent_dir = os.path.dirname(save_path)
        print(f"[DEBUG] Intended save path: {save_path}")
        print(f"[DEBUG] Parent directory: {parent_dir}")
        # Create parent directory if it doesn't exist
        if not os.path.exists(parent_dir):
            print(f"[DEBUG] Creating missing directory: {parent_dir}")
            os.makedirs(parent_dir, exist_ok=True)
        else:
            print(f"[DEBUG] Directory already exists: {parent_dir}")
        print(f"[DEBUG] Attempting to write knowledge base to: {save_path}")
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(kb, f, ensure_ascii=False, indent=2)
            print(f"[DEBUG] Knowledge base successfully saved to {save_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save knowledge base: {e}")
    print("[DEBUG] build_knowledge_base function completed.")
    sample_docid = None
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
    write_test_file()
    try:
        sample_queries = ["constitution", "article 21", "fundamental rights"]
        build_knowledge_base(sample_queries, max_docs=2)
    except Exception as e:
        print(f"[ERROR] Exception in main: {e}")

# Define save_path and parent_dir at the top
save_path = os.path.abspath(r"c:\Users\srija\Documents\maj1\legal_ai_model\knowledge_base.json")

