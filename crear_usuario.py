from app import app
from extensions import db
from models import User

EMAIL = "fwachlin@gmail.com"
PASSWORD = "1234"
NAME = "Felipe"

with app.app_context():
    if User.query.filter_by(email=EMAIL).first():
        print("El usuario ya existe")
        exit()

    u = User(email=EMAIL, name=NAME)
    u.set_password(PASSWORD)

    db.session.add(u)
    db.session.commit()

    print("Usuario creado correctamente")