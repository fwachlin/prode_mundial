# -*- coding: utf-8 -*-
import sqlite3

for db_name in ['instance/prode.db', 'instance/prode_mundial.db']:
    print(f"\n{'='*60}")
    print(f"Verificando: {db_name}")
    print('='*60)
    
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if tables:
            print("\nTablas encontradas:")
            for t in tables:
                print(f"  - {t[0]}")

            # Buscar tabla de partidos
            table_name = None
            for name in ['match', 'matches', 'Match']:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {name}")
                    count = cursor.fetchone()[0]
                    table_name = name
                    print(f"\nTabla de partidos: {name} ({count} registros)")
                    break
                except:
                    pass
            
            if table_name:
                print(f"\nPrimeros 10 partidos en {table_name}:")
                cursor.execute(f"SELECT id, home_team, away_team FROM {table_name} LIMIT 10")
                rows = cursor.fetchall()
                for r in rows:
                    print(f"  ID: {r[0]:3d} | Home: '{r[1]:6s}' | Away: '{r[2]:6s}'")
        else:
            print("\n⚠ Base de datos vacía (sin tablas)")
        
        conn.close()
    except Exception as e:
        print(f"\n❌ Error: {e}")

print("\n" + "="*60)
