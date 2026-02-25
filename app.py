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


# Endpoint temporal de emergencia para agregar Fase 4 (acceso directo)
@app.route('/cargar-fase4-ahora')
def cargar_fase4_emergencia():
    """Endpoint de emergencia para cargar Fase 4 sin autenticación (TEMPORAL)"""
    from models import Phase
    from datetime import timedelta
    
    PARTIDOS_FASE4 = [
        ("1A", "2B", "2026-06-29 19:00"), ("1C", "2D", "2026-06-29 22:00"),
        ("1E", "2F", "2026-06-30 19:00"), ("1G", "2H", "2026-06-30 22:00"),
        ("1B", "2A", "2026-07-01 19:00"), ("1D", "2C", "2026-07-01 22:00"),
        ("1F", "2E", "2026-07-02 19:00"), ("1H", "2G", "2026-07-02 22:00"),
        ("1I", "2J", "2026-07-03 19:00"), ("1K", "2L", "2026-07-03 22:00"),
        ("1J", "2I", "2026-07-04 19:00"), ("1L", "2K", "2026-07-04 22:00"),
        ("1A", "3C/D/E", "2026-07-05 19:00"), ("1B", "3A/C/D", "2026-07-05 22:00"),
        ("1C", "3A/B/E", "2026-07-06 19:00"), ("1D", "3A/B/C", "2026-07-06 22:00"),
        ("W1", "W2", "2026-07-09 19:00"), ("W3", "W4", "2026-07-09 22:00"),
        ("W5", "W6", "2026-07-10 19:00"), ("W7", "W8", "2026-07-10 22:00"),
        ("W9", "W10", "2026-07-11 19:00"), ("W11", "W12", "2026-07-11 22:00"),
        ("W13", "W14", "2026-07-12 19:00"), ("W15", "W16", "2026-07-12 22:00"),
        ("W17", "W18", "2026-07-14 22:00"), ("W19", "W20", "2026-07-15 22:00"),
        ("W21", "W22", "2026-07-16 22:00"), ("W23", "W24", "2026-07-17 22:00"),
        ("L25", "L26", "2026-07-18 19:00"), ("W25", "W26", "2026-07-18 22:00"),
        ("L27", "L28", "2026-07-19 19:00"), ("W27", "W28", "2026-07-19 22:00"),
    ]
    
    try:
        fase4 = Phase.query.filter_by(name='Fecha 4 - Eliminación Directa').first()
        if not fase4:
            return "❌ ERROR: No se encontró la Fase 4", 500
        
        total_antes = Match.query.count()
        partidos_agregados = 0
        
        for home, away, kickoff_str in PARTIDOS_FASE4:
            existing = Match.query.filter_by(home_team=home, away_team=away, phase_id=fase4.id).first()
            if existing:
                continue
            
            kickoff = datetime.strptime(kickoff_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            closes = kickoff - timedelta(minutes=10)
            
            match = Match(home_team=home, away_team=away, kickoff_at=kickoff, closes_at=closes, phase_id=fase4.id)
            db.session.add(match)
            partidos_agregados += 1
        
        db.session.commit()
        total_despues = Match.query.count()
        
        return f"""
        <h1>✅ Fase 4 Cargada Exitosamente</h1>
        <p>Partidos agregados: {partidos_agregados}</p>
        <p>Total antes: {total_antes}</p>
        <p>Total después: {total_despues}</p>
        <p><a href="/admin/dashboard">Ir al Dashboard</a></p>
        <p><strong>IMPORTANTE: Eliminar este endpoint después de usar</strong></p>
        """
    except Exception as e:
        db.session.rollback()
        return f"❌ Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)