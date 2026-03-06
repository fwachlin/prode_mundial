"""
Script para verificar que la migración a Fly.io fue exitosa
Compara datos entre Render y Fly.io
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def get_connection(env_var_name):
    """Obtener conexión a base de datos"""
    db_url = os.environ.get(env_var_name)
    if not db_url:
        print(f"❌ ERROR: Variable {env_var_name} no encontrada")
        sys.exit(1)
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    return create_engine(db_url)

def count_table(session, table_name):
    """Contar registros en una tabla"""
    try:
        result = session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        return result.scalar()
    except Exception as e:
        print(f"  ❌ Error al leer {table_name}: {e}")
        return -1

def verify_migration():
    """Verificar que la migración fue exitosa"""
    print("="*70)
    print("VERIFICACIÓN DE MIGRACIÓN RENDER → FLY.IO")
    print("="*70)
    
    render_engine = get_connection('RENDER_DATABASE_URL')
    flyio_engine = get_connection('FLYIO_DATABASE_URL')
    
    RenderSession = sessionmaker(bind=render_engine)
    FlyioSession = sessionmaker(bind=flyio_engine)
    
    render_session = RenderSession()
    flyio_session = FlyioSession()
    
    tables = ['allowed_emails', 'users', 'phases', 'matches', 'predictions', 'comment']
    
    print("\nComparación de registros:\n")
    print(f"{'Tabla':<20} {'Render':<15} {'Fly.io':<15} {'Estado':<10}")
    print("-"*70)
    
    all_ok = True
    
    for table in tables:
        render_count = count_table(render_session, table)
        flyio_count = count_table(flyio_session, table)
        
        if render_count == flyio_count and render_count >= 0:
            status = "✅ OK"
        else:
            status = "❌ DIFF"
            all_ok = False
        
        print(f"{table:<20} {str(render_count):<15} {str(flyio_count):<15} {status:<10}")
    
    print("\n" + "="*70)
    
    if all_ok:
        print("✅ VERIFICACIÓN EXITOSA: Todos los datos coinciden")
        print("="*70)
        print("\nLa migración se completó correctamente.")
        print("Puedes proceder a hacer el deploy en Fly.io.")
    else:
        print("❌ VERIFICACIÓN FALLIDA: Algunos datos no coinciden")
        print("="*70)
        print("\nRevisa los errores y ejecuta sync_render_to_flyio.py nuevamente.")
    
    render_session.close()
    flyio_session.close()

if __name__ == "__main__":
    print("\n⚠️  Configurar variables de entorno:")
    print("   set RENDER_DATABASE_URL=postgresql://...")
    print("   set FLYIO_DATABASE_URL=postgresql://...")
    print("\n   Presiona ENTER para continuar...")
    input()
    
    verify_migration()
