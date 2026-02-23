#!/usr/bin/env bash
# Build script para Render.com

# Instalar dependencias
pip install -r requirements.txt

# Crear directorio instance si no existe
mkdir -p instance

# Inicializar base de datos si no existe
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Base de datos inicializada')
"
