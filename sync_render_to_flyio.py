"""
Script para sincronizar datos de Render PostgreSQL a Fly.io PostgreSQL
Migración completa: allowed_emails, users, phases, matches, predictions, comment
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def get_render_connection():
    """Obtener conexión a base de datos Render"""
    render_url = os.environ.get('RENDER_DATABASE_URL')
    if not render_url:
        print("❌ ERROR: Variable RENDER_DATABASE_URL no encontrada")
        print("   Configúrala con: set RENDER_DATABASE_URL=postgresql://...")
        sys.exit(1)
    
    # Ajustar formato si es necesario
    if render_url.startswith('postgres://'):
        render_url = render_url.replace('postgres://', 'postgresql://', 1)
    
    return create_engine(render_url)

def get_flyio_connection():
    """Obtener conexión a base de datos Fly.io"""
    flyio_url = os.environ.get('FLYIO_DATABASE_URL')
    if not flyio_url:
        print("❌ ERROR: Variable FLYIO_DATABASE_URL no encontrada")
        print("   Configúrala con: set FLYIO_DATABASE_URL=postgresql://...")
        sys.exit(1)
    
    # Ajustar formato si es necesario
    if flyio_url.startswith('postgres://'):
        flyio_url = flyio_url.replace('postgres://', 'postgresql://', 1)
    
    return create_engine(flyio_url)

def sync_table(render_session, flyio_session, table_name, columns):
    """Sincronizar una tabla completa"""
    print(f"\n{'='*60}")
    print(f"Sincronizando: {table_name}")
    print(f"{'='*60}")
    
    # Leer datos de Render
    query = f"SELECT * FROM {table_name} ORDER BY id"
    result = render_session.execute(text(query))
    rows = result.fetchall()
    
    print(f"  Registros en Render: {len(rows)}")
    
    if len(rows) == 0:
        print(f"  ⚠️  Tabla {table_name} vacía en Render")
        return
    
    # Limpiar tabla en Fly.io
    flyio_session.execute(text(f"DELETE FROM {table_name}"))
    flyio_session.commit()
    print(f"  ✓ Tabla limpiada en Fly.io")
    
    # Insertar datos en Fly.io
    col_str = ", ".join(columns)
    placeholders = ", ".join([f":{col}" for col in columns])
    insert_query = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholders})"
    
    for row in rows:
        row_dict = dict(zip(columns, row))
        flyio_session.execute(text(insert_query), row_dict)
    
    flyio_session.commit()
    print(f"  ✓ {len(rows)} registros insertados en Fly.io")

def sync_all():
    """Sincronizar todas las tablas"""
    print("="*70)
    print("MIGRACIÓN DE RENDER A FLY.IO")
    print("="*70)
    
    render_engine = get_render_connection()
    flyio_engine = get_flyio_connection()
    
    RenderSession = sessionmaker(bind=render_engine)
    FlyioSession = sessionmaker(bind=flyio_engine)
    
    render_session = RenderSession()
    flyio_session = FlyioSession()
    
    try:
        # 1. allowed_emails
        sync_table(
            render_session, flyio_session,
            'allowed_emails',
            ['id', 'email', 'name']
        )
        
        # 2. users
        sync_table(
            render_session, flyio_session,
            'users',
            ['id', 'email', 'name', 'password_hash', 'is_admin', 'is_enabled']
        )
        
        # 3. phases
        sync_table(
            render_session, flyio_session,
            'phases',
            ['id', 'name', 'order']
        )
        
        # 4. matches
        sync_table(
            render_session, flyio_session,
            'matches',
            ['id', 'home_team', 'away_team', 'kickoff_at', 'closes_at',
             'home_goals', 'away_goals', 'phase_id']
        )
        
        # 5. predictions
        sync_table(
            render_session, flyio_session,
            'predictions',
            ['id', 'user_id', 'match_id', 'home_goals', 'away_goals']
        )
        
        # 6. comment
        sync_table(
            render_session, flyio_session,
            'comment',
            ['id', 'user_id', 'text', 'created_at']
        )
        
        print("\n" + "="*70)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        
        # Resumen
        print("\nResumen:")
        for table in ['allowed_emails', 'users', 'phases', 'matches', 'predictions', 'comment']:
            result = flyio_session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"  {table}: {count} registros")
        
    except Exception as e:
        print(f"\n❌ ERROR durante la migración: {e}")
        flyio_session.rollback()
        raise
    finally:
        render_session.close()
        flyio_session.close()

if __name__ == "__main__":
    print("\n⚠️  IMPORTANTE:")
    print("   Antes de ejecutar, configura las variables de entorno:")
    print("   set RENDER_DATABASE_URL=postgresql://user:pass@host/db")
    print("   set FLYIO_DATABASE_URL=postgresql://user:pass@host/db")
    print("\n   Presiona ENTER para continuar o Ctrl+C para cancelar...")
    input()
    
    sync_all()
