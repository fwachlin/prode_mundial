from app import app
from models import db, User, AllowedEmail

with app.app_context():
    # Agregar email permitido
    ae = AllowedEmail(email='test@test.com')
    db.session.merge(ae)
    
    # Verificar si ya existe
    user = User.query.filter_by(email='test@test.com').first()
    
    if not user:
        user = User(
            name='Usuario Test',
            email='test@test.com',
            is_admin=False,
            is_enabled=True
        )
        user.set_password('test123')
        db.session.add(user)
        db.session.commit()
        print('✅ Usuario creado')
    else:
        # Actualizar contraseña del existente
        user.set_password('test123')
        db.session.commit()
        print('✅ Contraseña actualizada para usuario existente')
    
    print('\n📧 Email: test@test.com')
    print('🔑 Password: test123')
    print('👤 Tipo: Usuario regular (NO admin)')
