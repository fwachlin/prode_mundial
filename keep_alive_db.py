"""
Script para mantener la base de datos de Supabase activa.
Hace una query simple cada vez que se ejecuta.
"""
import os
import sys
from sqlalchemy import create_engine, text

def keep_alive():
    """Ejecuta una query simple para mantener la DB activa"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL no está configurada")
        sys.exit(1)
    
    # Ajustar formato si es necesario
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Crear conexión
        engine = create_engine(database_url)
        
        # Ejecutar query simple
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            
        print(f"✅ Keep-alive exitoso: {count} usuarios en la base de datos")
        return True
        
    except Exception as e:
        print(f"❌ ERROR en keep-alive: {e}")
        sys.exit(1)

if __name__ == "__main__":
    keep_alive()
