from flask import Flask
from flask_login import LoginManager, current_user
from models import db, User
from datetime import datetime, timezone
import os

app = Flask(__name__)

# Configuración de base de datos
# En producción (Render), usar la ruta correcta para instance
if os.environ.get('RENDER'):
    # Render provee un directorio persistente
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/render/project/src/instance/prode_mundial.db'
else:
    # Desarrollo local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prode_mundial.db'

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
    fifa_codes = {
        'Argentina': 'ARG', 'Brasil': 'BRA', 'Uruguay': 'URU', 'Chile': 'CHI',
        'Paraguay': 'PAR', 'Colombia': 'COL', 'Ecuador': 'ECU', 'Perú': 'PER',
        'Venezuela': 'VEN', 'Bolivia': 'BOL', 'México': 'MEX', 'Estados Unidos': 'USA',
        'Canadá': 'CAN', 'Costa Rica': 'CRC', 'Jamaica': 'JAM', 'Panamá': 'PAN',
        'Honduras': 'HON', 'El Salvador': 'SLV', 'Trinidad y Tobago': 'TRI',
        'Alemania': 'GER', 'España': 'ESP', 'Francia': 'FRA', 'Inglaterra': 'ENG',
        'Italia': 'ITA', 'Portugal': 'POR', 'Países Bajos': 'NED', 'Bélgica': 'BEL',
        'Croacia': 'CRO', 'Dinamarca': 'DEN', 'Suiza': 'SUI', 'Polonia': 'POL',
        'Suecia': 'SWE', 'Austria': 'AUT', 'República Checa': 'CZE', 'Serbia': 'SRB',
        'Ucrania': 'UKR', 'Gales': 'WAL', 'Escocia': 'SCO', 'Noruega': 'NOR',
        'Japón': 'JPN', 'Corea del Sur': 'KOR', 'Australia': 'AUS', 'Arabia Saudita': 'KSA',
        'Irán': 'IRN', 'Irak': 'IRQ', 'Catar': 'QAT', 'China': 'CHN',
        'Nigeria': 'NGA', 'Senegal': 'SEN', 'Ghana': 'GHA', 'Camerún': 'CMR',
        'Túnez': 'TUN', 'Argelia': 'ALG', 'Marruecos': 'MAR', 'Costa de Marfil': 'CIV',
        'Egipto': 'EGY', 'Sudáfrica': 'RSA', 'Mali': 'MLI', 'Burkina Faso': 'BFA',
        'Nueva Zelanda': 'NZL'
    }
    return fifa_codes.get(country_name, country_name[:3].upper())

# Registrar blueprints
from auth.routes import auth_bp
from main.routes import main_bp
from admin.routes import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)