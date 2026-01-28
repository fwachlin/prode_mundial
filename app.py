from flask import Flask
from flask_login import LoginManager, current_user
from models import db, User
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prode_mundial.db'
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

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