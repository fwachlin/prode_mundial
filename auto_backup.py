"""
🔒 BACKUP AUTOMÁTICO DE BASE DE DATOS
Este script se ejecuta automáticamente al iniciar Flask
Y en cada operación crítica del sistema
"""
import os
import shutil
from datetime import datetime

def backup_database():
    """Crear backup de la base de datos antes de cualquier operación"""
    db_path = os.path.join('instance', 'prode.db')
    
    if not os.path.exists(db_path):
        return None
    
    # Verificar que la DB tiene datos (más de 50KB)
    db_size = os.path.getsize(db_path)
    if db_size < 50000:
        print(f"⚠️ Base de datos muy pequeña ({db_size} bytes) - posiblemente vacía")
        return None
    
    # Crear carpeta de backups
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nombre del backup con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'prode_backup_{timestamp}.db')
    
    # Copiar base de datos
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado: {backup_path} ({db_size:,} bytes)")
        
        # Mantener solo los últimos 10 backups
        cleanup_old_backups(backup_dir, keep=10)
        
        return backup_path
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return None

def backup_on_change(operation_type="cambio"):
    """
    Crear backup automático en cada operación crítica
    Para ser llamado desde rutas que modifican datos
    
    operation_type: "pronóstico", "usuario", "resultado", "cambio"
    """
    db_path = os.path.join('instance', 'prode.db')
    
    if not os.path.exists(db_path):
        return None
    
    # Verificar que la DB tiene datos
    db_size = os.path.getsize(db_path)
    if db_size < 50000:
        return None
    
    # Crear carpeta de backups automáticos
    backup_dir = 'backups/auto'
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nombre del backup con timestamp y tipo de operación
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'auto_{operation_type}_{timestamp}.db')
    
    # Copiar base de datos silenciosamente (sin print en producción)
    try:
        shutil.copy2(db_path, backup_path)
        
        # Mantener solo los últimos 30 backups automáticos
        cleanup_auto_backups(backup_dir, keep=30)
        
        return backup_path
    except Exception as e:
        # Silenciar errores en producción (no afectar experiencia del usuario)
        return None

def cleanup_old_backups(backup_dir, keep=10):
    """Eliminar backups antiguos, manteniendo solo los últimos N"""
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith('prode_backup_') and file.endswith('.db'):
            filepath = os.path.join(backup_dir, file)
            backups.append((filepath, os.path.getmtime(filepath)))
    
    # Ordenar por fecha (más reciente primero)
    backups.sort(key=lambda x: x[1], reverse=True)
    
    # Eliminar los más antiguos
    for filepath, _ in backups[keep:]:
        try:
            os.remove(filepath)
            print(f"🗑️ Backup antiguo eliminado: {os.path.basename(filepath)}")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar {filepath}: {e}")

def cleanup_auto_backups(backup_dir, keep=30):
    """Eliminar backups automáticos antiguos, manteniendo solo los últimos N"""
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith('auto_') and file.endswith('.db'):
            filepath = os.path.join(backup_dir, file)
            backups.append((filepath, os.path.getmtime(filepath)))
    
    # Ordenar por fecha (más reciente primero)
    backups.sort(key=lambda x: x[1], reverse=True)
    
    # Eliminar los más antiguos (silenciosamente)
    for filepath, _ in backups[keep:]:
        try:
            os.remove(filepath)
        except:
            pass  # Silenciar errores

def restore_latest_backup():
    """Restaurar el backup más reciente"""
    backup_dir = 'backups'
    
    if not os.path.exists(backup_dir):
        print("❌ No hay backups disponibles")
        return False
    
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith('prode_backup_') and file.endswith('.db'):
            filepath = os.path.join(backup_dir, file)
            backups.append((filepath, os.path.getmtime(filepath)))
    
    if not backups:
        print("❌ No hay backups disponibles")
        return False
    
    # Backup más reciente
    backups.sort(key=lambda x: x[1], reverse=True)
    latest_backup, _ = backups[0]
    
    # Restaurar
    db_path = os.path.join('instance', 'prode.db')
    try:
        shutil.copy2(latest_backup, db_path)
        print(f"✅ Base de datos restaurada desde: {os.path.basename(latest_backup)}")
        return True
    except Exception as e:
        print(f"❌ Error restaurando backup: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        restore_latest_backup()
    else:
        backup_database()
