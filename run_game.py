from email.utils import parseaddr

from mail.mail_reader import get_latest_email
from cases.helpers import get_active_case, advance_case, can_attempt_case
from llm.checker import check_email_against_case
from mail.smtp_sender import send_email_smtp
from logs.game_logger import log_game_event
from logs.log_reader import read_game_logs


def main():
    email_data = get_latest_email()

    if not email_data:
        print("No email found.")
        return

    sender_name, sender_email = parseaddr(email_data.get("from", ""))
    sender_email = sender_email.strip().lower()

    receiver = email_data.get("to", "").strip().lower()
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")

    if not sender_email:
        print("No valid sender email found.")
        return

    if not receiver:
        print("No valid receiver email found.")
        return

    print("\n=== CURRENT CASE ===")
    print(f"Player: {sender_email}")
    print(f"Target: {receiver}")

    case = get_active_case(receiver)

    if not case:
        print(f"No active case found for: {receiver}")
        return

    print(f"Case ID: {case['case_id']}")
    print(f"Title: {case['title']}")
    print(f"Level: {case['level']}")
    print("====================\n")

    # Read previous logs to check player progress and level unlock
    log_rows = read_game_logs()

    # Block attempts for locked levels
    if not can_attempt_case(case, log_rows, sender_email):
        locked_msg = (
            f"This case is locked. You must complete the previous level "
            f"before attempting {case['level']} cases."
        )

        print("=== GAME RESULT ===")
        print(f"Player: {sender_email}")
        print(f"Target: {receiver}")
        print(f"Case: {case['case_id']}")
        print("Status: LOCKED 🔒")
        print("Message:")
        print(locked_msg)
        print("===================\n")

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
            print("Locked reply sent successfully.")
        except Exception as e:
            print("Reply could not be delivered through mail.")
            print("Delivery error:", e)

        return

    # Normal case checking
    result = check_email_against_case(body, case)

    if result is None:
        print("ERROR: checker returned no result")
        return

    if "status" not in result or "msg" not in result:
        print("ERROR: checker result missing required fields")
        print("Returned result:", result)
        return

    print("=== GAME RESULT ===")
    print(f"Player: {sender_email}")
    print(f"Target: {receiver}")
    print(f"Case: {case['case_id']}")
    print(f"Status: {'SUCCESS ✅' if result['status'] else 'FAILED ❌'}")
    print("Message:")
    print(result["msg"])
    print("===================\n")

    # Advance only if successful
    if result["status"]:
        advanced = advance_case(receiver)

        if advanced:
            print("➡ Moving to next case...\n")
        else:
            print("🎉 All cases completed for this target!\n")

    # Log result
    log_game_event(
        player=sender_email,
        target=receiver,
        case_id=case["case_id"],
        level=case.get("level", ""),
        status=result["status"],
        flag=case.get("flag", "") if result["status"] else "",
        message=result["msg"]
    )

    # Send reply mail
    try:
        send_email_smtp(
            sender=receiver,
            recipient=sender_email,
            subject=f"Re: {subject}" if subject else "Re: Your Request",
            body=result["msg"],
            smtp_host="localhost",
            smtp_port=25
        )
        print("Reply sent successfully.")
    except Exception as e:
        print("Reply could not be delivered through mail.")
        print("Delivery error:", e)


if __name__ == "__main__":
    main()