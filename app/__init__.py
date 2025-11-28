# app/__init__.py
from flask import Flask
from app.extensions import db, migrate, login_manager

def create_app(config_class=None):
    app = Flask(__name__)

    # Config (usa DevConfig por defecto)
    app.config.from_object(config_class or "app.config.DevConfig")

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import models  # importa los modelos

    # Blueprints
    from app.auth.routes import bp as auth_bp
    from app.dashboard.routes import bp as dashboard_bp
    from app.company.routes import bp as company_bp
    from app.risk_model.routes import bp as risk_model_bp
    from app.inference.routes import bp as inference_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(risk_model_bp)
    app.register_blueprint(inference_bp)

    return app