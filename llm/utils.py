import json
import re
from typing import Any, Dict

def safe_parse_json(text: str) -> Dict[str, Any]:
    """
    Try to parse LLM output as JSON.
    If it contains extra text, attempt to extract the JSON object.
    Always returns a dict with either valid fields or an error payload.
    """
    if not text:
        return {"ok": False, "error": "Empty LLM output", "raw": text}

    # 1) Try direct JSON parse
    try:
        data = json.loads(text)
        return {"ok": True, "data": data, "raw": text}
    except Exception:
        pass

    # 2) Try to extract the first {...} block
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        candidate = match.group(0)
        try:
            data = json.loads(candidate)
            return {"ok": True, "data": data, "raw": text}
        except Exception:
            return {"ok": False, "error": "Found JSON-like block but failed to parse", "raw": text}

    return {"ok": False, "error": "No JSON object found in output", "raw": text}


def normalize_result(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize the output into a stable schema your Flask UI can rely on.
    """
    if not parsed.get("ok"):
        return {
            "is_phishing": None,
            "phishing_type": "",
            "flags": [],
            "confidence": 0.0,
            "explanation": parsed.get("error", "Unknown error"),
            "raw_output": parsed.get("raw", "")
        }

    d = parsed["data"] if isinstance(parsed["data"], dict) else {}

    return {
        "is_phishing": d.get("is_phishing", None),
        "phishing_type": d.get("phishing_type", "") or "",
        "flags": d.get("flags", []) or [],
        "confidence": float(d.get("confidence", 0.0) or 0.0),
        "explanation": d.get("explanation", "") or "",
        "raw_output": parsed.get("raw", "")
    }
