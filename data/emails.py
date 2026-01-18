# data/emails.py

EMAILS = [
    # -------------------------
    # PHISHING (Obvious)
    # -------------------------
    {
        "id": "E1",
        "title": "Facebook Security Alert",
        "sender": "support@faceb0ok.com",
        "subject": "Immediate Action Required",
        "body": (
            "We detected suspicious activity on your Facebook account.\n"
            "Your account will be suspended in 24 hours.\n"
            "Verify now: http://fb-security-check[.]com"
        ),
        "expected_is_phishing": True,
        "expected_type": "Brand Impersonation",
        "expected_flags": ["F1", "F2", "F3", "F9"],
        "difficulty": "easy"
    },
    {
        "id": "E2",
        "title": "Password Reset Request",
        "sender": "no-reply@outlook-security.com",
        "subject": "Reset your password now",
        "body": (
            "Someone requested a password reset for your email.\n"
            "If this was not you, confirm your password here:\n"
            "http://outlook-reset-login[.]com"
        ),
        "expected_is_phishing": True,
        "expected_type": "Account Recovery / Password Reset",
        "expected_flags": ["F2", "F3", "F4"],
        "difficulty": "easy"
    },
    {
        "id": "E3",
        "title": "Invoice Attached",
        "sender": "billing@company-payments.com",
        "subject": "Invoice Attached - Payment Due",
        "body": (
            "Hello,\n"
            "Please pay the attached invoice today to avoid late fees.\n"
            "Attachment: invoice.pdf"
        ),
        "expected_is_phishing": True,
        "expected_type": "Financial Request",
        "expected_flags": ["F6", "F8"],
        "difficulty": "easy"
    },

    # -------------------------
    # PHISHING (More Realistic)
    # -------------------------
    {
        "id": "E4",
        "title": "HR Document Update",
        "sender": "hr-team@company-portal.com",
        "subject": "Updated Employee Policy Document",
        "body": (
            "Dear Employee,\n"
            "We updated the employee policy document.\n"
            "Please review and sign in with your email credentials:\n"
            "https://company-portal-login.example.com"
        ),
        "expected_is_phishing": True,
        "expected_type": "Credential Theft",
        "expected_flags": ["F5", "F4", "F3"],
        "difficulty": "medium"
    },
    {
        "id": "E5",
        "title": "Shared File From Colleague",
        "sender": "share-notify@drive-files.com",
        "subject": "A file was shared with you",
        "body": (
            "You have been sent a file: 'Q1_Payroll_Updates.xlsx'\n"
            "Open the file here: http://drive-viewer[.]com/open?id=123\n"
            "Note: Access expires soon."
        ),
        "expected_is_phishing": True,
        "expected_type": "Suspicious Link",
        "expected_flags": ["F1", "F3"],
        "difficulty": "medium"
    },
    {
        "id": "E6",
        "title": "CEO Request (BEC)",
        "sender": "ceo.office@company-mail.com",
        "subject": "Urgent: Need a quick transfer",
        "body": (
            "Hi,\n"
            "I need you to make a quick transfer today.\n"
            "Do not discuss this with anyone.\n"
            "Reply when ready."
        ),
        "expected_is_phishing": True,
        "expected_type": "Business Email Compromise",
        "expected_flags": ["F1", "F8", "F9"],
        "difficulty": "hard"
    },

    # -------------------------
    # PHISHING (Language / Errors)
    # -------------------------
    {
        "id": "E7",
        "title": "Unusual Login Actvity",
        "sender": "alerts@security-service.com",
        "subject": "Unusal login actvity detected",
        "body": (
            "We detect unusal login actvity in your account.\n"
            "Verify now to keep safe: http://secure-verify[.]com"
        ),
        "expected_is_phishing": True,
        "expected_type": "Urgency / Fear",
        "expected_flags": ["F7", "F1", "F3"],
        "difficulty": "easy"
    },

    # -------------------------
    # LEGITIMATE EMAILS
    # -------------------------
    {
        "id": "E8",
        "title": "Team Meeting Reminder",
        "sender": "hr@company.com",
        "subject": "Team meeting tomorrow",
        "body": (
            "Reminder: our team meeting is tomorrow at 10 AM in Meeting Room 2.\n"
            "Agenda: sprint updates + blockers."
        ),
        "expected_is_phishing": False,
        "expected_type": "",
        "expected_flags": [],
        "difficulty": "easy"
    },
    {
        "id": "E9",
        "title": "University Announcement",
        "sender": "noreply@university.edu",
        "subject": "Library Hours Updated",
        "body": (
            "The library will be open from 8 AM to 10 PM during exam week.\n"
            "Good luck on your finals."
        ),
        "expected_is_phishing": False,
        "expected_type": "",
        "expected_flags": [],
        "difficulty": "easy"
    },
    {
        "id": "E10",
        "title": "Subscription Receipt",
        "sender": "receipts@service.com",
        "subject": "Your monthly receipt",
        "body": (
            "Thanks for your payment.\n"
            "Receipt ID: 847392\n"
            "If you have questions, contact support inside your account portal."
        ),
        "expected_is_phishing": False,
        "expected_type": "",
        "expected_flags": [],
        "difficulty": "medium"
    },

    # -------------------------
    # BORDERLINE / GRAY CASES (for evaluation)
    # -------------------------
    {
        "id": "E11",
        "title": "Account Alert (Borderline)",
        "sender": "security@service.com",
        "subject": "Security Alert: new login",
        "body": (
            "We noticed a new login to your account from a new device.\n"
            "If this was you, ignore this email.\n"
            "If not, reset your password in the official app settings."
        ),
        "expected_is_phishing": False,
        "expected_type": "",
        "expected_flags": ["F1"],  # borderline: urgency might appear but it's legitimate
        "difficulty": "hard"
    },
    {
        "id": "E12",
        "title": "Prize Offer",
        "sender": "rewards@promo-gift.com",
        "subject": "Congratulations! You won",
        "body": (
            "Congratulations! You won a gift card.\n"
            "Claim within 2 hours: http://promo-claim[.]com"
        ),
        "expected_is_phishing": True,
        "expected_type": "Gift / Prize Scam",
        "expected_flags": ["F10", "F1", "F3"],
        "difficulty": "easy"
    },
]
