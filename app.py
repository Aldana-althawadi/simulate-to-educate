from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from email.utils import parseaddr

from cases.profiles import CASES
from cases.helpers import (
    get_progress_summary,
    get_all_cases,
    get_case_by_id,
    get_cases_by_level_sorted,
    is_case_completed,
    get_first_incomplete_case_in_level,
    can_open_case,
    get_next_case_in_level,
)
from logs.log_reader import read_game_logs
from logs.game_logger import log_game_event
from mail.mail_reader import get_latest_email
from mail.smtp_sender import send_email_smtp
from llm.checker import check_email_against_case

app = Flask(__name__)
app.secret_key="stoe"

PLAYER_EMAIL = "player1@emailme.com"
PLAYER_USERNAME = "player1"


@app.route("/")
def home():
    log_rows = read_game_logs()
    progress = get_progress_summary(log_rows, PLAYER_EMAIL)

    return render_template(
        "index.html",
        username=PLAYER_USERNAME,
        player_email=PLAYER_EMAIL,
        total_targets=len(CASES),
        total_cases=sum(len(profile.get("cases", [])) for profile in CASES.values()),
        total_levels=len(progress["levels"]),
        total_flags=progress["total_flags"],
        progress=progress,
    )


@app.route("/profiles")
def profiles():
    return render_template(
        "profiles.html",
        username=PLAYER_USERNAME,
        player_email=PLAYER_EMAIL,
    )


@app.route("/levels")
def levels():
    log_rows = read_game_logs()
    progress = get_progress_summary(log_rows, PLAYER_EMAIL)

    selected_level = request.args.get("level", "Junior")
    level_cases = get_cases_by_level_sorted(selected_level)

    for case in level_cases:
        case["completed"] = is_case_completed(case["case_id"], progress["completed_case_ids"])
        case["openable"] = can_open_case(case, progress["completed_case_ids"])

    selected_level_unlocked = selected_level in progress["unlocked_levels"]

    return render_template(
        "levels.html",
        username=PLAYER_USERNAME,
        player_email=PLAYER_EMAIL,
        progress=progress,
        selected_level=selected_level,
        level_cases=level_cases,
        selected_level_unlocked=selected_level_unlocked,
    )

@app.route("/case/<case_id>")
def case_page(case_id):
    log_rows = read_game_logs()
    progress = get_progress_summary(log_rows, PLAYER_EMAIL)

    case = get_case_by_id(case_id)
    if not case:
        return "Case not found", 404

    case_completed = is_case_completed(case_id, progress["completed_case_ids"])
    case_openable = can_open_case(case, progress["completed_case_ids"])
    next_case = get_next_case_in_level(case)

    feedback = session.pop(f"feedback_{case_id}", None)

    return render_template(
        "case.html",
        username=PLAYER_USERNAME,
        player_email=PLAYER_EMAIL,
        case=case,
        case_completed=case_completed,
        case_openable=case_openable,
        next_case=next_case,
        feedback=feedback,
    )

@app.post("/case/<case_id>/process")
def process_case(case_id):
    log_rows = read_game_logs()
    progress = get_progress_summary(log_rows, PLAYER_EMAIL)

    case = get_case_by_id(case_id)
    if not case:
        return jsonify({"ok": False, "message": "Case not found."}), 404

    if not can_open_case(case, progress["completed_case_ids"]):
        return jsonify({"ok": False, "message": "This case is locked right now."}), 403

    email_data = get_latest_email()

    if not email_data:
        return jsonify({"ok": False, "message": "No email found."}), 404

    sender_name, sender_email = parseaddr(email_data.get("from", ""))
    sender_email = sender_email.strip().lower()

    receiver = email_data.get("to", "").strip().lower()
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")

    if sender_email != PLAYER_EMAIL:
        return jsonify({
            "ok": False,
            "message": f"Latest email is not from {PLAYER_EMAIL}."
        }), 400

    if receiver != case["target_email"]:
        return jsonify({
            "ok": False,
            "message": f"Latest email was not sent to {case['target_email']}."
        }), 400

    result = check_email_against_case(body, case)

    if not result or "status" not in result or "msg" not in result:
        return jsonify({"ok": False, "message": "Checker returned invalid result."}), 500

    log_game_event(
        player=sender_email,
        target=receiver,
        case_id=case["case_id"],
        level=case.get("level", ""),
        status=result["status"],
        flag=case.get("flag", "") if result["status"] else "",
        message=result["msg"]
    )

    try:
        send_email_smtp(
            sender=receiver,
            recipient=sender_email,
            subject=f"Re: {subject}" if subject else "Re: Your Request",
            body=result["msg"],
            smtp_host="localhost",
            smtp_port=25
        )
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Reply could not be delivered: {str(e)}"
        }), 500

    session[f"feedback_{case_id}"] = {
        "status": result["status"],
        "message": result["msg"]
    }

    return jsonify({
        "ok": True,
        "status": "success" if result["status"] else "failed",
        "message": result["msg"],
        "redirect_url": url_for("case_page", case_id=case_id)
    })


