# Flag-Based UI Educational Mapping

This document defines how phishing indicators (flags) are presented
to users in the Phishing Awareness Training Simulator.

The goal is to transform detection results into an educational
experience that helps users understand phishing techniques.

---

## 1. Result Overview Section

This section appears at the top of the result page.

It should display:
- Final classification: Phishing or Legitimate
- Confidence score (percentage)

Example:
Result: ⚠️ Phishing  
Confidence: 82%

This gives the user immediate feedback before explanations.

---

## 2. Detected Phishing Indicators (Flags)

For each detected phishing flag, the system should display the
following educational elements:

- Flag name  
- What it means (description)  
- Why attackers use this technique  
- What the user should do  

Each flag explanation should be shown clearly and separately.

### Example Flag Display:

Urgency / Fear  
What it means: The message pressures the user to act quickly.  
Why attackers use it: Urgency reduces critical thinking and increases impulsive actions.  
What you should do: Pause and verify the message using official channels.

This section is the core learning component of the simulator.

---

## 3. Risk Explanation Summary

Below the flags, the system should present a short paragraph
summarizing why the email is risky or suspicious.

This summary should:
- Combine all detected flags
- Explain how they work together
- Avoid technical language

Example:
This email combines urgency with impersonation and suspicious links.
These techniques are commonly used in phishing attacks to trick users
into revealing sensitive information or credentials.

---

## 4. Learning Tip Section

Every analyzed email should end with a practical learning tip.

The learning tip should:
- Be actionable
- Reflect real-world best practices
- Encourage safe user behavior

Example:
Learning Tip:
Do not click links from urgent security emails.
Instead, manually visit the official website and check your account.

---

## 5. Borderline and Legitimate Cases

Some legitimate emails may contain phishing-like indicators
(e.g., urgency).

For borderline cases, the UI should display an educational note:

Important Note:
This email contains one phishing indicator (such as urgency),
but it is classified as legitimate.
A single indicator does not automatically mean phishing.
Always evaluate the sender, context, and message content together.

This reinforces critical thinking rather than rule-based decisions.

---

## 6. Educational Objective

The purpose of this UI design is not only to classify emails,
but to educate users by:
- Explaining phishing techniques
- Highlighting attacker psychology
- Teaching safer decision-making skills

This approach supports phishing awareness training rather than
simple automated detection.
