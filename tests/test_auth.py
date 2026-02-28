"""
Tests de autenticación
"""
import pytest
from models import db, User, AllowedEmail


class TestRegistration:
    """Tests de registro de usuarios"""
    
    def test_register_success(self, client, allowed_email):
        """Registro exitoso con email permitido"""
        response = client.post('/auth/register', data={
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=False)
        
        assert response.status_code == 302  # Redirect
        
        # Verificar que el usuario fue creado con el nombre del AllowedEmail
        with client.application.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user is not None
            assert user.name == 'Test User'  # Nombre asignado por admin en AllowedEmail
            assert user.is_admin is False
    
    def test_register_email_not_allowed(self, client):
        """Registro falla si email no está permitido"""
        response = client.post('/auth/register', data={
            'email': 'notallowed@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        
        assert b'no est' in response.data  # "no está habilitado"
        
        # Verificar que NO se creó el usuario
        with client.application.app_context():
            user = User.query.filter_by(email='notallowed@example.com').first()
            assert user is None
    
    def test_register_password_mismatch(self, client, allowed_email):
        """Registro falla si contraseñas no coinciden"""
        response = client.post('/auth/register', data={
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'different456'
        }, follow_redirects=True)
        
        assert b'no coinciden' in response.data
        
        # Verificar que NO se creó el usuario
        with client.application.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            assert user is None
    
    def test_register_password_too_short(self, client, allowed_email):
        """Registro falla si contraseña es muy corta"""
        response = client.post('/auth/register', data={
            'email': 'test@example.com',
            'password': '123',  # Menos de 4 caracteres
            'password_confirm': '123'
        }, follow_redirects=True)
        
        assert b'al menos 4 caracteres' in response.data
    
    def test_register_duplicate_email(self, client, regular_user, allowed_email):
        """Registro falla si email ya existe"""
        response = client.post('/auth/register', data={
            'email': 'test@example.com',  # Email ya registrado
            'password': 'password123',
            'password_confirm': 'password123'
        }, follow_redirects=True)
        
        assert b'ya est' in response.data  # "ya está registrado"


class TestLogin:
    """Tests de inicio de sesión"""
    
    def test_login_success(self, client, regular_user):
        """Login exitoso con credenciales correctas"""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test1234'
        }, follow_redirects=False)
        
        assert response.status_code == 302  # Redirect
    
    def test_login_wrong_password(self, client, regular_user):
        """Login falla con contraseña incorrecta"""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'incorrectos' in response.data
    
    def test_login_nonexistent_user(self, client):
        """Login falla con usuario inexistente"""
        response = client.post('/auth/login', data={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert b'incorrectos' in response.data
    
    def test_login_disabled_user(self, client, app):
        """Login falla si usuario está deshabilitado"""
        with app.app_context():
            # Crear usuario deshabilitado
            allowed = AllowedEmail(email='disabled@example.com', name='Disabled User')
            db.session.add(allowed)
            
            user = User(
                name='Disabled User',
                email='disabled@example.com',
                is_enabled=False
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/auth/login', data={
            'email': 'disabled@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert b'deshabilitada' in response.data


class TestLogout:
    """Tests de cierre de sesión"""
    
    def test_logout(self, client, regular_user):
        """Logout exitoso"""
        # Primero login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test1234'
        })
        
        # Luego logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200


class TestChangePassword:
    """Tests de cambio de contraseña"""
    
    def test_change_password_success(self, client, regular_user):
        """Cambio de contraseña exitoso"""
        # Login primero
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test1234'
        })
        
        # Cambiar contraseña
        response = client.post('/auth/change-password', data={
            'current_password': 'test1234',
            'new_password': 'newpassword123',
            'new_password_confirm': 'newpassword123'
        }, follow_redirects=True)
        
        assert b'cambiada' in response.data or response.status_code == 200
        
        # Verificar que la nueva contraseña funciona
        client.get('/auth/logout')
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'newpassword123'
        }, follow_redirects=False)
        
        assert response.status_code == 302  # Redirect = success
