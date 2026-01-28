from app import app, db
from models import AllowedEmail

def add_allowed_emails():
    """Agregar emails permitidos"""
    with app.app_context():
        # Verificar si ya existe
        if AllowedEmail.query.filter_by(email='admin@prode.com').first():
            print("admin@prode.com ya está en la lista")
            return
        
        allowed = AllowedEmail(email='admin@prode.com')
        db.session.add(allowed)
        db.session.commit()
        
        print("✅ admin@prode.com agregado a emails permitidos")

if __name__ == '__main__':
    add_allowed_emails()

print("Ejecutar: python 2_crear_admin_nuevamente.py")