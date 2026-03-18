from llm.llm_handler import analyze_email_raw
from llm.utils import safe_parse_json, normalize_result
from llm.post_processor import fix_output

def analyze_email_pipeline(email_text: str) -> dict:
    raw = analyze_email_raw(email_text)
    parsed = safe_parse_json(raw)
    result = normalize_result(parsed)
    result = fix_output(result, email_text)
    return result
