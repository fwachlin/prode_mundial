"""
Sincronizar base de datos DESDE local (SQLite) HACIA Render (PostgreSQL)

⚠️ ADVERTENCIA: Este script SOBRESCRIBE los datos en Render con los datos locales
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, AllowedEmail, Phase, Match, Prediction, Comment

# Configuración
RENDER_DATABASE_URL = os.environ.get('DATABASE_URL')
if not RENDER_DATABASE_URL:
    print("❌ ERROR: Variable de entorno DATABASE_URL no encontrada")
    print("Configúrala con: $env:DATABASE_URL='postgresql://...'")
    sys.exit(1)

# Arreglar URL si es necesario
if RENDER_DATABASE_URL.startswith('postgres://'):
    RENDER_DATABASE_URL = RENDER_DATABASE_URL.replace('postgres://', 'postgresql://', 1)

LOCAL_DB = 'sqlite:///instance/prode.db'

print("=" * 60)
print("🚀 SINCRONIZACIÓN: LOCAL → RENDER")
print("=" * 60)
print(f"\n📍 Origen: SQLite local (instance/prode.db)")
print(f"📍 Destino: Render PostgreSQL")
print(f"\n⚠️  ADVERTENCIA: Esto SOBRESCRIBIRÁ los datos en Render")

# Confirmación del usuario
respuesta = input("\n¿Deseas continuar? Escribe 'SI SINCRONIZAR' para confirmar: ")
if respuesta != "SI SINCRONIZAR":
    print("❌ Operación cancelada")
    sys.exit(0)

print("\n🔄 Conectando a SQLite local...")
local_engine = create_engine(LOCAL_DB)
LocalSession = sessionmaker(bind=local_engine)

print("🔄 Conectando a Render PostgreSQL...")
render_engine = create_engine(RENDER_DATABASE_URL)
RenderSession = sessionmaker(bind=render_engine)

# Crear todas las tablas en Render si no existen
print("✅ Verificando tablas en Render...")
from sqlalchemy import MetaData
User.__table__.create(render_engine, checkfirst=True)
AllowedEmail.__table__.create(render_engine, checkfirst=True)
Phase.__table__.create(render_engine, checkfirst=True)
Match.__table__.create(render_engine, checkfirst=True)
Prediction.__table__.create(render_engine, checkfirst=True)
Comment.__table__.create(render_engine, checkfirst=True)
print("✅ Tablas verificadas/creadas en Render")

local_session = LocalSession()
render_session = RenderSession()

try:
    print("\n📊 Sincronizando datos...\n")
    
    # IMPORTANTE: Eliminar en orden inverso de dependencias
    # (primero las tablas que dependen de otras)
    
    print("🗑️ Limpiando datos existentes en Render (respetando foreign keys)...")
    render_session.query(Prediction).delete()
    render_session.query(Comment).delete()
    render_session.query(Match).delete()
    render_session.query(Phase).delete()
    render_session.query(User).delete()
    render_session.query(AllowedEmail).delete()
    render_session.commit()
    print("   ✅ Datos anteriores eliminados")
    
    # Ahora insertar en orden correcto
    
    # 1. AllowedEmail (no tiene dependencias)
    print("\n1️⃣ Emails permitidos...")
    local_count = local_session.query(AllowedEmail).count()
    allowed_emails = local_session.query(AllowedEmail).all()
    for ae in allowed_emails:
        new_ae = AllowedEmail(id=ae.id, email=ae.email)
        render_session.merge(new_ae)
    render_session.commit()
    print(f"   ✅ {len(allowed_emails)} emails sincronizados (local: {local_count})")
    
    # 2. Users (depende de AllowedEmail indirectamente)
    print("2️⃣ Usuarios...")
    local_count = local_session.query(User).count()
    users = local_session.query(User).all()
    for user in users:
        new_user = User(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            is_admin=user.is_admin,
            is_enabled=user.is_enabled
        )
        render_session.merge(new_user)
    render_session.commit()
    print(f"   ✅ {len(users)} usuarios sincronizados (local: {local_count})")
    
    # 3. Phases (no tiene dependencias)
    print("3️⃣ Fases...")
    local_count = local_session.query(Phase).count()
    phases = local_session.query(Phase).all()
    for phase in phases:
        new_phase = Phase(
            id=phase.id,
            name=phase.name,
            order=phase.order
        )
        render_session.merge(new_phase)
    render_session.commit()
    print(f"   ✅ {len(phases)} fases sincronizadas (local: {local_count})")
    
    # 4. Matches (depende de Phase)
    print("4️⃣ Partidos...")
    local_count = local_session.query(Match).count()
    matches = local_session.query(Match).all()
    for match in matches:
        new_match = Match(
            id=match.id,
            home_team=match.home_team,
            away_team=match.away_team,
            kickoff_at=match.kickoff_at,
            closes_at=match.closes_at,
            phase_id=match.phase_id,
            home_goals=match.home_goals,
            away_goals=match.away_goals
        )
        render_session.merge(new_match)
    render_session.commit()
    print(f"   ✅ {len(matches)} partidos sincronizados (local: {local_count})")
    
    # 5. Predictions (depende de User y Match)
    print("5️⃣ Pronósticos...")
    local_count = local_session.query(Prediction).count()
    predictions = local_session.query(Prediction).all()
    for pred in predictions:
        new_pred = Prediction(
            id=pred.id,
            user_id=pred.user_id,
            match_id=pred.match_id,
            home_goals=pred.home_goals,
            away_goals=pred.away_goals,
            points_awarded=pred.points_awarded
        )
        render_session.merge(new_pred)
    render_session.commit()
    print(f"   ✅ {len(predictions)} pronósticos sincronizados (local: {local_count})")
    
    # 6. Comments (depende de User)
    print("6️⃣ Comentarios...")
    local_count = local_session.query(Comment).count()
    comments = local_session.query(Comment).all()
    for comment in comments:
        new_comment = Comment(
            id=comment.id,
            user_id=comment.user_id,
            content=comment.content,
            created_at=comment.created_at
        )
        render_session.merge(new_comment)
    render_session.commit()
    print(f"   ✅ {len(comments)} comentarios sincronizados (local: {local_count})")
    
    print("\n" + "=" * 60)
    print("✅ SINCRONIZACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📊 Resumen:")
    print(f"   • {len(allowed_emails)} emails permitidos")
    print(f"   • {len(users)} usuarios")
    print(f"   • {len(phases)} fases")
    print(f"   • {len(matches)} partidos")
    print(f"   • {len(predictions)} pronósticos")
    print(f"   • {len(comments)} comentarios")
    print("\n🌐 Los datos ahora están en Render")
    
except Exception as e:
    print(f"\n❌ ERROR durante la sincronización: {e}")
    import traceback
    traceback.print_exc()
    render_session.rollback()
    sys.exit(1)
finally:
    local_session.close()
    render_session.close()
