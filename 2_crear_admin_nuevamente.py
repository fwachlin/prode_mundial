from app import app, db
from models import User
with app.app_context():
    admin = User(name='Admin', email='admin@prode.com', is_admin=True, is_enabled=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin creado")