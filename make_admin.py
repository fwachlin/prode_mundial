from app import app
from extensions import db
from models import User

def make_admin(email):
    """Hacer admin a un usuario por email"""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ Usuario con email '{email}' no encontrado")
            return
        
        if user.is_admin:
            print(f"⚠️ El usuario '{email}' ya es admin")
            return
        
        user.is_admin = True
        db.session.commit()
        print(f"✅ {user.name} ({email}) ahora es ADMIN")

if __name__ == '__main__':
    # Cambia esto por tu email
    make_admin('admin@prode.com')