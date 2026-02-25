from app import app
from models import User

with app.app_context():
    # Simular exactamente lo que hace el formulario de login
    email_input = 'test@test.com'
    password_input = 'test123'
    
    # Procesar como lo hace auth/routes.py línea 72
    email = email_input.strip().lower()
    password = password_input
    
    print(f'🔍 Simulando login...')
    print(f'   Email procesado: "{email}"')
    print(f'   Password: "{password}"')
    print()
    
    # Buscar usuario
    user = User.query.filter_by(email=email).first()
    
    if not user:
        print('❌ Usuario NO encontrado')
    else:
        print('✅ Usuario encontrado')
        print(f'   Email en DB: "{user.email}"')
        print(f'   Nombre: {user.name}')
        print(f'   Habilitado: {user.is_enabled}')
        
        # Verificar contraseña
        password_ok = user.check_password(password)
        print(f'   check_password(): {password_ok}')
        
        if not user.is_enabled:
            print('\n❌ PROBLEMA: Usuario deshabilitado')
        elif not password_ok:
            print('\n❌ PROBLEMA: Contraseña incorrecta')
        else:
            print('\n✅ LOGIN DEBERÍA FUNCIONAR')
