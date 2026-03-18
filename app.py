from flask import Flask, render_template, request
from llm.pipeline import analyze_email_pipeline
from data.emails import EMAILS
from flask import jsonify
from mail.mail_reader import read_maildir
from mail.smtp_sender import send_email_smtp
from llm.reply_generator import generate_ai_reply
from flask import session, redirect, url_for
from ldap3 import Server, Connection, ALL
from logs.game_logger import log_game_result
import re
import secrets



app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
LDAP_SERVER = "ldap://127.0.0.1"
LDAP_BASE_DN = "dc=emailme,dc=com"
LDAP_USER_DN_FORMAT = "uid={},ou=users," + LDAP_BASE_DN


app.config["SESSION_PERMANENT"] = False

def extract_case_id(subject):
    match = re.search(r"\[(E\d+)\]", subject)
    if match:
        return match.group(1)
    return None

def get_email_by_id(email_id):
    for email in EMAILS:
        if email["id"] == email_id:
            return email
    return None

def authenticate_ldap(username, password):
    try:
        user_dn = LDAP_USER_DN_FORMAT.format(username)
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        conn.unbind()
        return True
    except Exception as e:
        print(f"LDAP authentication failed for {username}: {e}")
        return False
 
          

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/game/start", methods=["GET"])
def game_start():
    if "username" not in session:
        return redirect(url_for("login"))

    session["score"] = 0
    session["answered"] = []
    session["student_answers"] = {}

    # Show the game start page instead of immediately going to inbox
    return render_template("game_start.html")


@app.route("/game/inbox", methods=["GET"])
def game_inbox():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user_home = f"/home/{username}"
    answered = session.get("answered", [])

    try:
        emails = read_maildir(user_home, box="new", limit=50)
    except Exception as e:
        print(f"Mailbox read error: {e}")
        emails = []

    # Add case_id and answered status to each real email
    for email in emails:
        case_id = extract_case_id(email["subject"])
        email["case_id"] = case_id
        email["is_answered"] = case_id in answered if case_id else False

    return render_template(
        "real_inbox.html",
        emails=emails,
        username=username
    )


@app.route("/real/email/<filename>")
def real_email(filename):
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user_home = f"/home/{username}"

    try:
        emails = read_maildir(user_home, box="new", limit=50)
    except Exception as e:
        print(f"Mailbox read error: {e}")
        emails = []

    selected_email = None
    for email in emails:
        if email["file"] == filename:
            selected_email = email
            break

    if not selected_email:
        return "Email not found", 404

    # extract scenario ID from subject
    case_id = extract_case_id(selected_email["subject"])

    if not case_id:
        return "Scenario ID not found in subject", 400

    return render_template(
        "real_email.html",
        email=selected_email,
        case_id=case_id,   
        username=username
    )


@app.route("/game/email/<email_id>")
def game_email(email_id):
    if "username" not in session:
        return redirect(url_for("login"))

    email = get_email_by_id(email_id)
    if not email:
        return "Email not found", 404

    student_answers = session.get("student_answers", {})
    existing_answer = student_answers.get(email_id)

    return render_template(
        "game_email.html",
        email=email,
        existing_answer=existing_answer,
        username=session.get("username")
    )    


@app.route("/real/answer/<case_id>", methods=["POST"])
def real_answer(case_id):
    if "username" not in session:
        return redirect(url_for("login"))

    scenario = get_email_by_id(case_id)
    if not scenario:
        return "Scenario not found", 404

    answer = request.form.get("answer")
    if answer not in ["phishing", "legitimate"]:
        return "Invalid answer", 400

    expected = "phishing" if scenario["expected_is_phishing"] else "legitimate"

    answered = session.get("answered", [])
    student_answers = session.get("student_answers", {})
    score = session.get("score", 0)

    if case_id not in answered:
        answered.append(case_id)
        student_answers[case_id] = answer

        if answer == expected:
            score += 1

        email_text = f"""From: {scenario['sender']}
Subject: {scenario['subject']}

{scenario['body']}"""

    analysis = analyze_email_pipeline(email_text)
    ai_answer = "phishing" if analysis.get("is_phishing") else "legitimate"

    log_game_result(
        student_id=session.get("username"),
        email_id=case_id,
        expected_label=expected,
        student_answer=answer,
        ai_answer=ai_answer,
        difficulty=scenario.get("difficulty", "unknown")
    )


    session["answered"] = answered
    session["student_answers"] = student_answers
    session["score"] = score

    return redirect(url_for("real_feedback", case_id=case_id))   


@app.route("/game/result")
def game_result():
    if "username" not in session:
        return redirect(url_for("login"))

    answered = session.get("answered", [])
    score = session.get("score", 0)
    total = len(EMAILS)
    student_answers = session.get("student_answers", {})

    results = []
    for email in EMAILS:
        if email["id"] in student_answers:
            expected = "phishing" if email["expected_is_phishing"] else "legitimate"
            results.append({
                "id": email["id"],
                "subject": email["subject"],
                "student_answer": student_answers[email["id"]],
                "expected_answer": expected
            })

    return render_template(
        "game_result.html",
        score=score,
        total=total,
        answered_count=len(answered),
        results=results,
        username=session.get("username")
    )  


