import os
from datetime import timedelta

from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_cors import CORS

from .models import db, Admin
from .routes.auth import auth_bp
from .routes.opportunities import opp_bp

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')


def create_app():
    app = Flask(__name__, static_folder=FRONTEND_DIR, template_folder=FRONTEND_DIR)

    app.config['SECRET_KEY']                  = os.environ.get('SECRET_KEY', 'change-me-in-production-abc123xyz')
    app.config['SQLALCHEMY_DATABASE_URI']     = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REMEMBER_COOKIE_DURATION']    = timedelta(hours=1)
    app.config['REMEMBER_COOKIE_HTTPONLY']    = True
    app.config['REMEMBER_COOKIE_SAMESITE']    = 'Lax'
    app.config['SESSION_COOKIE_SAMESITE']     = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME']  = timedelta(hours=1)

    CORS(app, supports_credentials=True)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import jsonify
        return jsonify({'error': 'Authentication required.'}), 401

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(opp_bp, url_prefix='/api/opportunities')

    # Serve frontend
    @app.route('/')
    def index():
        return send_from_directory(FRONTEND_DIR, 'admin.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory(FRONTEND_DIR, filename)

    with app.app_context():
        db.create_all()

    return app
