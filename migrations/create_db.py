# create_db.py
from app import create_app
from app.extensions import db
from app.models import User   # importa los modelos para que SQLAlchemy los detecte

app = create_app()

with app.app_context():
    db.create_all()
    print(">>> Tablas creadas correctamente.")