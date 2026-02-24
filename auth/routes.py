from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, AllowedEmail
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registrar nuevo usuario"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validar campos obligatorios
        if not name or not email or not password:
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('auth.register'))
        
        # ← PRIMERO: Validar que el email está permitido
        allowed = AllowedEmail.query.filter_by(email=email).first()
        if not allowed:
            flash(f'El email {email} no está habilitado para registrarse', 'error')
            return redirect(url_for('auth.register'))
        
        # SEGUNDO: Validar que el usuario no exista
        if User.query.filter_by(email=email).first():
            flash('Este email ya está registrado', 'error')
            return redirect(url_for('auth.register'))
        
        # TERCERO: Validar que las contraseñas coincidan
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.register'))
        
        # CUARTO: Validar longitud de contraseña
        if len(password) < 4:
            flash('La contraseña debe tener al menos 4 caracteres', 'error')
            return redirect(url_for('auth.register'))
        
        # Crear usuario
        try:
            user = User(name=name, email=email, is_enabled=True)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Iniciar sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Email o contraseña incorrectos', 'error')
            return redirect(url_for('auth.login'))
        
        if not user.is_enabled:
            flash('Tu cuenta ha sido deshabilitada', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambiar contraseña del usuario actual"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validar que todos los campos estén completos
        if not current_password or not new_password or not confirm_password:
            flash('Todos los campos son requeridos', 'error')
            return redirect(url_for('auth.change_password'))
        
        # Verificar contraseña actual
        if not current_user.check_password(current_password):
            flash('La contraseña actual es incorrecta', 'error')
            return redirect(url_for('auth.change_password'))
        
        # Validar que las nuevas contraseñas coincidan
        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden', 'error')
            return redirect(url_for('auth.change_password'))
        
        # Validar longitud mínima
        if len(new_password) < 4:
            flash('La nueva contraseña debe tener al menos 4 caracteres', 'error')
            return redirect(url_for('auth.change_password'))
        
        # Actualizar contraseña
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Contraseña actualizada exitosamente', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/change_password.html')