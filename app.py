from flask import Flask, render_template, request
from llm.pipeline import analyze_email_pipeline
from llm.logger import log_event, now_iso
from data.emails import EMAILS

app = Flask(__name__)

@app.route("/")
def inbox():
    return render_template("inbox.html", emails=EMAILS)

@app.route("/analyze", methods=["POST"])
def analyze():
    email_id = request.form["email_id"]
    email_text = request.form["email_text"]

    # Ground truth
    expected_is_phishing = request.form.get("expected_is_phishing", "")
    expected_type = request.form.get("expected_type", "")
    expected_flags = request.form.get("expected_flags", "")

    # Model analysis
    result = analyze_email_pipeline(email_text)

    # Convert model flags list into a string for CSV
    model_flags = ";".join(result.get("flags", []))

    # Log event
    log_event({
        "ts": now_iso(),
        "email_id": email_id,
        "expected_is_phishing": expected_is_phishing,
        "model_is_phishing": result.get("is_phishing"),
        "expected_type": expected_type,
        "model_type": result.get("phishing_type", ""),
        "expected_flags": expected_flags,
        "model_flags": model_flags,
        "confidence": result.get("confidence", 0.0),
    })

    return render_template(
        "result.html",
        result=result,
        email_text=email_text,
        email_id=email_id,
        expected_is_phishing=expected_is_phishing,
        expected_type=expected_type,
        expected_flags=expected_flags
    )

if __name__ == "__main__":
    app.run(debug=True)
