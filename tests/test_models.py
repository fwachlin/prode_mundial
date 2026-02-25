"""
Tests del modelo de base de datos
"""
import pytest
from models import User, Match, Prediction, AllowedEmail, Phase
from datetime import datetime, timezone, timedelta


class TestUserModel:
    """Tests del modelo User"""
    
    def test_create_user(self, app):
        """Crear usuario básico"""
        with app.app_context():
            user = User(name='Test', email='test@test.com')
            user.set_password('password123')
            assert user.name == 'Test'
            assert user.email == 'test@test.com'
            assert user.password_hash is not None
    
    def test_password_hashing(self, app):
        """Verificar hash de contraseña"""
        with app.app_context():
            user = User(name='Test', email='test@test.com')
            user.set_password('mypassword')
            
            # Contraseña correcta
            assert user.check_password('mypassword') is True
            
            # Contraseña incorrecta
            assert user.check_password('wrongpassword') is False
    
    def test_user_defaults(self, app):
        """Verificar valores por defecto"""
        with app.app_context():
            from models import db
            user = User(name='Test', email='test@test.com')
            db.session.add(user)
            db.session.commit()
            assert user.is_admin is False
            assert user.is_enabled is True


class TestMatchModel:
    """Tests del modelo Match"""
    
    def test_create_match(self, app):
        """Crear partido básico"""
        with app.app_context():
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Argentina',
                away_team='Brasil',
                kickoff_at=now + timedelta(hours=2),
                closes_at=now + timedelta(hours=1),
                phase_id=1
            )
            assert match.home_team == 'Argentina'
            assert match.away_team == 'Brasil'
            assert match.home_goals is None
            assert match.away_goals is None
    
    def test_is_open_true(self, app, open_match):
        """Pronóstico abierto devuelve True"""
        with app.app_context():
            match = Match.query.get(open_match)
            assert match.is_open() is True
    
    def test_is_open_false(self, app, closed_match):
        """Pronóstico cerrado devuelve False"""
        with app.app_context():
            match = Match.query.get(closed_match)
            assert match.is_open() is False


class TestPredictionModel:
    """Tests del modelo Prediction"""
    
    def test_create_prediction(self, app, regular_user, open_match):
        """Crear pronóstico básico"""
        with app.app_context():
            from models import db
            pred = Prediction(
                user_id=regular_user,
                match_id=open_match,
                home_goals=3,
                away_goals=1
            )
            db.session.add(pred)
            db.session.commit()
            
            assert pred.home_goals == 3
            assert pred.away_goals == 1
            assert pred.points_awarded is None


class TestAllowedEmailModel:
    """Tests del modelo AllowedEmail"""
    
    def test_create_allowed_email(self, app):
        """Crear email permitido"""
        with app.app_context():
            from models import db
            allowed = AllowedEmail(email='user@example.com')
            db.session.add(allowed)
            db.session.commit()
            
            assert allowed.email == 'user@example.com'


class TestPhaseModel:
    """Tests del modelo Phase"""
    
    def test_phases_exist(self, app):
        """Verificar que las 4 fases existen"""
        with app.app_context():
            phases = Phase.query.order_by(Phase.order).all()
            assert len(phases) == 4
            assert phases[0].name == 'Fecha 1'
            assert phases[3].name == 'Fecha 4'
