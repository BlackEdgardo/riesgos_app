# app/models.py
from app.extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ========= MÉTODOS IMPORTANTES =========
    def set_password(self, password):
        """Genera el hash seguro de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña contra el hash"""
        return check_password_hash(self.password_hash, password)


class Empresa(db.Model):
    __tablename__ = "empresas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ruc = db.Column(db.String(11))
    sector = db.Column(db.String(100))


class ModeloBN(db.Model):
    """
    Representa un modelo bayesiano (estructura + CPTs) guardado como JSON.
    """
    __tablename__ = "modelos_bn"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"))
    estructura_json = db.Column(db.JSON, nullable=False)  # nodos + edges
    cpts_json = db.Column(db.JSON, nullable=False)        # tablas CPT
    creado_por = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Evidencia(db.Model):
    __tablename__ = "evidencias"
    id = db.Column(db.Integer, primary_key=True)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelos_bn.id"))
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    evidencia_json = db.Column(db.JSON, nullable=False)  # {"CorteElectrico": "SI", ...}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ResultadoInferencia(db.Model):
    __tablename__ = "resultados_inferencia"
    id = db.Column(db.Integer, primary_key=True)
    modelo_id = db.Column(db.Integer, db.ForeignKey("modelos_bn.id"))
    evidencia_id = db.Column(db.Integer, db.ForeignKey("evidencias.id"))
    resultado_json = db.Column(db.JSON, nullable=False)  # {"RiesgoDisponibilidad": {"bajo":0.1,...}}
    riesgo_clasificado = db.Column(db.String(20))        # bajo/medio/alto
    created_at = db.Column(db.DateTime, default=datetime.utcnow)