@app.route("/real/feedback/<case_id>")
def real_feedback(case_id):
    if "username" not in session:
        return redirect(url_for("login"))

    scenario = get_email_by_id(case_id)
    if not scenario:
        return "Scenario not found", 404

    student_answers = session.get("student_answers", {})
    score = session.get("score", 0)
    answered = session.get("answered", [])

    student_answer = student_answers.get(case_id)
    expected_answer = "phishing" if scenario["expected_is_phishing"] else "legitimate"

    # one email text string for the AI pipeline
    email_text = f"""From: {scenario['sender']}
Subject: {scenario['subject']}

{scenario['body']}"""

    # AI analysis
    analysis = analyze_email_pipeline(email_text)

    ai_answer = "phishing" if analysis.get("is_phishing") else "legitimate"
    session[f"logged_{case_id}"] = True
    ai_flags = analysis.get("flags", [])
    ai_explanation = analysis.get("explanation", "").strip()
    ai_confidence = analysis.get("confidence", 0.0)
    ai_type = analysis.get("phishing_type", "")

    # Logging student result                                                                                                                                         
    log_game_result(
    student_id=session.get("username"),
    email_id=case_id,
    expected_label=expected_answer,
    student_answer=student_answer,
    ai_answer=ai_answer,
    difficulty=scenario.get("difficulty", "unknown")
)
    

    if not ai_explanation:
        ai_explanation = "No detailed explanation was returned by the model."

    return render_template(
        "real_feedback.html",
        scenario=scenario,
        case_id=case_id,
        student_answer=student_answer,
        expected_answer=expected_answer,
        ai_answer=ai_answer,
        ai_flags=ai_flags,
        ai_explanation=ai_explanation,
        ai_confidence=ai_confidence,
        ai_type=ai_type,
        current_score=score,
        answered_count=len(answered),
        total=len(EMAILS),
        username=session.get("username")
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if authenticate_ldap(username, password):
            session.clear()

            session["username"] = username
            return redirect(url_for("game_start"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return f"Welcome, {session['username']}! You are logged in."    

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/reset")
def reset_game():

    session.clear()

    return redirect(url_for("login"))


@app.route("/analyze_ui", methods=["POST"])
def analyze_ui():
    # Accept JSON from fetch()
    payload = request.get_json(force=True)

    sender = payload.get("sender", "")
    subject = payload.get("subject", "")
    body = payload.get("body", "")

    email_text = payload.get("email_text")
    if not email_text:
        email_text = f"Subject: {subject}\nFrom: {sender}\n\n{body}"

    # Run pipeline
    result = analyze_email_pipeline(email_text)

    # Convert flags safely
    flags_list = result.get("flags", []) or []
    model_flags = ";".join([str(x) for x in flags_list])

    # Log event
    log_event({
        "ts": now_iso(),
        "email_id": "manual-ui",
        "expected_is_phishing": "",
        "model_is_phishing": result.get("is_phishing"),
        "expected_type": "",
        "model_type": result.get("phishing_type", ""),
        "expected_flags": "",
        "model_flags": model_flags,
        "confidence": result.get("confidence", 0.0),
    })

    # Return result block
    return render_template(
        "analysis_result.html",
        result=result,
        sender=sender,
        subject=subject
    )

BOB_HOME = "/home/bob"


@app.get("/api/inbox/<username>")
def api_inbox(username):
    box = request.args.get("box", "new")
    limit = int(request.args.get("limit", 20))
    user_home = f"/home/{username}"

    emails = read_maildir(user_home, box=box, limit=limit)
    return jsonify({"count": len(emails), "emails": emails})


@app.post("/api/reply/hello/<username>")
def api_reply_hello(username):
    payload = request.get_json(force=True)
    to_addr = payload.get("to", "")
    subject = payload.get("subject", "")

    if not to_addr:
        return jsonify({"ok": False, "error": "Missing 'to'"}), 400

    sender_email = f"{username}@emailme.com"

    send_email_smtp(
        sender=sender_email,
        recipient=to_addr,
        subject=f"Re: {subject}" if subject else "Re:",
        body="hello"
    )
    return jsonify({"ok": True})



@app.post("/api/reply/ai/<username>")
def api_reply_ai(username):
    payload = request.get_json(force=True)

    to_addr = payload.get("to", "")
    subject = payload.get("subject", "")
    email_text = payload.get("email_text", "")

    if not to_addr or not email_text:
        return jsonify({"ok": False, "error": "Missing 'to' or 'email_text'"}), 400

    sender_email = f"{username}@emailme.com"

    out = generate_ai_reply(email_text)
    reply_text = out["reply_text"]
    analysis = out["analysis"]

    send_email_smtp(
        sender=sender_email,
        recipient=to_addr,
        subject=f"Re: {subject}" if subject else "Re:",
        body=reply_text
    )

    return jsonify({"ok": True, "analysis": analysis}) 

    
           


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
