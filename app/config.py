# app/config.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def build_default_postgres_url():
    """
    URL por defecto para desarrollo con PostgreSQL.
    AJUSTA usuario, password, host, puerto y nombre de BD.
    """
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ.get("DB_NAME", "app_riesgos")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-super-secreta")

    # 🔹 Prioridad:
    # 1) DATABASE_URL (si la defines)
    # 2) Postgres con datos por defecto
    # 3) SQLite de emergencia
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or build_default_postgres_url()
        or f"sqlite:///{BASE_DIR / 'riesgos.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False