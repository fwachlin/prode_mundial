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

# Ejecutar migración para agregar columna 'name' a allowed_emails
python << END
import os
os.environ['RENDER'] = '1'
from app import app
from extensions import db
from sqlalchemy import text

with app.app_context():
    try:
        # Verificar si la columna ya existe
        result = db.session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='allowed_emails' AND column_name='name'
        """))
        
        if result.fetchone():
            print("✓ La columna 'name' ya existe en allowed_emails")
        else:
            # Agregar columna
            print("Agregando columna 'name' a allowed_emails...")
            db.session.execute(text("""
                ALTER TABLE allowed_emails 
                ADD COLUMN name VARCHAR(100)
            """))
            db.session.commit()
            
            # Actualizar registros existentes
            print("Actualizando registros existentes...")
            db.session.execute(text("""
                UPDATE allowed_emails 
                SET name = SPLIT_PART(email, '@', 1)
                WHERE name IS NULL
            """))
            db.session.commit()
            
            # Hacer columna NOT NULL
            print("Estableciendo columna como NOT NULL...")
            db.session.execute(text("""
                ALTER TABLE allowed_emails 
                ALTER COLUMN name SET NOT NULL
            """))
            db.session.commit()
            print("✅ Migración de 'name' completada exitosamente")
    except Exception as e:
        db.session.rollback()
        print(f"⚠️ Error en migración: {e}")
        # No fallar el build si la columna ya existe
        pass
END

