from langchain_community.llms import Ollama
from llm.rag import retrieve_context

llm = Ollama(model="llama3.1")

def analyze_email_raw(email_text: str) -> str:
    context = retrieve_context(email_text)

    prompt = f"""
You are a cybersecurity phishing detection system.

Rules:
- Respond ONLY in valid JSON.
- Do not add text outside JSON.

Use this exact format:
{{
  "is_phishing": true or false,
  "phishing_type": "",
  "flags": [],
  "confidence": 0.0,
  "explanation": ""
}}

Phishing reference examples:
{context}

Email to analyze:
{email_text}
"""
    return llm.invoke(prompt)
