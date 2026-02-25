"""
⬆️ SUBIR BASE DE DATOS LOCAL A RENDER
Sincronización: SQLite Local → PostgreSQL Render

ADVERTENCIA: Esto BORRARÁ todos los datos actuales en Render
            y los reemplazará con los datos locales.

Ejecutar: python upload_to_render.py
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
    print("\nConfigúrala con:")
    print("  $env:DATABASE_URL='postgresql://...'")
    print("\nObtén la URL desde Render Dashboard → PostgreSQL → Connect")
    sys.exit(1)

# Arreglar URL si es necesario
if RENDER_DATABASE_URL.startswith('postgres://'):
    RENDER_DATABASE_URL = RENDER_DATABASE_URL.replace('postgres://', 'postgresql://', 1)

LOCAL_DB = 'sqlite:///instance/prode.db'

print("=" * 80)
print("⬆️  SUBIR BASE DE DATOS LOCAL A RENDER")
print("=" * 80)

# Verificar base de datos local existe
if not os.path.exists('instance/prode.db'):
    print("\n❌ ERROR: No se encuentra instance/prode.db")
    print("No hay datos locales para subir.")
    sys.exit(1)

# Conectar a ambas bases
print("\n🔄 Conectando a bases de datos...")
local_engine = create_engine(LOCAL_DB)
LocalSession = sessionmaker(bind=local_engine)
local_session = LocalSession()

render_engine = create_engine(RENDER_DATABASE_URL)
RenderSession = sessionmaker(bind=render_engine)
render_session = RenderSession()

try:
    # Verificar conexión a Render
    from sqlalchemy import text
    render_session.execute(text('SELECT 1'))
    print("✅ Conexión a Render OK")
    
    # Contar registros en local
    print("\n📊 Datos en base LOCAL:")
    local_users = local_session.query(User).count()
    local_emails = local_session.query(AllowedEmail).count()
    local_phases = local_session.query(Phase).count()
    local_matches = local_session.query(Match).count()
    local_predictions = local_session.query(Prediction).count()
    local_comments = local_session.query(Comment).count()
    
    print(f"   - {local_users} usuarios")
    print(f"   - {local_emails} emails permitidos")
    print(f"   - {local_phases} fases")
    print(f"   - {local_matches} partidos")
    print(f"   - {local_predictions} pronósticos")
    print(f"   - {local_comments} comentarios")
    
    if local_users == 0 and local_matches == 0:
        print("\n⚠️  Base de datos local parece vacía. ¿Seguro quieres continuar?")
        respuesta = input("Escribe 'SI' para continuar: ")
        if respuesta != 'SI':
            print("❌ Operación cancelada")
            sys.exit(0)
    
    # CONFIRMACIÓN CRÍTICA
    print("\n" + "=" * 80)
    print("⚠️  ADVERTENCIA CRÍTICA")
    print("=" * 80)
    print("Esta operación va a:")
    print("  1. BORRAR todos los datos actuales en Render")
    print("  2. SUBIR los datos de tu base local a Render")
    print("\nEsto afectará a todos los usuarios conectados a producción.")
    print("=" * 80)
    
    confirmacion = input("\n¿Estás SEGURO? Escribe 'CONFIRMAR' para continuar: ")
    
    if confirmacion != 'CONFIRMAR':
        print("\n❌ Operación cancelada por el usuario")
        print("No se realizaron cambios en Render.")
        sys.exit(0)
    
    print("\n🔄 Iniciando sincronización...")
    
    # PASO 1: Limpiar Render (respetar orden de foreign keys)
    print("\n[1/7] 🗑️  Limpiando datos en Render...")
    render_session.query(Comment).delete()
    render_session.query(Prediction).delete()
    render_session.query(Match).delete()
    render_session.query(Phase).delete()
    render_session.query(User).delete()
    render_session.query(AllowedEmail).delete()
    render_session.commit()
    print("✅ Datos antiguos eliminados")
    
    # PASO 2: Copiar AllowedEmail
    print("\n[2/7] 📧 Copiando emails permitidos...")
    allowed_emails = local_session.query(AllowedEmail).all()
    for ae in allowed_emails:
        new_ae = AllowedEmail(id=ae.id, email=ae.email)
        render_session.merge(new_ae)
    render_session.commit()
    print(f"✅ {len(allowed_emails)} emails copiados")
    
    # PASO 3: Copiar Users
    print("\n[3/7] 👥 Copiando usuarios...")
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
    print(f"✅ {len(users)} usuarios copiados")
    
    # PASO 4: Copiar Phases
    print("\n[4/7] 📅 Copiando fases...")
    phases = local_session.query(Phase).all()
    for phase in phases:
        new_phase = Phase(
            id=phase.id,
            name=phase.name,
            order=phase.order
        )
        render_session.merge(new_phase)
    render_session.commit()
    print(f"✅ {len(phases)} fases copiadas")
    
    # PASO 5: Copiar Matches
    print("\n[5/7] ⚽ Copiando partidos...")
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
    print(f"✅ {len(matches)} partidos copiados")
    
    # PASO 6: Copiar Predictions
    print("\n[6/7] 🎲 Copiando pronósticos...")
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
    print(f"✅ {len(predictions)} pronósticos copiados")
    
    # PASO 7: Copiar Comments
    print("\n[7/7] 💬 Copiando comentarios...")
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
    print(f"✅ {len(comments)} comentarios copiados")
    
    # Verificar en Render
    print("\n📊 Verificando datos en Render...")
    render_users = render_session.query(User).count()
    render_matches = render_session.query(Match).count()
    render_predictions = render_session.query(Prediction).count()
    
    print(f"   - {render_users} usuarios")
    print(f"   - {render_matches} partidos")
    print(f"   - {render_predictions} pronósticos")
    
    print("\n" + "=" * 80)
    print("✅ SINCRONIZACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print("\n📊 Resumen:")
    print(f"   Local → Render:")
    print(f"   - {len(users)} usuarios")
    print(f"   - {len(allowed_emails)} emails permitidos")
    print(f"   - {len(phases)} fases")
    print(f"   - {len(matches)} partidos")
    print(f"   - {len(predictions)} pronósticos")
    print(f"   - {len(comments)} comentarios")
    
    print("\n💡 Próximos pasos:")
    print("   1. Verifica que Render se haya reiniciado (puede tomar 1-2 min)")
    print("   2. Abre tu sitio web en producción")
    print("   3. Verifica que los datos estén correctos")
    print("=" * 80 + "\n")

except Exception as e:
    print(f"\n❌ Error durante la sincronización: {e}")
    import traceback
    traceback.print_exc()
    render_session.rollback()
    print("\n⚠️  Se revirtieron los cambios en Render")
    sys.exit(1)
finally:
    local_session.close()
    render_session.close()
