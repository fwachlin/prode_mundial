"""
Script para exportar la base de datos Supabase a archivos JSON

INSTRUCCIONES:
1. Asegúrate de tener la variable de entorno DATABASE_URL configurada con la URL de Supabase
2. Ejecuta: python export_supabase_to_json.py

El script:
- Se conecta a Supabase (PostgreSQL)
- Exporta cada tabla a un archivo JSON separado
- Crea una carpeta con timestamp en backups/
"""

import os
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

def export_supabase_to_json():
    """Exporta todos los datos de Supabase a archivos JSON"""
    
    # 1. Verificar que existe DATABASE_URL
    supabase_url = os.environ.get('DATABASE_URL')
    if not supabase_url:
        print("❌ ERROR: No se encontró la variable de entorno DATABASE_URL")
        print("   Debes configurar DATABASE_URL con la URL de tu base de datos Supabase")
        sys.exit(1)
    
    # Ajustar formato si es necesario
    if supabase_url.startswith('postgres://'):
        supabase_url = supabase_url.replace('postgres://', 'postgresql://', 1)
    
    print(f"✅ Conectando a Supabase...")
    
    # 2. Conectar a Supabase
    try:
        supabase_engine = create_engine(supabase_url, pool_pre_ping=True)
        SupabaseSession = sessionmaker(bind=supabase_engine)
        supabase_session = SupabaseSession()
    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        sys.exit(1)
    
    # 3. Crear carpeta de backup
    base_dir = os.path.abspath(os.path.dirname(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(base_dir, "backups", f"supabase_backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)
    
    print(f"✅ Carpeta de backup creada: {backup_folder}")
    
    # 4. Lista de tablas a exportar
    tables = [
        'groups',
        'teams',
        'phases',
        'matches',
        'allowed_emails',
        'users',
        'predictions',
        'comment'
    ]
    
    # 5. Exportar cada tabla
    print("\n📦 Exportando tablas...")
    
    backup_info = {
        'timestamp': timestamp,
        'date': datetime.now().isoformat(),
        'tables': {}
    }
    
    for table in tables:
        try:
            # Obtener datos
            result = supabase_session.execute(text(f"SELECT * FROM {table}"))
            rows = result.fetchall()
            columns = result.keys()
            
            # Convertir a lista de diccionarios
            data = []
            for row in rows:
                row_dict = {}
                for col, val in zip(columns, row):
                    # Convertir datetime a string
                    if isinstance(val, datetime):
                        val = val.isoformat()
                    row_dict[col] = val
                data.append(row_dict)
            
            # Guardar a JSON
            json_file = os.path.join(backup_folder, f"{table}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            backup_info['tables'][table] = {
                'rows': len(data),
                'file': f"{table}.json"
            }
            
            print(f"   ✓ {table}: {len(data)} filas → {table}.json")
            
        except Exception as e:
            print(f"   ❌ Error exportando tabla {table}: {e}")
            backup_info['tables'][table] = {
                'error': str(e)
            }
            continue
    
    # 6. Guardar información del backup
    info_file = os.path.join(backup_folder, "_backup_info.json")
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(backup_info, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Exportación completada!")
    print(f"   Carpeta: {backup_folder}")
    print(f"   Archivos creados: {len(backup_info['tables']) + 1}")
    
    # Mostrar resumen
    print("\n📊 Resumen:")
    total_rows = 0
    for table, info in backup_info['tables'].items():
        if 'rows' in info:
            total_rows += info['rows']
            print(f"   {table}: {info['rows']} filas")
    print(f"\n   Total: {total_rows} filas")
    
    # 7. Cerrar conexión
    supabase_session.close()
    
    return backup_folder

if __name__ == "__main__":
    print("=" * 60)
    print("EXPORTAR SUPABASE A JSON")
    print("=" * 60)
    
    try:
        backup_folder = export_supabase_to_json()
        print(f"\n✅ Backup guardado en: {backup_folder}")
    except KeyboardInterrupt:
        print("\n\n⚠️  Exportación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
