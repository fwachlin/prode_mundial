#!/usr/bin/env bash
# Build script para Render.com

set -o errexit  # Salir si hay error

# Instalar dependencias
pip install -r requirements.txt

# Crear directorio instance si no existe
mkdir -p /opt/render/project/src/instance

# Inicializar base de datos
python << END
import os
os.environ['RENDER'] = '1'
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Base de datos inicializada')
END

