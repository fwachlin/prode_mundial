from flask import Flask
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
from models import db, User, Match
from datetime import datetime, timezone, timedelta
from fifa_countries import get_fifa_code, get_country_iso2, get_country_name
import os

app = Flask(__name__)

# Configuración de base de datos
# En producción (Render), usar PostgreSQL
# En desarrollo local, usar SQLite
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Render provee DATABASE_URL con postgres://, pero SQLAlchemy necesita postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Agregar parámetros SSL para Render PostgreSQL
    if '?' in DATABASE_URL:
        DATABASE_URL += '&sslmode=require'
    else:
        DATABASE_URL += '?sslmode=require'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'sslmode': 'require'
        }
    }
else:
    # Desarrollo local con SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'prode.db')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Google Analytics 4
app.config['GA_MEASUREMENT_ID'] = os.environ.get('GA_MEASUREMENT_ID')

# Deshabilitar caché de templates en desarrollo
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Headers anti-caché para páginas dinámicas (desarrollo y producción)
@app.after_request
def add_no_cache_headers(response):
    # Aplicar headers anti-caché a páginas HTML dinámicas
    # No aplicar a archivos estáticos (CSS, JS, imágenes)
    if response.content_type and 'text/html' in response.content_type:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Inicializar extensiones
db.init_app(app)

# Inicializar protección CSRF
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Hacer current_user disponible en todos los templates
@app.context_processor
def inject_user():
    return {'current_user': current_user}

# Filtro para convertir nombres de países a códigos FIFA
@app.template_filter('fifa_code')
def fifa_code_filter(country_name):
    """Convierte nombre de país a código FIFA de 3 letras usando base de datos completa (211 países)"""
    return get_fifa_code(country_name)

# Filtro para convertir códigos FIFA a ISO 3166-1 alpha-2 (para banderas)
@app.template_filter('country_iso2')
def country_iso2_filter(fifa_code):
    """Convierte código FIFA a código ISO2 para mostrar banderas (soporta 211 países)"""
    return get_country_iso2(fifa_code)

# Filtro para convertir códigos FIFA a nombres completos de países
@app.template_filter('country_name')
def country_name_filter(fifa_code):
    """Convierte código FIFA a nombre completo del país en español (211 países)"""
    return get_country_name(fifa_code)

# Filtro para convertir UTC a hora argentina (UTC-3)
@app.template_filter('hora_argentina')
def hora_argentina_filter(utc_datetime):
    """Convierte datetime UTC a hora legal argentina (UTC-3) y formatea como 'dd/mm/yyyy HH:MM HLA'"""
    if utc_datetime is None:
        return ''
    # Convertir a hora argentina (UTC-3)
    argentina_time = utc_datetime - timedelta(hours=3)
    return argentina_time.strftime('%d/%m/%Y %H:%M HLA')

# Registrar blueprints
from auth.routes import auth_bp
from main.routes import main_bp
from admin.routes import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)

# 🔒 BACKUP AUTOMÁTICO antes de iniciar
if not os.environ.get('DATABASE_URL'):  # Solo en desarrollo local
    try:
        from auto_backup import backup_database
        backup_database()
    except ImportError:
        pass

# Crear tablas si no existen y asegurar admin existe
with app.app_context():
    db.create_all()
    
    # Crear usuario admin automáticamente si no existe
    admin = User.query.filter_by(email='admin@prode.com').first()
    if not admin:
        admin = User(email='admin@prode.com', name='Admin')
        admin.set_password('admin123')
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado automáticamente")
    else:
        # Asegurar que tenga privilegios de admin
        if not admin.is_admin:
            admin.is_admin = True
            db.session.commit()
            print("✅ Privilegios de admin actualizados")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)