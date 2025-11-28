# create_admin.py
from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():
    # Cambia el correo y contraseña si deseas
    email = "admin@admin.com"
    password = "admin123"

    # Evitar duplicados
    user = User.query.filter_by(email=email).first()
    if user:
        print(">>> El usuario administrador ya existe.")
    else:
        user = User(email=email, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(">>> Usuario administrador creado:")
        print(f"Email: {email}")
        print(f"Password: {password}")