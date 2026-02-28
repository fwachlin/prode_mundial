"""
Configuración de fixtures para pytest
"""
import pytest
from datetime import datetime, timezone, timedelta
from flask import Flask
from models import db, User, Match, Prediction, AllowedEmail, Phase
from flask_login import LoginManager


@pytest.fixture
def app():
    """
    Fixture de aplicación Flask para testing - COMPLETAMENTE AISLADA de la app real
    
    GARANTÍAS DE SEGURIDAD:
    1. NO importa 'app' de app.py - crea una app NUEVA
    2. Base de datos en MEMORIA (sqlite:///:memory:) - NUNCA toca archivos
    3. Cada test crea y destruye su propia DB en memoria
    4. IMPOSIBLE que afecte instance/prode.db
    """
    import os
    from flask_login import current_user
    
    # Crear una app NUEVA para tests, NO usar la app de desarrollo
    # Configurar para que busque templates desde la raíz del proyecto
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    test_app = Flask(__name__, template_folder=template_dir)
    
    test_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # ⚠️ MEMORIA - NUNCA archivo
        'WTF_CSRF_ENABLED': False,  # Deshabilitar CSRF en tests
        'SECRET_KEY': 'test-secret-key',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    # ✅ VERIFICACIÓN DE SEGURIDAD: Confirmar que NO usa DB real
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:', \
        "❌ PELIGRO: Tests NO deben usar base de datos de archivo"
    assert test_app.config['TESTING'] is True, \
        "❌ PELIGRO: Tests deben tener TESTING=True"
    
    # Inicializar extensiones con la app de test
    db.init_app(test_app)
    login_manager = LoginManager()
    login_manager.init_app(test_app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Hacer current_user disponible en templates
    @test_app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    # Registrar filtros de template (copiadosde app.py)
    @test_app.template_filter('fifa_code')
    def fifa_code_filter(country_name):
        """Convierte nombre de país a código FIFA de 3 letras"""
        if not country_name:
            return ''
        if len(country_name) <= 4 and country_name.isupper():
            return country_name
        if 'Path' in country_name or 'IC' in country_name:
            return country_name
        if any(country_name.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                                      '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                                      '3A', '3B', '3C', '3D', '3E', '3F']):
            return country_name
        if (country_name.startswith('W') or country_name.startswith('L')) and len(country_name) >= 2:
            if country_name[1].isdigit():
                return country_name
        return country_name[:3].upper()
    
    @test_app.template_filter('country_iso2')
    def country_iso2_filter(country_name):
        """Convierte nombre de país a código ISO2 para banderas"""
        if not country_name:
            return 'xx'
        if 'Path' in country_name or country_name.startswith('IC '):
            return 'xx'
        if any(country_name.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                                      '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                                      '3A', '3B', '3C', '3D', '3E', '3F']):
            return 'xx'
        if (country_name.startswith('W') or country_name.startswith('L')) and len(country_name) >= 2:
            if country_name[1].isdigit():
                return 'xx'
        return 'xx'  # Simplificado para tests
    
    # Registrar blueprints (sin url_prefix porque ya los tienen definidos)
    from auth.routes import auth_bp
    from main.routes import main_bp
    from admin.routes import admin_bp
    
    test_app.register_blueprint(auth_bp)
    test_app.register_blueprint(main_bp)
    test_app.register_blueprint(admin_bp)
    
    with test_app.app_context():
        db.create_all()
        # Crear fases por defecto
        _create_default_phases()
        yield test_app
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
        email = AllowedEmail(email='test@example.com', name='Test User')
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
