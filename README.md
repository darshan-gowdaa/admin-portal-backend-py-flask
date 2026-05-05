<div align="center">

<img src="https://iconape.com/wp-content/files/hz/20759/png/Qatar-Foundation-01.png" width="100" alt="Qatar Foundation Logo"/>

# Qatar Foundation — Admin Portal
### Universal Skills Passport · مؤسسة قطر

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-22c55e?style=for-the-badge)]()

*A full-stack admin portal for managing opportunities, learners, verifiers, and collaborators — built on Flask + SQLite with a pre-designed modern UI.*

[Features](#-features) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Architecture](#-architecture) · [Tests](#-running-tests)

---

</div>

## 📸 Overview

The Qatar Foundation Admin Portal is a single-page application (SPA) that provides institutional administrators a secure, role-isolated dashboard to:

- **Authenticate** via signup / login / forgot-password flows with CAPTCHA
- **Manage opportunities** — create, view, edit, delete with full persistence
- **View learner, verifier, and collaborator data** across the platform
- **Analyze** platform usage via charts and statistics
- **Isolate data** between admin accounts so no cross-contamination occurs

The frontend is a pre-built, pixel-perfect Admin UI. This project delivers the entire Python/Flask backend that powers it.

---

## ✨ Features

### 🔐 Authentication
| Feature | Detail |
|---|---|
| Signup | Full name, email, password validation + duplicate detection |
| Login | Bcrypt password verification, generic error messages, session management |
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
- **Learner Management** — student table with status filters and date range, course management grid, bulk upload + quick-add modals
- **Verifier Management** — verifier table with stats, subject breakdown, student progress view
- **Collaborator Management** — submitted course approval/rejection workflow
- **Reports & Analytics** — engagement trend charts, completion rates, verification status tables, level distribution

---

## 🏗 Architecture

```
qatar-foundation-admin/
│
├── app/
│   ├── __init__.py          # Flask app factory, CORS, LoginManager, blueprints
│   ├── models.py            # SQLAlchemy models: Admin, PasswordResetToken, Opportunity
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # /auth/* — signup, login, logout, forgot/reset password, status
│       └── opportunities.py # /api/opportunities/* — full CRUD, ownership enforcement
│
├── frontend/
│   ├── admin.html           # Single-page application shell (DO NOT MODIFY)
│   ├── admin.css            # UI styles with CSS variables + dark mode (DO NOT MODIFY)
│   └── admin.js             # SPA logic, API calls, DOM management (DO NOT MODIFY)
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

### 1. Clone
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

The app starts at **http://localhost:5000**

> On first boot, `database.db` is auto-created with all tables via `db.create_all()`. No migrations needed.

---

## 🔌 API Reference

All endpoints return JSON. Auth endpoints live under `/auth`, opportunity endpoints under `/api/opportunities`.

### Authentication

#### `POST /auth/signup`
Create a new admin account.

**Request**
```json
{
  "full_name": "Jane Smith",
  "email": "jane@qf.org.qa",
  "password": "Secure123!",
  "confirm_password": "Secure123!"
}
```

**Responses**
| Status | Meaning |
|---|---|
| `201` | Account created |
| `400` | Validation failure (missing field, invalid email, short/mismatched password) |
| `409` | Email already registered |

---

#### `POST /auth/login`
Authenticate an existing admin.

**Request**
```json
{
  "email": "jane@qf.org.qa",
  "password": "Secure123!",
  "remember_me": true
}
```

**Responses**
| Status | Meaning |
|---|---|
| `200` | Login successful — session cookie set |
| `401` | `"Invalid email or password"` (generic — never reveals which field failed) |

---

#### `POST /auth/logout`
End the current session. Requires authentication.

**Responses** — `200 OK`

---

#### `POST /auth/forgot-password`
Request a password reset link.

**Request**
```json
{ "email": "jane@qf.org.qa" }
```

**Responses** — Always `200` with identical message regardless of whether email exists. Reset link is logged to server console only.

---

#### `GET /auth/reset-password/<token>`
Validate a reset token.

| Status | Meaning |
|---|---|
| `200` | Token valid |
| `400` | Token invalid, already used, or expired |

#### `POST /auth/reset-password/<token>`
Submit new password for a valid token.

**Request**
```json
{ "password": "NewPass456!" }
```

| Status | Meaning |
|---|---|
| `200` | Password updated — token marked used |
| `400` | Token invalid / expired / already used, or password too short |

---

#### `GET /auth/status`
Check current session state (used on page load).

```json
{ "logged_in": true, "admin": { "id": 1, "full_name": "Jane Smith", "email": "jane@qf.org.qa" } }
```

---

### Opportunities

> All endpoints require an active session. Admins only access their own data.

#### `GET /api/opportunities/`
Returns all opportunities for the logged-in admin, ordered by `created_at` descending.

```json
[
  {
    "id": 1,
    "admin_id": 3,
    "name": "AI Internship",
    "category": "Technology",
    "duration": "3 months",
    "start_date": "2025-09-01",
    "description": "Work on AI projects",
    "skills_to_gain": "Python,ML,TensorFlow",
    "future_opportunities": "Full-time role",
    "max_applicants": 50,
    "created_at": "2025-05-01T12:00:00"
  }
]
```

---

#### `POST /api/opportunities/`
Create a new opportunity linked to the logged-in admin.

**Required fields:** `name`, `category`, `duration`, `start_date`, `description`, `skills_to_gain`, `future_opportunities`

**Optional fields:** `max_applicants` (positive integer)

**Valid categories:** `Technology`, `Business`, `Design`, `Marketing`, `Data Science`, `Other`

| Status | Meaning |
|---|---|
| `201` | Opportunity created — returns full object |
| `400` | Validation failure |
| `401` | Not authenticated |

---

#### `GET /api/opportunities/<id>`
Fetch a single opportunity by ID.

| Status | Meaning |
|---|---|
| `200` | Returns opportunity object |
| `403` | Opportunity belongs to another admin |
| `404` | Not found |

---

#### `PUT /api/opportunities/<id>`
Update an existing opportunity. Same validation rules as POST.

| Status | Meaning |
|---|---|
| `200` | Updated — returns full object |
| `400` | Validation failure |
| `403` | Not owner |
| `404` | Not found |

---

#### `DELETE /api/opportunities/<id>`
Permanently delete an opportunity.

| Status | Meaning |
|---|---|
| `200` | Deleted |
| `403` | Not owner |
| `404` | Not found |

---

## 🧪 Running Tests

The test suite (`test_all.py`) uses only Python stdlib — no pytest or extra packages required.

```bash
# Start the server first
python run.py &

# Then run tests
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
| Cross-admin isolation | Admin B cannot read/edit/delete Admin A's opportunities, list is empty |
| Password reset | Full flow: trigger → read token from DB → validate → set new password → reuse blocked → login with new/old password |
| Logout | Post-logout GET and POST blocked with 401 |
| Static files | `/`, `/admin.css`, `/admin.js` all return 200 |

Expected output:
```
=== FINAL RESULTS: 42 passed, 0 failed ===
ALL TESTS PASSED
```

---

## 🔒 Security

- Passwords hashed with **Werkzeug's PBKDF2-SHA256** (`generate_password_hash`)
- Login errors are **generic** — never reveals whether email or password was wrong
- Password reset tokens are **cryptographically random** (`secrets.token_urlsafe(32)`)
- Reset tokens **expire after 1 hour** and are **single-use** (marked `used=True` on consumption)
- Forgot-password always returns **identical response** regardless of email existence
- All opportunity routes enforce **ownership** — 403 on cross-admin access attempts
- `HttpOnly` remember-me cookies, `SameSite=Lax` on both session and remember cookies
- User input sanitized in frontend via `escapeHtml()` before DOM injection

---

## ⚙️ Configuration

All config lives in `app/__init__.py` via the `create_app()` factory.

| Key | Default | Description |
|---|---|---|
| `SECRET_KEY` | `change-me-in-production-abc123xyz` | Session signing key — **override via env var in production** |
| `SQLALCHEMY_DATABASE_URI` | `sqlite:///database.db` | Database path |
| `REMEMBER_COOKIE_DURATION` | 1 hour | Lifetime of remember-me cookie |
| `PERMANENT_SESSION_LIFETIME` | 1 hour | Lifetime of permanent sessions |

Set `SECRET_KEY` in production:
```bash
export SECRET_KEY="your-random-secret-key-here"
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
| Database | SQLite | Persistent storage (zero-config) |
| CORS | Flask-CORS | Cross-origin request support |
| Frontend | Vanilla JS + CSS | Pre-built SPA — not modified |

---

## 📁 Frontend Notes

> ⚠️ The `frontend/` directory is **read-only**. No changes were made to `admin.html`, `admin.css`, or `admin.js`.

The frontend communicates with the backend exclusively via:
- `fetch('/auth/signup')` · `fetch('/auth/login')` · `fetch('/auth/logout')`
- `fetch('/auth/status')` — called on DOMContentLoaded to restore session
- `fetch('/api/opportunities/')` — CRUD calls with JSON payloads

All DOM updates (card append, update, remove) happen client-side without page refresh.

---

## 👤 Author

Built as part of the **CertifyMe Full Stack Intern Assessment**.

- Original UI Repository: [github.com/Neerajvs32/Test1](https://github.com/Neerajvs32/Test1)
- Backend authored from scratch — Flask, SQLAlchemy, Flask-Login, Flask-CORS

---
