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

---

### - 📥 Incoming Mail (IMAP - Dovecot)
- Hostname: localhost
- Server: `127.0.0.1`
- Port: `143`
- Connection Security: None
- Authentication Method: Normal password

---

### - 📤 Outgoing Mail (SMTP - Postfix)
- Hostname: localhost
- Server: `127.0.0.1`
- Port: `25`
- Connection Security: None
- Authentication Method: None

---

### 🧠 Important Notes

- All services run locally inside the Ubuntu VM.
- Emails are stored in Maildir format:/home/<user>/Maildir/

---
### 🔄 Game Flow

1. Open a case in the web interface  
2. Write your email in Thunderbird  
3. Send it to the target (Alice or Bob)  
4. Click **Check My Attempt**  
5. The system evaluates your email and sends a reply  
6. View the response in Thunderbird  

---

## 🎮 How It Works

---

## 🧠 Core Concept

---

## 🏗 System Architecture

---

## 📊 Features

---

## 🚀 Future Improvements

---

## 👥 Contributors
