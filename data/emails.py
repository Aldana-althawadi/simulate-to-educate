
"""
Synthetic email dataset for phishing-awareness simulation.

Important note (for report honesty):
- These emails are synthetic (created by the project team) to avoid ethical/legal risk of distributing real phishing content.
- The structure and tactics are grounded in authoritative sources describing common phishing patterns.

Primary grounding sources (authoritative):
- CISA guidance on social engineering / phishing indicators (generic greetings, urgency, etc.).  :contentReference[oaicite:0]{index=0}
- NIST guidance and NIST TN 2276 / phish-related publications describing phishing as social engineering to induce clicks/credential entry. :contentReference[oaicite:1]{index=1}
- FBI IC3 / FBI resources describing Business Email Compromise (BEC) scams and their characteristics. :contentReference[oaicite:2]{index=2}
- Microsoft Security research on file hosting / file-sharing services being misused for identity phishing. :contentReference[oaicite:3]{index=3}
- FTC consumer guidance on fake prizes / sweepstakes scams (e.g., “You won” messages). :contentReference[oaicite:4]{index=4}
- APWG Phishing Activity Trends Reports describing the prevalence and evolving techniques of phishing and related fraud. :contentReference[oaicite:5]{index=5}
- ENISA threat landscape reporting phishing as a prevalent attack vector in fraud contexts. :contentReference[oaicite:6]{index=6}
"""

EMAILS = [
   
    # PHISHING (Obvious)

    # E1: Brand impersonation + urgency + suspicious link + threat language
    # Grounding: common phishing indicators: urgency + suspicious links + impersonation patterns
    # (CISA/NIST general indicators). :contentReference[oaicite:7]{index=7}
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

    # E2: Credential harvesting via password reset lure
    # Grounding: phishing attempts to induce user to click a link and provide credentials (NIST phishing guidance). :contentReference[oaicite:8]{index=8}
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

    # E3: Invoice scam + attachment lure (common financial phishing/fraud pattern)
    # Grounding: phishing/fraud often uses invoices and attachments to trigger action (NIST describes phishing inducing clicks/downloads). :contentReference[oaicite:9]{index=9}
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

   
    # PHISHING (More Realistic)

    # E4: Internal-portal / HR lure + credential request + generic greeting
    # Grounding: generic greeting + credential request are common social engineering indicators (CISA). :contentReference[oaicite:10]{index=10}
    # Also consistent with NIST definition of phishing as inducing credentials via fraudulent sites. :contentReference[oaicite:11]{index=11}
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

    # E5: File-sharing lure + suspicious link + expiry pressure
    # Grounding: Microsoft reports identity phishing campaigns misusing file hosting/sharing services. :contentReference[oaicite:12]{index=12}
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
        "expected_type": "File-share / Link-based Phishing",
        "expected_flags": ["F1", "F3"],
        "difficulty": "medium"
    },

    # E6: Business Email Compromise (BEC) style request for transfer + secrecy
    # Grounding: FBI IC3 / FBI describe BEC as scams targeting payments/transfers via business email. :contentReference[oaicite:13]{index=13}
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

    # PHISHING (Language / Errors)

    # E7: Typos/grammar errors + urgency + suspicious link
    # Grounding: CISA highlights common phishing indicators like poor grammar and suspicious links. :contentReference[oaicite:14]{index=14}
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


    # LEGITIMATE EMAILS

    # E8-E10: Legitimate internal/normal service messages included to measure false positives.
    # Grounding: NIST/CISA recommend verifying context and avoiding over-trusting “security-looking” messages. :contentReference[oaicite:15]{index=15}
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

    
    # BORDERLINE / GRAY CASES

    # E11: Legit security alert style (borderline) to test over-flagging.
    # Grounding: NIST discusses phishing as social engineering; legitimate alerts exist too,
    # so evaluation should include borderline cases to measure false positives. :contentReference[oaicite:16]{index=16}
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
        "expected_flags": ["F1"],  # mild urgency can appear in legitimate security notices
        "difficulty": "hard"
    },

    # E12: Prize/gift lure + urgency + suspicious link
    # Grounding: FTC describes “you won a prize” scams as common fraud patterns. :contentReference[oaicite:17]{index=17}
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
