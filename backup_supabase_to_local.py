"""
Script para hacer backup de la base de datos Supabase a SQLite local

INSTRUCCIONES:
1. Asegúrate de tener la variable de entorno DATABASE_URL configurada con la URL de Supabase
2. Cierra cualquier instancia de la aplicación Flask que esté corriendo
3. Ejecuta: python backup_supabase_to_local.py

El script:
- Se conecta a Supabase (PostgreSQL)
- Extrae todos los datos
- Los inserta en la base de datos local (instance/prode.db)
- Hace backup del archivo local antes de sobrescribir
"""

import os
import sys
import shutil
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def backup_supabase_to_local():
    """Copia todos los datos de Supabase a la base de datos local"""
    
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
    
    # 3. Preparar base de datos local
    base_dir = os.path.abspath(os.path.dirname(__file__))
    local_db_path = os.path.join(base_dir, "instance", "prode.db")
    
    # Hacer backup del archivo actual si existe
    if os.path.exists(local_db_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = local_db_path.replace(".db", f"_backup_{timestamp}.db")
        shutil.copy2(local_db_path, backup_path)
        print(f"✅ Backup del archivo local creado: {backup_path}")
    
    # Conectar a SQLite local
    local_db_uri = f"sqlite:///{local_db_path}"
    local_engine = create_engine(local_db_uri)
    LocalSession = sessionmaker(bind=local_engine)
    local_session = LocalSession()
    
    print(f"✅ Conectado a base de datos local: {local_db_path}")
    
    # 4. Obtener datos de Supabase en orden correcto (respetando foreign keys)
    tables_order = [
        'groups',
        'teams', 
        'phases',
        'matches',
        'allowed_emails',
        'users',
        'predictions',
        'comment'
    ]
    
    # 5. Limpiar tablas locales (en orden inverso para respetar FK)
    print("\n🗑️  Limpiando base de datos local...")
    local_session.execute(text("PRAGMA foreign_keys = OFF"))
    
    for table in reversed(tables_order):
        try:
            local_session.execute(text(f"DELETE FROM {table}"))
            print(f"   ✓ Tabla {table} limpiada")
        except Exception as e:
            print(f"   ⚠️  Advertencia limpiando {table}: {e}")
    
    local_session.commit()
    local_session.execute(text("PRAGMA foreign_keys = ON"))
    
    # 6. Copiar datos tabla por tabla
    print("\n📦 Copiando datos de Supabase a local...")
    
    total_rows = 0
    
    for table in tables_order:
        try:
            # Obtener datos de Supabase
            result = supabase_session.execute(text(f"SELECT * FROM {table}"))
            rows = result.fetchall()
            columns = result.keys()
            
            if not rows:
                print(f"   ⚠️  Tabla {table}: 0 filas")
                continue
            
            # Insertar en local
            for row in rows:
                # Crear diccionario con los datos
                row_dict = dict(zip(columns, row))
                
                # Construir query INSERT
                cols = ', '.join(row_dict.keys())
                placeholders = ', '.join([f':{k}' for k in row_dict.keys()])
                insert_query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
                
                local_session.execute(text(insert_query), row_dict)
            
            local_session.commit()
            total_rows += len(rows)
            print(f"   ✓ Tabla {table}: {len(rows)} filas copiadas")
            
        except Exception as e:
            print(f"   ❌ Error copiando tabla {table}: {e}")
            local_session.rollback()
            continue
    
    # 7. Cerrar conexiones
    supabase_session.close()
    local_session.close()
    
    print(f"\n✅ ¡Backup completado exitosamente!")
    print(f"   Total de filas copiadas: {total_rows}")
    print(f"   Base de datos local: {local_db_path}")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("BACKUP DE SUPABASE A BASE DE DATOS LOCAL")
    print("=" * 60)
    
    try:
        backup_supabase_to_local()
    except KeyboardInterrupt:
        print("\n\n⚠️  Backup cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
