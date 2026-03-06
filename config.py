import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key - debe estar en variable de entorno en producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or "cambiar-mas-adelante"
    
    # Base de datos
    # Prioridad: DATABASE_URL (Render/Fly.io) > SQLite local
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Ajustar formato postgres:// a postgresql:// si es necesario
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        
        # Configuración para PostgreSQL en producción
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
    else:
        # Desarrollo local: SQLite
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "prode.db")
        SQLALCHEMY_ENGINE_OPTIONS = {}
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google Analytics 4 - Opcional
    GA_MEASUREMENT_ID = os.environ.get('GA_MEASUREMENT_ID')