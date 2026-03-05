"""
Agregar columna 'name' a allowed_emails y sincronizar con usuarios (versión simple para SQLite)
"""
import sqlite3

def migrate():
    conn = sqlite3.connect('instance/prode.db')
    cursor = conn.cursor()
    
    try:
        # 1. Ver estado actual
        print("Estado actual de la tabla allowed_emails:")
        cursor.execute("PRAGMA table_info(allowed_emails)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"  Columnas: {columns}")
        
        if 'name' in columns:
            print("\n✓ La columna 'name' ya existe")
            return
        
        # 2. Agregar columna name (permitiendo NULL)
        print("\n1. Agregando columna 'name'...")
        cursor.execute("ALTER TABLE allowed_emails ADD COLUMN name VARCHAR(100)")
        conn.commit()
        print("✅ Columna agregada")
        
        # 3. Sincronizar con usuarios registrados
        print("\n2. Sincronizando nombres desde usuarios...")
        cursor.execute("""
            UPDATE allowed_emails 
            SET name = (
                SELECT users.name 
                FROM users 
                WHERE users.email = allowed_emails.email
            )
            WHERE EXISTS (
                SELECT 1 FROM users WHERE users.email = allowed_emails.email
            )
        """)
        updated = cursor.rowcount
        print(f"✅ {updated} emails sincronizados con usuarios")
        
        # 4. Para los que quedan NULL, usar parte del email
        cursor.execute("""
            UPDATE allowed_emails 
            SET name = SUBSTR(email, 1, INSTR(email, '@') - 1)
            WHERE name IS NULL
        """)
        updated2 = cursor.rowcount
        print(f"✅ {updated2} emails sin usuario actualizados con nombre genérico")
        
        conn.commit()
        
        # 5. Verificar
        print("\n3. Verificación:")
        cursor.execute("SELECT id, email, name FROM allowed_emails LIMIT 11")
        rows = cursor.fetchall()
        for row in rows:
            print(f"  ID {row[0]}: {row[1]} → {row[2]}")
        
        print("\n✅ Migración completada")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
