# app/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager
from app.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


# -------- user_loader para Flask-Login --------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------- LOGIN --------
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Credenciales incorrectas.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


# -------- REGISTRO BÁSICO (opcional) --------
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Correo y contraseña son obligatorios.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado.", "warning")
            return redirect(url_for("auth.register"))

        user = User(
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# -------- LOGOUT --------
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))