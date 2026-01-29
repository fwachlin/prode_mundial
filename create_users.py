from app import app
from extensions import db
from models import User, AllowedEmail

def create_users():
    """Crear múltiples usuarios de prueba con emails habilitados"""
    
    users_data = [
        {"name": "Juan Pérez", "email": "juan@prode.com", "password": "123456", "is_admin": False},
        {"name": "María González", "email": "maria@prode.com", "password": "123456", "is_admin": False},
        {"name": "Carlos Rodríguez", "email": "carlos@prode.com", "password": "123456", "is_admin": False},
        {"name": "Ana Martínez", "email": "ana@prode.com", "password": "123456", "is_admin": False},
        {"name": "Pedro López", "email": "pedro@prode.com", "password": "123456", "is_admin": False},
        {"name": "Laura Fernández", "email": "laura@prode.com", "password": "123456", "is_admin": False},
        {"name": "Admin", "email": "admin@prode.com", "password": "admin123", "is_admin": True},
    ]
    
    with app.app_context():
        created = 0
        skipped = 0
        
        for user_data in users_data:
            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=user_data["email"]).first()
            
            if existing_user:
                print(f"⚠️  Usuario '{user_data['name']}' ({user_data['email']}) ya existe")
                skipped += 1
                continue
            
            # Crear el email en la lista de permitidos
            allowed_email = AllowedEmail.query.filter_by(email=user_data["email"]).first()
            if not allowed_email:
                allowed_email = AllowedEmail(email=user_data["email"])
                db.session.add(allowed_email)
            
            # Crear el usuario
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                is_admin=user_data["is_admin"],
                is_enabled=True
            )
            user.set_password(user_data["password"])
            
            db.session.add(user)
            
            status = "👑 ADMIN" if user_data["is_admin"] else "👤 Usuario"
            print(f"✅ {status} creado: {user_data['name']} ({user_data['email']})")
            created += 1
        
        db.session.commit()
        
        print(f"\n📊 Resumen:")
        print(f"   ✅ Creados: {created}")
        print(f"   ⚠️  Ya existían: {skipped}")
        print(f"\n🔑 Contraseñas:")
        print(f"   • Usuarios normales: 123456")
        print(f"   • Admin: admin123")

if __name__ == '__main__':
    create_users()