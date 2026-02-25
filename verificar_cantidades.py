"""
📊 Verificar cantidades detalladas de datos
"""
from app import app
from models import User, Match, Prediction, Phase, AllowedEmail, Comment

with app.app_context():
    # Contar registros
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    regular_users = User.query.filter_by(is_admin=False).count()
    
    total_matches = Match.query.count()
    matches_with_result = Match.query.filter(Match.home_goals != None).count()
    matches_pending = Match.query.filter(Match.home_goals == None).count()
    
    total_predictions = Prediction.query.count()
    predictions_with_points = Prediction.query.filter(Prediction.points_awarded != None).count()
    predictions_pending = Prediction.query.filter(Prediction.points_awarded == None).count()
    
    total_phases = Phase.query.count()
    total_emails = AllowedEmail.query.count()
    total_comments = Comment.query.count()
    
    # Mostrar resultados
    print("=" * 80)
    print("📊 RESUMEN COMPLETO DE BASE DE DATOS")
    print("=" * 80)
    
    print(f"\n👥 USUARIOS:")
    print(f"   Total: {total_users}")
    print(f"   - Administradores: {admin_users}")
    print(f"   - Usuarios regulares: {regular_users}")
    
    print(f"\n⚽ PARTIDOS:")
    print(f"   Total: {total_matches}")
    print(f"   - Con resultado cargado: {matches_with_result}")
    print(f"   - Pendientes: {matches_pending}")
    
    # Partidos por fase
    print(f"\n   Distribución por fase:")
    for phase in Phase.query.order_by(Phase.order).all():
        count = Match.query.filter_by(phase_id=phase.id).count()
        print(f"   - {phase.name}: {count} partidos")
    
    print(f"\n🎲 PRONÓSTICOS:")
    print(f"   Total: {total_predictions}")
    print(f"   - Con puntos asignados: {predictions_with_points}")
    print(f"   - Pendientes (sin resultado): {predictions_pending}")
    
    # Pronósticos por usuario
    print(f"\n   Distribución por usuario:")
    for user in User.query.filter_by(is_admin=False).order_by(User.name).all():
        count = Prediction.query.filter_by(user_id=user.id).count()
        print(f"   - {user.name}: {count} pronósticos")
    
    print(f"\n📧 OTROS:")
    print(f"   - Fases: {total_phases}")
    print(f"   - Emails permitidos: {total_emails}")
    print(f"   - Comentarios: {total_comments}")
    
    # Cálculo de cobertura
    max_predictions = regular_users * total_matches
    coverage = (total_predictions / max_predictions * 100) if max_predictions > 0 else 0
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"   Pronósticos posibles: {max_predictions} ({regular_users} usuarios × {total_matches} partidos)")
    print(f"   Pronósticos realizados: {total_predictions}")
    print(f"   Cobertura: {coverage:.1f}%")
    
    print("\n" + "=" * 80)
    print("✅ Verificación completada")
    print("=" * 80 + "\n")
