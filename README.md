<div align="center">
  <h1>🌟 Qatar Foundation — Admin Portal</h1>
  <p><i>A robust, Flask-powered backend serving a sleek Admin Dashboard for managing platform opportunities.</i></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  </p>
</div>

---

## 📖 Overview

This repository contains the backend implementation for the **Qatar Foundation Admin Portal**. Built as part of a full-stack assessment, it focuses on delivering a secure, session-managed RESTful API using **Python** and **Flask** to seamlessly integrate with an existing, pre-built frontend UI.

The platform empowers administrators to manage opportunities (like internships or courses) dynamically, ensuring data persistence, user authentication, and a smooth, asynchronous user experience.

---



## ✨ Key Features & User Stories Implemented

### 🔐 Task 1: Authentication & Security
- **Admin Sign Up:** Secure registration with email validation, strong password enforcement, and duplicate account prevention.
- **Admin Login:** Robust authentication with session management. Features a "Remember Me" toggle for persistent vs. browser-session login states.
- **Forgot Password:** Privacy-focused password recovery flow generating time-limited (1-hour) reset links.

### 💼 Task 2: Opportunity Management
- **View Opportunities:** Dynamic dashboard displaying opportunities exclusively created by the currently logged-in admin (Multi-tenant architecture).
- **Add Opportunity:** Comprehensive form with field validation for Name, Duration, Start Date, Description, Skills, Category, etc. Updates UI asynchronously without page reloads.
- **Data Persistence:** All opportunities are securely stored in the SQLite database.
- **View Details:** Interactive modals displaying full details of each opportunity.
- **Edit & Update:** Pre-filled edit forms allowing admins to instantly update records.
- **Secure Deletion:** Protected delete functionality with confirmation dialogues, ensuring admins can only delete their own data.

---

## 🛠️ Tech Stack

- **Backend Logic:** Python 3.x
- **Web Framework:** Flask
- **Database:** SQLite (using SQLAlchemy / Flask-SQLAlchemy)
- **Frontend:** HTML, CSS, JavaScript (Fetch API for asynchronous DOM updates)

---

## 🚀 Getting Started

Follow these steps to run the application locally on your machine.

### Prerequisites
- Python 3.8+ installed on your system.
- Git.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/darshan-gowdaa/admin-portal-backend-py-flask.git
   cd admin-portal-backend-py-flask
   ```

2. **Create and activate a virtual environment**
   - **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask Application**
   ```bash
   python run.py
   ```
   *The server will typically start on `http://127.0.0.1:5000`.*

5. **Access the Portal**
   Open your browser and navigate to `http://127.0.0.1:5000` to view the Admin Portal!

   > **Note on Credentials:** There are no pre-configured default accounts. Please use the "Sign Up" page to create a new admin account. Any usernames, emails, and passwords shown in screenshots or testing scripts are purely dummy credentials for demonstration purposes only.

---

## 📂 Project Structure

```text
📦 admin-portal-backend
 ┣ 📂 app
 ┃ ┣ 📜 routes.py       # API endpoints and route handlers
 ┃ ┣ 📜 models.py       # Database schema
 ┃ ┗ 📜 ...             # Core application logic
 ┣ 📂 frontend          # Static UI files provided for the assessment
 ┣ 📜 database.db       # SQLite Database
 ┣ 📜 run.py            # Application entry point
 ┣ 📜 requirements.txt  # Python dependencies
 ┣ 📜 test_all.py       # Test scripts
 ┗ 📜 README.md         # Project documentation
```

---

## 🎯 Final Assessment Notes
- **Frontend Integrity:** The provided frontend UI was left completely untouched as per the strict assessment requirements.
- **Backend Architecture:** RESTful endpoints were meticulously designed to support the pre-built JavaScript fetch calls, ensuring the UI remains highly responsive.
- **Data Isolation:** Complete data privacy has been achieved; sessions securely link entries so admins solely view and interact with their own data.

<br>
