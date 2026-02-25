"""
🔒 BACKUP DESDE RENDER - Versión Simple
Crea backup directamente desde Render a carpeta backups/
"""
import os
import sys
from datetime import datetime

print("=" * 80)
print("🔒 BACKUP DESDE RENDER")
print("=" * 80)

# Verificar DATABASE_URL
RENDER_URL = os.environ.get('DATABASE_URL')
if not RENDER_URL:
    print("\n❌ ERROR: Variable DATABASE_URL no configurada")
    print("\nConfigúrala primero:")
    print("  $env:DATABASE_URL='postgresql://...'")
    sys.exit(1)

print(f"\n✅ DATABASE_URL configurada")
print(f"   {RENDER_URL[:60]}...")

# Conectar a Render y obtener datos
print("\n🔄 Conectando a Render PostgreSQL...")

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    
    # Crear motor y sesión de Render
    render_engine = create_engine(RENDER_URL)
    RenderSession = sessionmaker(bind=render_engine)
    render_session = RenderSession()
    
    # Verificar conexión
    render_session.execute(text('SELECT 1'))
    print("✅ Conexión exitosa a Render")
    
    # Contar registros
    users_count = render_session.execute(text('SELECT COUNT(*) FROM users')).scalar()
    matches_count = render_session.execute(text('SELECT COUNT(*) FROM matches')).scalar()
    predictions_count = render_session.execute(text('SELECT COUNT(*) FROM predictions')).scalar()
    
    print(f"\n📊 Datos en Render:")
    print(f"   - {users_count} usuarios")
    print(f"   - {matches_count} partidos")
    print(f"   - {predictions_count} pronósticos")
    
    render_session.close()
    render_engine.dispose()
    
    # Crear backup usando pg_dump (si está disponible)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backups/render_backup_{timestamp}.sql"
    
    print(f"\n💾 Creando backup SQL...")
    print(f"   Archivo: {backup_filename}")
    
    # Usar pg_dump si está disponible
    import subprocess
    
    # Extraer componentes de la URL
    import re
    match = re.match(r'postgresql://([^:]+):([^@]+)@([^/]+)/(.+)', RENDER_URL)
    if match:
        user, password, host, database = match.groups()
        
        # Intentar pg_dump
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        try:
            result = subprocess.run([
                'pg_dump',
                '-h', host,
                '-U', user,
                '-d', database,
                '-f', backup_filename
            ], env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Backup SQL creado exitosamente")
                print(f"\n📂 Ubicación: {os.path.abspath(backup_filename)}")
            else:
                print(f"⚠️ pg_dump no disponible o falló")
                print(f"   Datos verificados en Render pero no se creó archivo SQL")
        except FileNotFoundError:
            print(f"⚠️ pg_dump no encontrado en el sistema")
            print(f"   Datos verificados en Render: {users_count} usuarios, {matches_count} partidos, {predictions_count} pronósticos")
    
    print("\n" + "=" * 80)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 80)
    print(f"\n📊 Resumen:")
    print(f"   Render tiene: {users_count} usuarios, {matches_count} partidos, {predictions_count} pronósticos")
    print(f"   Estado: ✅ Datos verificados")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
