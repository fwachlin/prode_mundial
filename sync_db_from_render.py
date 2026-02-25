"""
Sincronizar base de datos desde Render (PostgreSQL) a local (SQLite)
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import User, AllowedEmail, Phase, Match, Prediction, Comment

# Configuración
RENDER_DATABASE_URL = os.environ.get('DATABASE_URL')
if not RENDER_DATABASE_URL:
    print("❌ ERROR: Variable de entorno DATABASE_URL no encontrada")
    print("Configúrala con: $env:DATABASE_URL='postgresql://...'")
    sys.exit(1)

# Arreglar URL si es necesario (Render usa postgres:// pero SQLAlchemy requiere postgresql://)
if RENDER_DATABASE_URL.startswith('postgres://'):
    RENDER_DATABASE_URL = RENDER_DATABASE_URL.replace('postgres://', 'postgresql://', 1)

LOCAL_DB = 'sqlite:///instance/prode.db'

print("🔄 Conectando a Render PostgreSQL...")
render_engine = create_engine(RENDER_DATABASE_URL)
RenderSession = sessionmaker(bind=render_engine)

print("🔄 Conectando a SQLite local...")
local_engine = create_engine(LOCAL_DB)
LocalSession = sessionmaker(bind=local_engine)

# Crear todas las tablas en local si no existen
print("✅ Creando tablas locales...")
from models import User, AllowedEmail, Phase, Match, Prediction, Comment
from sqlalchemy import MetaData
metadata = MetaData()
User.__table__.create(local_engine, checkfirst=True)
AllowedEmail.__table__.create(local_engine, checkfirst=True)
Phase.__table__.create(local_engine, checkfirst=True)
Match.__table__.create(local_engine, checkfirst=True)
Prediction.__table__.create(local_engine, checkfirst=True)
Comment.__table__.create(local_engine, checkfirst=True)
print("✅ Tablas locales verificadas/creadas")

render_session = RenderSession()
local_session = LocalSession()

try:
    print("\n📊 Sincronizando datos...\n")
    
    # 1. AllowedEmail
    print("1️⃣ Emails permitidos...")
    local_session.query(AllowedEmail).delete()
    allowed_emails = render_session.query(AllowedEmail).all()
    for ae in allowed_emails:
        new_ae = AllowedEmail(id=ae.id, email=ae.email)
        local_session.merge(new_ae)
    local_session.commit()
    print(f"   ✅ {len(allowed_emails)} emails copiados")
    
    # 2. Users
    print("2️⃣ Usuarios...")
    local_session.query(User).delete()
    users = render_session.query(User).all()
    for user in users:
        new_user = User(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            is_admin=user.is_admin,
            is_enabled=user.is_enabled
        )
        local_session.merge(new_user)
    local_session.commit()
    print(f"   ✅ {len(users)} usuarios copiados")
    
    # 3. Phases
    print("3️⃣ Fases...")
    local_session.query(Phase).delete()
    phases = render_session.query(Phase).all()
    for phase in phases:
        new_phase = Phase(
            id=phase.id,
            name=phase.name,
            order=phase.order
        )
        local_session.merge(new_phase)
    local_session.commit()
    print(f"   ✅ {len(phases)} fases copiadas")
    
    # 4. Matches
    print("4️⃣ Partidos...")
    local_session.query(Match).delete()
    matches = render_session.query(Match).all()
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
        local_session.merge(new_match)
    local_session.commit()
    print(f"   ✅ {len(matches)} partidos copiados")
    
    # 5. Predictions
    print("5️⃣ Pronósticos...")
    local_session.query(Prediction).delete()
    predictions = render_session.query(Prediction).all()
    for pred in predictions:
        new_pred = Prediction(
            id=pred.id,
            user_id=pred.user_id,
            match_id=pred.match_id,
            home_goals=pred.home_goals,
            away_goals=pred.away_goals,
            points_awarded=pred.points_awarded
        )
        local_session.merge(new_pred)
    local_session.commit()
    print(f"   ✅ {len(predictions)} pronósticos copiados")
    
    # 6. Comments
    print("6️⃣ Comentarios...")
    local_session.query(Comment).delete()
    comments = render_session.query(Comment).all()
    for comment in comments:
        new_comment = Comment(
            id=comment.id,
            user_id=comment.user_id,
            content=comment.content,
            created_at=comment.created_at
        )
        local_session.merge(new_comment)
    local_session.commit()
    print(f"   ✅ {len(comments)} comentarios copiados")
    
    print("\n✅ ¡Sincronización completada exitosamente!")
    print(f"\nResumen:")
    print(f"  - {len(users)} usuarios")
    print(f"  - {len(matches)} partidos")
    print(f"  - {len(predictions)} pronósticos")
    print(f"  - {len(comments)} comentarios")
    print(f"  - {len(phases)} fases")
    print(f"  - {len(allowed_emails)} emails permitidos")

except Exception as e:
    print(f"\n❌ Error durante la sincronización: {e}")
    import traceback
    traceback.print_exc()
    local_session.rollback()
    sys.exit(1)
finally:
    render_session.close()
    local_session.close()
