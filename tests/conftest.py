"""
Configuración de fixtures para pytest
"""
import pytest
from datetime import datetime, timezone, timedelta
from app import app as flask_app
from models import db, User, Match, Prediction, AllowedEmail, Phase


@pytest.fixture
def app():
    """Fixture de aplicación Flask para testing"""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Base de datos en memoria
        'WTF_CSRF_ENABLED': False,  # Deshabilitar CSRF en tests
        'SECRET_KEY': 'test-secret-key'
    })
    
    with flask_app.app_context():
        db.create_all()
        # Crear fases por defecto
        _create_default_phases()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de test de Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner para tests"""
    return app.test_cli_runner()


def _create_default_phases():
    """Crea las 4 fases por defecto si no existen"""
    # Verificar si ya existen fases
    existing_phases = Phase.query.count()
    if existing_phases == 0:
        phases = [
            Phase(name='Fecha 1', order=1),
            Phase(name='Fecha 2', order=2),
            Phase(name='Fecha 3', order=3),
            Phase(name='Fecha 4', order=4)
        ]
        for phase in phases:
            db.session.add(phase)
        db.session.commit()


@pytest.fixture
def allowed_email(app):
    """Email permitido para registro"""
    with app.app_context():
        email = AllowedEmail(email='test@example.com')
        db.session.add(email)
        db.session.commit()
        email_id = email.id
    return email_id


@pytest.fixture
def regular_user(app, allowed_email):
    """Usuario regular (no admin)"""
    with app.app_context():
        user = User(
            name='Test User',
            email='test@example.com',
            is_admin=False,
            is_enabled=True
        )
        user.set_password('test1234')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    return user_id


@pytest.fixture
def admin_user(app):
    """Usuario administrador"""
    with app.app_context():
        # Admin no necesita email permitido
        admin = User(
            name='Admin User',
            email='admin@example.com',
            is_admin=True,
            is_enabled=True
        )
        admin.set_password('admin1234')
        db.session.add(admin)
        db.session.commit()
        admin_id = admin.id
    return admin_id


@pytest.fixture
def open_match(app):
    """Partido con pronósticos abiertos"""
    with app.app_context():
        now = datetime.now(timezone.utc)
        match = Match(
            home_team='Argentina',
            away_team='Brasil',
            kickoff_at=now + timedelta(hours=2),
            closes_at=now + timedelta(hours=1),  # Cierra en 1 hora
            phase_id=1
        )
        db.session.add(match)
        db.session.commit()
        match_id = match.id
    return match_id


@pytest.fixture
def closed_match(app):
    """Partido con pronósticos cerrados"""
    with app.app_context():
        now = datetime.now(timezone.utc)
        match = Match(
            home_team='Chile',
            away_team='Uruguay',
            kickoff_at=now + timedelta(hours=1),
            closes_at=now - timedelta(hours=1),  # Cerró hace 1 hora
            phase_id=1
        )
        db.session.add(match)
        db.session.commit()
        match_id = match.id
    return match_id


@pytest.fixture
def finished_match(app):
    """Partido con resultado cargado"""
    with app.app_context():
        now = datetime.now(timezone.utc)
        match = Match(
            home_team='México',
            away_team='Canadá',
            kickoff_at=now - timedelta(hours=2),
            closes_at=now - timedelta(hours=3),
            phase_id=1,
            home_goals=2,
            away_goals=1
        )
        db.session.add(match)
        db.session.commit()
        match_id = match.id
    return match_id


@pytest.fixture
def prediction(app, regular_user, open_match):
    """Pronóstico de usuario regular"""
    with app.app_context():
        pred = Prediction(
            user_id=regular_user,
            match_id=open_match,
            home_goals=2,
            away_goals=1
        )
        db.session.add(pred)
        db.session.commit()
        pred_id = pred.id
    return pred_id
