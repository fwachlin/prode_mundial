"""
Verificar estado de base de datos en Render
"""
import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print(f"🔍 Conectando a: {DATABASE_URL[:50]}...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Verificar tablas
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = cur.fetchall()
    
    print(f"\n📋 Tablas encontradas: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Contar registros en cada tabla
    print(f"\n📊 Conteo de registros:")
    for table in tables:
        table_name = table[0]
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            print(f"   {table_name}: {count} registros")
        except Exception as e:
            print(f"   {table_name}: Error - {e}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
