"""
🔒 BACKUP MANUAL DESDE RENDER
Ejecutar: python backup_from_render.py

1. Sincroniza Render → Local (instance/prode.db)
2. Crea backup timestamped (backups/)
3. Muestra resumen de datos
"""
import os
import sys

print("=" * 80)
print("🔒 BACKUP MANUAL DESDE RENDER")
print("=" * 80)

# Verificar DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("\n❌ ERROR: Variable DATABASE_URL no configurada")
    print("\nConfigúrala primero:")
    print("  $env:DATABASE_URL='postgresql://...'")
    print("\nObtén la URL desde:")
    print("  Render Dashboard → PostgreSQL Service → Connect → External Database URL")
    sys.exit(1)

print(f"\n✅ DATABASE_URL configurada")
print(f"   {DATABASE_URL[:50]}...")

# Paso 1: Sincronizar desde Render
print("\n" + "=" * 80)
print("PASO 1: Sincronizando Render → Local")
print("=" * 80)

import subprocess
result = subprocess.run(['python', 'sync_db_from_render.py'], capture_output=False)

if result.returncode != 0:
    print("\n❌ Error en sincronización")
    sys.exit(1)

# Paso 2: Crear backup local
print("\n" + "=" * 80)
print("PASO 2: Creando backup timestamped")
print("=" * 80)

from auto_backup import backup_database
backup_path = backup_database()

if backup_path:
    print(f"✅ Backup creado: {backup_path}")
else:
    print("⚠️ No se pudo crear backup (base de datos vacía?)")

# Paso 3: Resumen
print("\n" + "=" * 80)
print("📊 RESUMEN DEL BACKUP")
print("=" * 80)

from app import app
from models import User, Match, Prediction, Phase, AllowedEmail, Comment

with app.app_context():
    users = User.query.count()
    matches = Match.query.count()
    predictions = Prediction.query.count()
    phases = Phase.query.count()
    emails = AllowedEmail.query.count()
    comments = Comment.query.count()
    
    print(f"\n✅ Datos respaldados:")
    print(f"   - {users} usuarios")
    print(f"   - {matches} partidos")
    print(f"   - {predictions} pronósticos")
    print(f"   - {phases} fases")
    print(f"   - {emails} emails permitidos")
    print(f"   - {comments} comentarios")

print("\n" + "=" * 80)
print("✅ BACKUP COMPLETADO EXITOSAMENTE")
print("=" * 80)
print(f"\n📂 Ubicaciones:")
print(f"   - Base de datos local: instance/prode.db")
print(f"   - Backup timestamped: {backup_path if backup_path else 'N/A'}")
print("\n💡 Para restaurar este backup más tarde:")
print(f"   python auto_backup.py restore")
print("=" * 80 + "\n")