@app.route("/rules")
def rules():
    return render_template(
        "rules.html",
        username=PLAYER_USERNAME,
        player_email=PLAYER_EMAIL,
    )

@app.route("/dashboard")
def dashboard():
    log_rows = read_game_logs()
    progress = get_progress_summary(log_rows, PLAYER_EMAIL)
    active_cases = get_available_active_cases_for_player(log_rows, PLAYER_EMAIL)

    return render_template(
        "dashboard.html",
        username=PLAYER_USERNAME,
        player_email=PLAYER_EMAIL,
        progress=progress,
        active_cases=active_cases,
    )


@app.post("/process-latest-email")
def process_latest_email():
    email_data = get_latest_email()

    if not email_data:
        return jsonify({
            "ok": False,
            "message": "No email found."
        }), 404

    sender_name, sender_email = parseaddr(email_data.get("from", ""))
    sender_email = sender_email.strip().lower()

    receiver = email_data.get("to", "").strip().lower()
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")

    if not sender_email or not receiver:
        return jsonify({
            "ok": False,
            "message": "Missing sender or receiver."
        }), 400

    case = get_active_case(receiver)
    if not case:
        return jsonify({
            "ok": False,
            "message": f"No active case found for {receiver}."
        }), 404

    log_rows = read_game_logs()

    if not can_attempt_case(case, log_rows, sender_email):
        locked_msg = (
            f"This case is locked. You must complete the previous level "
            f"before attempting {case['level']} cases."
        )

        log_game_event(
            player=sender_email,
            target=receiver,
            case_id=case["case_id"],
            level=case.get("level", ""),
            status=False,
            flag="",
            message=locked_msg
        )

        try:
            send_email_smtp(
                sender=receiver,
                recipient=sender_email,
                subject=f"Re: {subject}" if subject else "Re: Your Request",
                body=locked_msg,
                smtp_host="localhost",
                smtp_port=25
            )
        except Exception as e:
            return jsonify({
                "ok": False,
                "message": f"Lock reply could not be delivered: {str(e)}"
            }), 500

        return jsonify({
            "ok": True,
            "status": "locked",
            "case_id": case["case_id"],
            "level": case["level"],
            "message": locked_msg
        })

    result = check_email_against_case(body, case)

    if not result or "status" not in result or "msg" not in result:
        return jsonify({
            "ok": False,
            "message": "Checker returned invalid result."
        }), 500

    if result["status"]:
        advanced = advance_case(receiver)
    else:
        advanced = False

    log_game_event(
        player=sender_email,
        target=receiver,
        case_id=case["case_id"],
        level=case.get("level", ""),
        status=result["status"],
        flag=case.get("flag", "") if result["status"] else "",
        message=result["msg"]
    )

    try:
        send_email_smtp(
            sender=receiver,
            recipient=sender_email,
            subject=f"Re: {subject}" if subject else "Re: Your Request",
            body=result["msg"],
            smtp_host="localhost",
            smtp_port=25
        )
    except Exception as e:
        return jsonify({
            "ok": False,
            "message": f"Reply could not be delivered: {str(e)}"
        }), 500

    return jsonify({
        "ok": True,
        "status": "success" if result["status"] else "failed",
        "case_id": case["case_id"],
        "level": case["level"],
        "advanced": advanced,
        "message": result["msg"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)