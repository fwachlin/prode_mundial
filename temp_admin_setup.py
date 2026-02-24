from flask import Blueprint

temp_admin_bp = Blueprint('temp_admin', __name__)

@temp_admin_bp.route('/secret-create-admin-xyz123')
def create_admin():
    """Endpoint temporal para crear admin en producción. Eliminar después de usar."""
    from models import User, db
    
    # Verificar si ya existe
    admin = User.query.filter_by(email='admin@prode.com').first()
    
    if admin:
        # Actualizar contraseña
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.commit()
        return f"✅ Admin actualizado: {admin.email} (is_admin={admin.is_admin})"
    else:
        # Crear nuevo
        admin = User(
            email='admin@prode.com',
            name='Admin'
        )
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        return f"✅ Admin creado: {admin.email} (is_admin={admin.is_admin})"
