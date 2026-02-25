"""
Script para agregar la columna match_number a la tabla matches
Ejecutar: python add_match_number_column.py
"""
from app import app
from models import db

with app.app_context():
    # Para SQLite, necesitamos hacer ALTER TABLE
    try:
        db.session.execute(db.text('ALTER TABLE matches ADD COLUMN match_number INTEGER'))
        db.session.commit()
        print("✅ Columna 'match_number' agregada exitosamente a la tabla 'matches'")
    except Exception as e:
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("ℹ️  La columna 'match_number' ya existe en la tabla 'matches'")
        else:
            print(f"❌ Error: {e}")
            db.session.rollback()
