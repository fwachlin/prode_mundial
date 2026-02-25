from app import app
from models import db, User, AllowedEmail

with app.app_context():
    email = 'test@test.com'
    password = 'test123'
    
    print(f'🔍 Verificando login para: {email}\n')
    
    # 1. Verificar AllowedEmail
    allowed = AllowedEmail.query.filter_by(email=email).first()
    print(f'1. Email en AllowedEmail: {allowed is not None}')
    
    if not allowed:
        print('   ⚠️ Email NO está en lista de permitidos - AGREGANDO...')
        allowed = AllowedEmail(email=email)
        db.session.add(allowed)
        db.session.commit()
        print('   ✅ Email agregado a AllowedEmail')
    
    # 2. Verificar User
    user = User.query.filter_by(email=email).first()
    print(f'2. Usuario existe: {user is not None}')
    
    if user:
        print(f'   - Nombre: {user.name}')
        print(f'   - Habilitado: {user.is_enabled}')
        print(f'   - Es admin: {user.is_admin}')
        
        # 3. Verificar contraseña
        password_ok = user.check_password(password)
        print(f'3. Contraseña correcta: {password_ok}')
        
        if not password_ok:
            print('   ⚠️ Contraseña incorrecta - ACTUALIZANDO...')
            user.set_password(password)
            db.session.commit()
            print('   ✅ Contraseña actualizada')
    
    print('\n✅ Ahora deberías poder iniciar sesión con:')
    print(f'   Email: {email}')
    print(f'   Password: {password}')
