from app import app
from models import User, db
from werkzeug.security import generate_password_hash

with app.app_context():
    # Buscar si ya existe
    admin = User.query.filter_by(email='admin@prode.com').first()
    
    if admin:
        # Actualizar contraseña
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.commit()
        print("✅ Contraseña de admin@prode.com actualizada a 'admin123'")
    else:
        # Crear nuevo usuario admin
        admin = User(
            email='admin@prode.com',
            name='Admin'
        )
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin@prode.com creado con contraseña 'admin123'")
    
    print(f"   Email: admin@prode.com")
    print(f"   Name: {admin.name}")
    print(f"   Is Admin: {admin.is_admin}")
