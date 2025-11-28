from app import create_app

app = create_app()
print("SQLALCHEMY_DATABASE_URI =", app.config["SQLALCHEMY_DATABASE_URI"])