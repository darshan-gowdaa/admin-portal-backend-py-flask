from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id            = db.Column(db.Integer, primary_key=True)
    full_name     = db.Column(db.String(120), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    opportunities = db.relationship(
        'Opportunity', backref='admin', lazy=True, cascade='all, delete-orphan'
    )


class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'

    id         = db.Column(db.Integer, primary_key=True)
    admin_id   = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    token      = db.Column(db.String(256), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used       = db.Column(db.Boolean, default=False)


VALID_CATEGORIES = {'Technology', 'Business', 'Design', 'Marketing', 'Data Science', 'Other'}


class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    id                   = db.Column(db.Integer, primary_key=True)
    admin_id             = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    name                 = db.Column(db.String(200), nullable=False)
    category             = db.Column(db.String(100), nullable=False)
    duration             = db.Column(db.String(100), nullable=False)
    start_date           = db.Column(db.String(50),  nullable=False)
    description          = db.Column(db.Text,        nullable=False)
    skills_to_gain       = db.Column(db.Text,        nullable=False)  # comma-separated
    future_opportunities = db.Column(db.Text,        nullable=False)
    max_applicants       = db.Column(db.Integer,     nullable=True)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)
