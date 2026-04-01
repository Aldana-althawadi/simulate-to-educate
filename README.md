# 🎮 PhishArena

## 🎯 Project Objective

PhishArena is an interactive cybersecurity training platform designed to help users understand how email communication can appear legitimate or suspicious.

The system trains users to write structured, credible emails while showing how incomplete, vague, or misleading messages can resemble phishing-like behavior.

PhishArena combines professional email writing practice with phishing-awareness training through a case-based game environment powered by real email infrastructure.

---

## 🚀 Quick Start (Setup)  

### 1. Clone
```bash
git clone https://github.com/Aldana-althawadi/PhishArena-_Game.git
cd PhishArena
```
### 2. Create venv
```bash
python3 -m venv env
source env/bin/activate
```
### 3. Install
```bash
pip install flask
```
### 4. Run
```bash
python3 app.py
```
The web interface will be available at: http://127.0.0.1:5000

---

## 📧 Thunderbird Configuration
PhishArena uses a real email environment. You must configure Thunderbird to send and receive emails through the local mail server.

### - Account Example
- Email: `player1@emailme.com`
- Username: player1
- Password: pass123


### - 📥 Incoming Mail (IMAP - Dovecot)
- Hostname: localhost
- Server: `127.0.0.1`
- Port: `143`
- Connection Security: None
- Authentication Method: Normal password


### - 📤 Outgoing Mail (SMTP - Postfix)
- Hostname: localhost
- Server: `127.0.0.1`
- Port: `25`
- Connection Security: None
- Authentication Method: None

---
## 🎮 How It Works
PhishArena is a case-based interactive game where users complete email scenarios to progress through levels.

### Game Flow

1. **Select a Level**  
   Navigate to the Levels page and choose an unlocked level.

2. **Open a Case**  
   Each level contains multiple cases. Open the first available case.

3. **Read the Mission Brief**  
   Review the scenario, profile details, and image hints carefully.

4. **Compose an Email**  
   Use Thunderbird to write and send your email to the target (e.g., Alice or Bob).  
   Your message must be clear, credible, and well-supported.

5. **Check Your Attempt**  
   Click **"Check My Attempt"** on the case page.  
   The system retrieves your latest email and evaluates it.

6. **Receive Feedback**  
   - If your message is **legitimate**, the case is completed and you progress  
   - If your message is **suspicious**, you must revise and resend

7. **Progress Through Levels**  
   Complete all cases in a level to unlock the next level.


### 🧠 Evaluation Logic

Your email is evaluated based on:

- Clarity
- Completeness
- Credibility

A strong message appears legitimate.  
A weak or misleading message is treated as suspicious (phishing-like behavior).

---

## 🧠 Core Concept
PhishArena is built on the idea that the difference between legitimate communication and phishing often lies in **how information is presented**, not just what is requested.

Instead of directly teaching users to detect phishing, the system trains them to:

- Write clear and structured emails  
- Provide sufficient and relevant information  
- Understand how missing or weak details reduce credibility  

### ✔ Legitimate Email

A message is considered legitimate when it is:

- Clear and well-structured  
- Supported with enough relevant details  
- Consistent and believable  
- Contextually appropriate  


### ⚠ Suspicious / Phishing-like Email

A message is treated as suspicious when it is:

- Vague or incomplete  
- Missing important supporting details  
- Misleading or poorly justified  
- Lacking credibility or context  

Through this approach, users learn both **professional communication skills** and how **phishing-like messages behave**, by experiencing how weak or misleading emails fail in realistic scenarios.

---

## 🏗 System Architecture
PhishArena is built using a combination of web technologies and real email infrastructure to simulate realistic communication scenarios.

### 🔧 Core Components

#### 🌐 Flask Web Application
- Handles frontend and backend logic  
- Manages routing, case progression, and user interaction  
- Displays levels, cases, dashboard, and results  


#### 📧 Mail Server (Postfix + Dovecot)

- **Postfix (SMTP)** → handles sending emails  
- **Dovecot (IMAP)** → handles receiving and storing emails  
- Emails are stored locally using **Maildir format**


#### 👤 User Management (OpenLDAP)

- Stores user accounts (e.g., Alice, Bob, player1)  
- Used for authentication and email identity  
- Enables realistic multi-user environment  


#### 💻 Email Client (Thunderbird)

- Used by the player to send emails  
- Connects to local mail server  
- Allows real-world email interaction instead of web forms  


#### 🤖 Email Evaluation (LLM Checker)

- Processes the user’s email  
- Verifies if required information is present  
- Evaluates clarity, completeness, and credibility  
- Returns feedback as legitimate or suspicious  


---
## 📁 Project Structure
PhishArena/
│
├── app.py # Main Flask application
│
├── cases/ # Game scenarios and helpers
│ ├── profiles.py # All cases and levels
│ ├── helpers.py # Case navigation logic
│
├── mail/ # Email handling
│ ├── mail_reader.py # Reads emails from Maildir
│ ├── smtp_sender.py # Sends responses via SMTP
│
├── llm/ # AI evaluation logic
│ ├── checker.py # Email validation and feedback
│
├── logs/ # Game logs
│ ├── game_logger.py # Stores results
│
├── templates/ # HTML pages
│ ├── index.html
│ ├── levels.html
│ ├── case.html
│ ├── dashboard.html
│ ├── rules.html
│
├── static/ # Static assets
│ ├── images/
│
└── README.md

---

## 👥 Contributors

- Aldana Althawadi
- Ghufran Sheikh
- Haya Alkaabi  


---

## 🏆 Academic Context

This project was developed as a final-year cybersecurity project focused on combining practical email communication training with phishing-awareness concepts using real-world infrastructure.

---

## 📌 Notes

This system is designed for **educational purposes only**.  
All scenarios are simulated within a controlled environment.

---

# 🎯 PhishArena  
Train smart. Think deeper. Communicate better.

