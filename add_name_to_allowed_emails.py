"""
Script de migración para agregar columna 'name' a la tabla allowed_emails
Ejecutar UNA SOLA VEZ después de actualizar el código
"""
from app import app
from extensions import db
from sqlalchemy import text

def add_name_column():
    """Agregar columna name a allowed_emails si no existe"""
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
                return
            
            # Agregar columna name (permitiendo NULL temporalmente)
            print("Agregando columna 'name' a allowed_emails...")
            db.session.execute(text("""
                ALTER TABLE allowed_emails 
                ADD COLUMN name VARCHAR(100)
            """))
            db.session.commit()
            print("✓ Columna 'name' agregada exitosamente")
            
            # Actualizar registros existentes con un nombre por defecto basado en el email
            print("Actualizando registros existentes...")
            db.session.execute(text("""
                UPDATE allowed_emails 
                SET name = SPLIT_PART(email, '@', 1)
                WHERE name IS NULL
            """))
            db.session.commit()
            print("✓ Registros actualizados con nombres por defecto")
            
            # Hacer la columna NOT NULL
            print("Estableciendo columna como NOT NULL...")
            db.session.execute(text("""
                ALTER TABLE allowed_emails 
                ALTER COLUMN name SET NOT NULL
            """))
            db.session.commit()
            print("✓ Columna 'name' configurada como NOT NULL")
            
            print("\n✅ Migración completada exitosamente")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error durante la migración: {e}")
            print("\nSi estás usando SQLite, usa el script alternativo SQLite.")

def add_name_column_sqlite():
    """Versión para SQLite (usa estrategia diferente)"""
    with app.app_context():
        try:
            # En SQLite, verificamos si la columna existe intentando acceder a ella
            result = db.session.execute(text("PRAGMA table_info(allowed_emails)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'name' in columns:
                print("✓ La columna 'name' ya existe en allowed_emails")
                return
            
            print("Agregando columna 'name' a allowed_emails (SQLite)...")
            db.session.execute(text("""
                ALTER TABLE allowed_emails 
                ADD COLUMN name VARCHAR(100) NOT NULL DEFAULT 'Usuario'
            """))
            db.session.commit()
            
            # Actualizar registros existentes con nombre basado en email
            print("Actualizando registros existentes...")
            db.session.execute(text("""
                UPDATE allowed_emails 
                SET name = SUBSTR(email, 1, INSTR(email, '@') - 1)
                WHERE name = 'Usuario'
            """))
            db.session.commit()
            
            print("✅ Migración completada exitosamente (SQLite)")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error durante la migración: {e}")

if __name__ == '__main__':
    import os
    
    print("=" * 60)
    print("MIGRACIÓN: Agregar campo 'name' a allowed_emails")
    print("=" * 60)
    
    # Detectar si estamos en SQLite o PostgreSQL
    db_url = os.environ.get('DATABASE_URL', '')
    if db_url and 'postgres' in db_url:
        print("\n🔍 Detectado: PostgreSQL")
        add_name_column()
    else:
        print("\n🔍 Detectado: SQLite")
        add_name_column_sqlite()
