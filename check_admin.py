from app import app
from models import User

with app.app_context():
    admin = User.query.filter_by(email='admin@prode.com').first()
    if admin:
        print(f"✅ Admin encontrado: {admin.name}")
        print(f"   is_admin: {admin.is_admin}")
        print(f"   is_enabled: {admin.is_enabled}")
    else:
        print("❌ Admin NO encontrado")