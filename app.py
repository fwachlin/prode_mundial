from flask import Flask
from flask_login import LoginManager, current_user
from models import db, User
from datetime import datetime, timezone
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
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Desarrollo local con SQLite
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'prode.db')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
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
    """Convierte nombre de país a código FIFA de 3 letras"""
    # Si ya es un código FIFA (3 letras mayúsculas o contiene "Path"), devolverlo tal cual
    if not country_name:
        return ''
    if len(country_name) <= 4 and country_name.isupper():
        return country_name
    if 'Path' in country_name or 'IC' in country_name:
        return country_name
    # Placeholders de eliminación directa
    # Primero verificar los códigos de grupo (1A, 2B, 3C/D/E, etc.)
    if any(country_name.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                                  '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                                  '3A', '3B', '3C', '3D', '3E', '3F']):
        return country_name
    
    # W y L solo si van seguidos de un número (W1, W2, L25, etc.)
    if (country_name.startswith('W') or country_name.startswith('L')) and len(country_name) >= 2:
        if country_name[1].isdigit():
            return country_name
    
    fifa_codes = {
        'Argentina': 'ARG', 'Brasil': 'BRA', 'Uruguay': 'URU', 'Chile': 'CHI',
        'Paraguay': 'PAR', 'Colombia': 'COL', 'Ecuador': 'ECU', 'Perú': 'PER',
        'Venezuela': 'VEN', 'Bolivia': 'BOL', 'México': 'MEX', 'Estados Unidos': 'USA',
        'EEUU': 'USA', 'EE.UU.': 'USA', 'USA': 'USA',
        'Canadá': 'CAN', 'Costa Rica': 'CRC', 'Jamaica': 'JAM', 'Panamá': 'PAN',
        'Honduras': 'HON', 'El Salvador': 'SLV', 'Trinidad y Tobago': 'TRI',
        'Alemania': 'GER', 'España': 'ESP', 'Francia': 'FRA', 'Inglaterra': 'ENG',
        'Italia': 'ITA', 'Portugal': 'POR', 'Países Bajos': 'NED', 'Holanda': 'NED', 'Bélgica': 'BEL',
        'Croacia': 'CRO', 'Dinamarca': 'DEN', 'Suiza': 'SUI', 'Polonia': 'POL',
        'Suecia': 'SWE', 'Austria': 'AUT', 'República Checa': 'CZE', 'Serbia': 'SRB',
        'Ucrania': 'UKR', 'Gales': 'WAL', 'Escocia': 'SCO', 'Noruega': 'NOR',
        'Japón': 'JPN', 'Corea del Sur': 'KOR', 'Australia': 'AUS', 'Arabia Saudita': 'KSA',
        'Irán': 'IRN', 'Irak': 'IRQ', 'Catar': 'QAT', 'Qatar': 'QAT', 'China': 'CHN',
        'Nigeria': 'NGA', 'Senegal': 'SEN', 'Ghana': 'GHA', 'Camerún': 'CMR',
        'Túnez': 'TUN', 'Argelia': 'ALG', 'Marruecos': 'MAR', 'Costa de Marfil': 'CIV',
        'Egipto': 'EGY', 'Sudáfrica': 'RSA', 'Mali': 'MLI', 'Burkina Faso': 'BFA',
        'Nueva Zelanda': 'NZL',
        'Haití': 'HAI', 'Haiti': 'HAI', 'Escocia': 'SCO', 'Scotland': 'SCO',
        'Curaçao': 'CUW', 'Curacao': 'CUW', 'Uzbekistán': 'UZB', 'Uzbekistan': 'UZB',
        'Jordania': 'JOR', 'Jordan': 'JOR', 'Cabo Verde': 'CPV', 'Cape Verde': 'CPV'
    }
    return fifa_codes.get(country_name, country_name[:3].upper())

# Filtro para convertir nombres de países a códigos ISO 3166-1 alpha-2 (para banderas)
@app.template_filter('country_iso2')
def country_iso2_filter(country_name):
    """Convierte nombre de país o código FIFA a código ISO de 2 letras para mostrar banderas"""
    if not country_name:
        return 'xx'
    
    # Si contiene "Path" o "IC", no mostrar bandera
    if 'Path' in country_name or country_name.startswith('IC '):
        return 'xx'
    
    # Placeholders de eliminación directa
    # Primero verificar los códigos de grupo (1A, 2B, 3C/D/E, etc.)
    if any(country_name.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                                  '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                                  '3A', '3B', '3C', '3D', '3E', '3F']):
        return 'xx'
    
    # W y L solo si van seguidos de un número (W1, W2, L25, etc.)
    if (country_name.startswith('W') or country_name.startswith('L')) and len(country_name) >= 2:
        if country_name[1].isdigit():
            return 'xx'
    
    # Mapeo de códigos FIFA a ISO2
    fifa_to_iso2 = {
        'ARG': 'ar', 'BRA': 'br', 'URU': 'uy', 'CHI': 'cl', 'PAR': 'py', 
        'COL': 'co', 'ECU': 'ec', 'PER': 'pe', 'VEN': 've', 'BOL': 'bo',
        'MEX': 'mx', 'USA': 'us', 'CAN': 'ca', 'CRC': 'cr', 'JAM': 'jm', 
        'PAN': 'pa', 'HON': 'hn', 'SLV': 'sv', 'TRI': 'tt',
        'GER': 'de', 'ESP': 'es', 'FRA': 'fr', 'ENG': 'gb-eng', 'ITA': 'it', 
        'POR': 'pt', 'NED': 'nl', 'BEL': 'be', 'CRO': 'hr', 'DEN': 'dk',
        'SUI': 'ch', 'POL': 'pl', 'SWE': 'se', 'AUT': 'at', 'CZE': 'cz', 
        'SRB': 'rs', 'UKR': 'ua', 'WAL': 'gb-wls', 'SCO': 'gb-sct', 'NOR': 'no',
        'JPN': 'jp', 'KOR': 'kr', 'AUS': 'au', 'KSA': 'sa', 'IRN': 'ir', 
        'IRQ': 'iq', 'QAT': 'qa', 'CHN': 'cn',
        'NGA': 'ng', 'SEN': 'sn', 'GHA': 'gh', 'CMR': 'cm', 'TUN': 'tn', 
        'ALG': 'dz', 'MAR': 'ma', 'CIV': 'ci', 'EGY': 'eg', 'RSA': 'za',
        'MLI': 'ml', 'BFA': 'bf', 'NZL': 'nz', 'HAI': 'ht', 'CUW': 'cw',
        'UZB': 'uz', 'JOR': 'jo', 'CPV': 'cv'
    }
    
    # Mapeo de nombres completos a ISO2 (para compatibilidad)
    country_to_iso2 = {
        'Argentina': 'ar', 'Brasil': 'br', 'Uruguay': 'uy', 'Chile': 'cl',
        'Paraguay': 'py', 'Colombia': 'co', 'Ecuador': 'ec', 'Perú': 'pe',
        'Venezuela': 've', 'Bolivia': 'bo', 'México': 'mx', 'Estados Unidos': 'us',
        'EEUU': 'us', 'EE.UU.': 'us', 'USA': 'us',
        'Canadá': 'ca', 'Costa Rica': 'cr', 'Jamaica': 'jm', 'Panamá': 'pa',
        'Honduras': 'hn', 'El Salvador': 'sv', 'Trinidad y Tobago': 'tt',
        'Alemania': 'de', 'España': 'es', 'Francia': 'fr', 'Inglaterra': 'gb-eng',
        'Italia': 'it', 'Portugal': 'pt', 'Países Bajos': 'nl', 'Holanda': 'nl', 'Bélgica': 'be',
        'Croacia': 'hr', 'Dinamarca': 'dk', 'Suiza': 'ch', 'Polonia': 'pl',
        'Suecia': 'se', 'Austria': 'at', 'República Checa': 'cz', 'Serbia': 'rs',
        'Ucrania': 'ua', 'Gales': 'gb-wls', 'Escocia': 'gb-sct', 'Noruega': 'no',
        'Japón': 'jp', 'Corea del Sur': 'kr', 'Australia': 'au', 'Arabia Saudita': 'sa',
        'Irán': 'ir', 'Irak': 'iq', 'Catar': 'qa', 'Qatar': 'qa', 'China': 'cn',
        'Nigeria': 'ng', 'Senegal': 'sn', 'Ghana': 'gh', 'Camerún': 'cm',
        'Túnez': 'tn', 'Argelia': 'dz', 'Marruecos': 'ma', 'Costa de Marfil': 'ci',
        'Egipto': 'eg', 'Sudáfrica': 'za', 'Mali': 'ml', 'Burkina Faso': 'bf',
        'Nueva Zelanda': 'nz', 'Haití': 'ht', 'Haiti': 'ht', 'Curaçao': 'cw',
        'Curacao': 'cw', 'Uzbekistán': 'uz', 'Uzbekistan': 'uz', 'Jordania': 'jo',
        'Jordan': 'jo', 'Cabo Verde': 'cv', 'Cape Verde': 'cv'
    }
    
    # Intentar primero con códigos FIFA, luego con nombres
    return fifa_to_iso2.get(country_name, country_to_iso2.get(country_name, 'xx'))

# Registrar blueprints
from auth.routes import auth_bp
from main.routes import main_bp
from admin.routes import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)

# Registrar endpoint temporal solo si existe
try:
    from reset_db_endpoint import reset_bp
    app.register_blueprint(reset_bp)
except ImportError:
    pass

# Crear tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)