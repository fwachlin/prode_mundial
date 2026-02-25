"""
Script para ejecutar en la shell de Render:
python create_admin_render.py
"""
import os
from app import app
from models import User, db

print("=" * 60)
print("CREANDO USUARIO ADMIN EN PRODUCCIÓN")
print("=" * 60)

with app.app_context():
    # Verificar conexión a base de datos
    try:
        db.session.execute(db.text('SELECT 1'))
        print("✅ Conexión a base de datos OK")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        exit(1)
    
    # Buscar o crear admin
    admin = User.query.filter_by(email='admin@prode.com').first()
    
    if admin:
        print(f"ℹ️  Usuario admin@prode.com ya existe (ID: {admin.id})")
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.commit()
        print("✅ Contraseña actualizada a 'admin123'")
        print(f"✅ Privilegios admin: {admin.is_admin}")
    else:
        admin = User(
            email='admin@prode.com',
            name='Admin'
        )
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado exitosamente")
        print(f"   ID: {admin.id}")
        print(f"   Email: {admin.email}")
        print(f"   Name: {admin.name}")
        print(f"   Is Admin: {admin.is_admin}")
    
    print("\n" + "=" * 60)
    print("CREDENCIALES:")
    print("Email: admin@prode.com")
    print("Password: admin123")
    print("=" * 60)
