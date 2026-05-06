<div align="center">

<img src="https://iconape.com/wp-content/files/hz/20759/png/Qatar-Foundation-01.png" width="100" alt="Qatar Foundation Logo"/>

# Qatar Foundation — Admin Portal
### Universal Skills Passport · مؤسسة قطر

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-22c55e?style=for-the-badge)]()

*A full-stack admin portal for managing opportunities, learners, verifiers, and collaborators — built on Flask + SQLite with a pre-designed modern UI.*

**My Repo** · [github.com/darshan-gowdaa/admin-portal-backend-py-flask](https://github.com/darshan-gowdaa/admin-portal-backend-py-flask)

[Features](#-features) · [Screenshots](#-screenshots) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Architecture](#-architecture) · [Tests](#-running-tests)

---

<p align="center"> <a href="https://drive.google.com/file/d/1d-CmdBSWoVJl9tIseu0rKCgbN8Hsqudk/view?usp=drive_link"> <img src="https://img.shields.io/badge/▶️%20Watch%20Demo%20Video-Open%20in%20Google%20Drive-4285F4?style=for-the-badge&logo=google-drive&logoColor=white" /> </a> </p>


---

</div>



## 🧩 Project Context

This is a **full-stack intern assessment** for CertifyMe / Qatar Foundation.

| Part | Source | Author |
|---|---|---|
| **Frontend** (HTML, CSS, JS) | Cloned from [Neerajvs32/Test1](https://github.com/Neerajvs32/Test1) | Original UI owner |
| **Backend** (Flask, SQLAlchemy, auth, API) | Built from scratch | [Darshan Gowda](https://github.com/darshan-gowdaa) |

> The `frontend/` directory (`admin.html`, `admin.css`, `admin.js`) was **not modified**. Every line of Python — models, routes, app factory, tests — was written independently to power the existing UI.

---

## 📸 Screenshots

### Task 1 — Login & Signup

#### US-1.1 · Admin Sign Up

<img src="https://github.com/user-attachments/assets/f9f98503-4b84-4aaa-b7cb-c8fed669721e" width="100%" alt="Sign Up Page"/>

<br/>

> **Duplicate email error** — shown when account already exists

<img src="https://github.com/user-attachments/assets/de85400a-3f6c-479e-8f02-5d1eccf17512" width="100%" alt="Sign Up — Email Already Exists"/>

---

#### US-1.2 · Admin Login

<img src="https://github.com/user-attachments/assets/6a04bb7b-8c26-46be-9292-5c67f18e750e" width="100%" alt="Login Page"/>

---

#### US-1.3 · Forgot Password

<table>
<tr>
<td width="60%">

**Forgot Password Form**

<img src="https://github.com/user-attachments/assets/ceb9c87b-011f-44e7-ae07-a91011ac84cf" width="100%" alt="Forgot Password"/>

</td>
<td width="40%">

**Reset token saved in DB**

<img src="https://github.com/user-attachments/assets/396a7cfc-0bd5-41bf-a735-aece2438e200" width="100%" alt="Password Reset Token in Database"/>

</td>
</tr>
</table>

---

### Task 2 — Opportunity Management

#### US-2.1 · View All Opportunities

<img src="https://github.com/user-attachments/assets/50355583-f39e-4091-b487-59a60bbc554a" width="100%" alt="View All Opportunities"/>

---

#### US-2.2 · Add New Opportunity

<table>
<tr>
<td width="50%">

**Form — top half**

<img src="https://github.com/user-attachments/assets/5dae4dcb-41df-44d4-b673-be2b6f75e177" width="100%" alt="Add Opportunity Modal — Top"/>

</td>
<td width="50%">

**Form — bottom half**

<img src="https://github.com/user-attachments/assets/9e47a938-86e2-4cdf-833e-ba2b97abd403" width="100%" alt="Add Opportunity Modal — Bottom"/>

</td>
</tr>
</table>

<br/>

**Opportunity card created and visible immediately (no page refresh)**

<img src="https://github.com/user-attachments/assets/310a7f4c-2364-4fcf-9c48-b01307294342" width="100%" alt="Opportunity Card Added to Grid"/>

---

#### US-2.4 · View Opportunity Details

<img src="https://github.com/user-attachments/assets/a195bdf5-4ceb-4ec6-b4ac-50c940af0afd" width="100%" alt="Opportunity Details Modal"/>

---

#### US-2.5 · Edit Opportunity

<img src="https://github.com/user-attachments/assets/d92ad40d-b0db-4fba-96d7-0f21ed072092" width="100%" alt="Edit Opportunity — Pre-filled Modal"/>

---

#### US-2.6 · Delete Confirmation

<img src="https://github.com/user-attachments/assets/bfb14295-1daa-4380-bfa8-23725d42f986" width="100%" alt="Delete Confirmation Dialog"/>

---

## ✨ Features

### 🔐 Authentication
| Feature | Detail |
|---|---|
| Signup | Full name, email, password validation + duplicate detection |
| Login | Password verification, generic error messages, session management |
| Remember Me | Long-lived persistent cookie vs session-scoped cookie |
| Forgot Password | Privacy-safe response regardless of email existence |
| Reset Password | Tokenized reset link (1-hour expiry, single-use), logged to console |
| CAPTCHA | Client-side 5-char alphanumeric CAPTCHA on all auth forms |

### 📋 Opportunity Management
| Feature | Detail |
|---|---|
| Create | 7 required fields + 1 optional, category validation, instant DOM injection |
| Read | Per-admin filtered list, empty-state message when none exist |
| Update | Pre-filled edit modal, same validation as create, instant card update |
| Delete | Confirmation dialog, permanent DB delete, instant DOM removal |
| Isolation | Admins can only see, edit, and delete their own opportunities |
| Persistence | SQLite storage — data survives logout/login cycles |

### 📊 Dashboard Modules
- **Learner Management** — student table with status filters, course grid, bulk upload + quick-add modals
- **Verifier Management** — verifier table with stats, subject breakdown, student progress
- **Collaborator Management** — submitted course approval/rejection workflow
- **Reports & Analytics** — engagement trend charts, completion rates, verification status, level distribution

---

## 🏗 Architecture

```
admin-portal-backend-py-flask/
│
├── app/
│   ├── __init__.py          # Flask app factory, CORS, LoginManager, blueprints
│   ├── models.py            # SQLAlchemy models: Admin, PasswordResetToken, Opportunity
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # /auth/* — signup, login, logout, forgot/reset password, status
│       └── opportunities.py # /api/opportunities/* — full CRUD, ownership enforcement
│
├── frontend/                # Cloned from Neerajvs32/Test1 — NOT modified
│   ├── admin.html
│   ├── admin.css
│   └── admin.js
│
├── run.py                   # Entry point
├── test_all.py              # Full integration test suite (stdlib only)
├── requirements.txt
└── database.db              # Auto-created on first run (gitignored)
```

### Data Model

```
Admin ──────────────────────────────────────────────── Opportunity
  id            PK                                       id            PK
  full_name                                              admin_id      FK → Admin.id
  email         UNIQUE                                   name
  password_hash                                          category
  │                                                      duration
  └─── PasswordResetToken                                start_date
         id            PK                                description
         admin_id      FK → Admin.id                     skills_to_gain
         token         UNIQUE                            future_opportunities
         expires_at                                      max_applicants  (nullable)
         used          BOOLEAN                           created_at
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### 1. Clone this repo
```bash
git clone https://github.com/darshan-gowdaa/admin-portal-backend-py-flask.git
cd admin-portal-backend-py-flask
```

### 2. Virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
python run.py
```

Open **http://localhost:5000** — `database.db` is auto-created on first boot, no migrations needed.

---

## 🔌 API Reference

All endpoints return JSON. Auth endpoints live under `/auth`, opportunity endpoints under `/api/opportunities`.

### Authentication

#### `POST /auth/signup`
Create a new admin account.

**Request** *(Note: These are dummy credentials for illustration)*
```json
{
  "full_name": "Jane Smith",
  "email": "jane@qf.org.qa",
  "password": "Secure123!",
  "confirm_password": "Secure123!"
}
```

| Status | Meaning |
|---|---|
| `201` | Account created |
| `400` | Validation failure (missing field, invalid email, short/mismatched password) |
| `409` | Email already registered |

---

#### `POST /auth/login`
Authenticate an existing admin.

**Request** *(Note: Uses dummy credentials)*
```json
{
  "email": "jane@qf.org.qa",
  "password": "Secure123!",
  "remember_me": true
}
```

| Status | Meaning |
|---|---|
| `200` | Login successful — session cookie set |
| `401` | `"Invalid email or password"` (generic — never reveals which field failed) |

---

#### `POST /auth/logout`
End the current session. Requires authentication. Returns `200 OK`.

---

#### `POST /auth/forgot-password`

**Request** — `{ "email": "jane@qf.org.qa" }`

Always returns `200` with identical message regardless of whether email exists. Reset link is logged to server console only.

---

#### `GET /auth/reset-password/<token>`
Validate a reset token — `200` valid, `400` invalid/expired/used.

#### `POST /auth/reset-password/<token>`

**Request** — `{ "password": "NewPass456!" }`

| Status | Meaning |
|---|---|
| `200` | Password updated — token marked used |
| `400` | Token invalid / expired / already used, or password too short |

---

#### `GET /auth/status`
Check current session — used on page load to restore dashboard without re-login.

```json
{ "logged_in": true, "admin": { "id": 1, "full_name": "Jane Smith", "email": "jane@qf.org.qa" } }
```

---

### Opportunities

> All endpoints require an active session. Admins only access their own data.

#### `GET /api/opportunities/`
Returns all opportunities for the logged-in admin, ordered newest first.

#### `POST /api/opportunities/`
Create a new opportunity linked to the logged-in admin.

**Required:** `name`, `category`, `duration`, `start_date`, `description`, `skills_to_gain`, `future_opportunities`

**Optional:** `max_applicants` (positive integer)

**Valid categories:** `Technology`, `Business`, `Design`, `Marketing`, `Data Science`, `Other`

| Status | Meaning |
|---|---|
| `201` | Created — returns full object |
| `400` | Validation failure |
| `401` | Not authenticated |

#### `GET /api/opportunities/<id>`

| Status | Meaning |
|---|---|
| `200` | Returns opportunity object |
| `403` | Belongs to another admin |
| `404` | Not found |

#### `PUT /api/opportunities/<id>`
Same validation rules as POST.

| Status | Meaning |
|---|---|
| `200` | Updated — returns full object |
| `400` | Validation failure |
| `403` | Not owner |
| `404` | Not found |

#### `DELETE /api/opportunities/<id>`

| Status | Meaning |
|---|---|
| `200` | Deleted |
| `403` | Not owner |
| `404` | Not found |

---

## 🧪 Running Tests

Uses only Python stdlib — no pytest or extra packages required.

```bash
# Terminal 1 — start server
python run.py

# Terminal 2 — run tests
python test_all.py
```

### Test Coverage

| Area | Tests |
|---|---|
| Signup | Success, duplicate email, missing fields, invalid email, short password, password mismatch |
| Login | Success, wrong password, nonexistent user |
| Forgot Password | Registered email, unregistered email (privacy parity), correct message format |
| CRUD | Create, read single, read list, update, delete, 404 after delete |
| Validation | Missing required fields, invalid category, negative max_applicants |
| Cross-admin isolation | Admin B cannot read/edit/delete Admin A's data, list returns empty |
| Password reset | Full flow: trigger → read DB token → validate → set new password → reuse blocked → login new/old |
| Logout protection | POST-logout GET and POST both blocked with 401 |
| Static files | `/`, `/admin.css`, `/admin.js` all serve 200 |

```
=== FINAL RESULTS: 42 passed, 0 failed ===
ALL TESTS PASSED
```

---

## 🔒 Security

- Passwords hashed with **Werkzeug PBKDF2-SHA256** (`generate_password_hash`)
- Login errors **generic** — never reveals which field failed
- Reset tokens **cryptographically random** (`secrets.token_urlsafe(32)`)
- Reset tokens **expire after 1 hour**, **single-use** (marked `used=True` after consumption)
- Forgot-password always returns **identical response** regardless of email existence
- All opportunity routes enforce **ownership** — 403 on cross-admin access
- `HttpOnly` + `SameSite=Strict` on session and remember-me cookies
- User input sanitized via `escapeHtml()` before DOM injection

---

## ⚙️ Configuration

| Key | Default | Description |
|---|---|---|
| `SECRET_KEY` | *(secure random 32-byte string)* | Session signing key — **set via env var in production** |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///database.db` | Database path |
| `REMEMBER_COOKIE_DURATION` | 1 hour | Lifetime of remember-me cookie |
| `PERMANENT_SESSION_LIFETIME` | 1 hour | Lifetime of permanent sessions |

```bash
export SECRET_KEY="your-random-secret-here"
python run.py
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.10+ | Backend runtime |
| Framework | Flask | HTTP routing, request handling |
| ORM | Flask-SQLAlchemy | Database models and queries |
| Auth | Flask-Login | Session management, `@login_required` |
| Security | Werkzeug | Password hashing |
| Database | SQLite | Persistent storage, zero-config |
| CORS | Flask-CORS | Cross-origin request support |
| Frontend | Vanilla JS + CSS | Pre-built SPA from Neerajvs32/Test1, not modified |

---

## 📁 Frontend Credit

The `frontend/` directory was cloned from **[Neerajvs32/Test1](https://github.com/Neerajvs32/Test1)** and is the original work of that repository's author. Zero modifications were made to `admin.html`, `admin.css`, or `admin.js`.

The frontend connects to the backend via these fetch calls:

```
/auth/signup              POST
/auth/login               POST
/auth/logout              POST
/auth/status              GET    ← called on DOMContentLoaded to restore session
/api/opportunities/       GET, POST
/api/opportunities/<id>   GET, PUT, DELETE
```

All DOM updates (card append, update, remove) happen client-side — no page refresh required.

---

## 👤 Author

**Darshan Gowda** · [github.com/darshan-gowdaa](https://github.com/darshan-gowdaa)

Built as part of the **CertifyMe Full Stack Intern Assessment** — Day 1 (Auth) + Day 2 (Opportunity Management).

---
