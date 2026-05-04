import re
import secrets
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import db, Admin, PasswordResetToken

auth_bp = Blueprint('auth', __name__)

EMAIL_RE = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')


def _valid_email(email):
    return bool(EMAIL_RE.match(email))


# --- Signup ---
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True) or request.form

    full_name        = (data.get('full_name') or '').strip()
    email            = (data.get('email') or '').strip().lower()
    password         = data.get('password') or ''
    confirm_password = data.get('confirm_password') or ''

    if not full_name:
        return jsonify({'error': 'Full name is required.'}), 400
    if not email or not _valid_email(email):
        return jsonify({'error': 'A valid email address is required.'}), 400
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters.'}), 400
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400

    if Admin.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email already exists.'}), 409

    admin = Admin(
        full_name=full_name,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(admin)
    db.session.commit()

    return jsonify({'message': 'Account created successfully.'}), 201


# --- Login ---
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or request.form

    email       = (data.get('email') or '').strip().lower()
    password    = data.get('password') or ''
    remember_me = bool(data.get('remember_me'))

    admin = Admin.query.filter_by(email=email).first()
    if not admin or not check_password_hash(admin.password_hash, password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    login_user(admin, remember=remember_me)
    return jsonify({
        'message': 'Login successful.',
        'admin': {'id': admin.id, 'full_name': admin.full_name, 'email': admin.email},
    }), 200


# --- Logout ---
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Signed out successfully.'}), 200


# --- Forgot password ---
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data  = request.get_json(silent=True) or request.form
    email = (data.get('email') or '').strip().lower()

    # always same response — never reveal existence
    msg = 'If this email is registered, a reset link has been sent.'

    admin = Admin.query.filter_by(email=email).first()
    if admin:
        token_str  = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        token = PasswordResetToken(
            admin_id=admin.id,
            token=token_str,
            expires_at=expires_at,
        )
        db.session.add(token)
        db.session.commit()

        reset_link = f'http://localhost:5000/auth/reset-password/{token_str}'
        print(f'[RESET LINK] {reset_link}')  # logged to console only

    return jsonify({'message': msg}), 200


# --- Reset password (GET = validate, POST = submit) ---
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    record = PasswordResetToken.query.filter_by(token=token).first()

    if not record or record.used:
        return jsonify({'error': 'This reset link is invalid.'}), 400
    if record.expires_at < datetime.utcnow():
        return jsonify({'error': 'This reset link has expired.'}), 400

    if request.method == 'GET':
        return jsonify({'message': 'Token is valid. Submit your new password via POST.'}), 200

    # POST — set new password
    data     = request.get_json(silent=True) or request.form
    password = data.get('password') or ''

    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters.'}), 400

    admin = Admin.query.get(record.admin_id)
    admin.password_hash = generate_password_hash(password)
    record.used = True
    db.session.commit()

    return jsonify({'message': 'Password reset successfully.'}), 200


# --- Status ---
@auth_bp.route('/status', methods=['GET'])
def status():
    if current_user.is_authenticated:
        return jsonify({
            'logged_in': True,
            'admin': {'id': current_user.id, 'full_name': current_user.full_name, 'email': current_user.email}
        }), 200
    return jsonify({'logged_in': False}), 200
