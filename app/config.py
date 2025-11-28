import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def build_default_postgres_url():
    """
    URL por defecto para desarrollo con PostgreSQL.
    """
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ.get("DB_NAME", "app_riesgos")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-super-secreta")

    # 1. Capturamos la variable de entorno cruda
    database_url = os.environ.get("DATABASE_URL")

    # 2. 🔥 EL FIX PARA RENDER AQUÍ 🔥
    # Render entrega "postgres://", pero SQLAlchemy requiere "postgresql://"
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # 3. Asignamos la URL ya corregida (o usamos los fallbacks)
    SQLALCHEMY_DATABASE_URI = (
        database_url
        or build_default_postgres_url()
        or f"sqlite:///{BASE_DIR / 'riesgos.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False