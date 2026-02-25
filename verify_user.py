from app import app
from models import User

with app.app_context():
    user = User.query.filter_by(email='test@test.com').first()
    
    if not user:
        print('❌ Usuario NO encontrado')
    else:
        print('✅ Usuario encontrado')
        print(f'   Nombre: {user.name}')
        print(f'   Email: {user.email}')
        print(f'   Habilitado: {user.is_enabled}')
        print(f'   Es admin: {user.is_admin}')
        print(f'   Tiene password_hash: {user.password_hash is not None}')
        
        # Verificar contraseña
        test_pass = user.check_password('test123')
        print(f'   Password "test123" es correcta: {test_pass}')
        
        if not test_pass:
            print('\n🔄 Reestableciendo contraseña...')
            from models import db
            user.set_password('test123')
            db.session.commit()
            print('✅ Contraseña actualizada')
            print('   Verificando nuevamente:', user.check_password('test123'))
