"""
Debug detallado del batacazo
"""
from app import app
from models import db, User, Match, Prediction

with app.app_context():
    match_id = 1  # MEX vs RSA
    match = Match.query.get(match_id)
    
    print(f"🏆 Partido #{match.id}: {match.home_team} vs {match.away_team}")
    print(f"   Resultado: {match.home_goals}-{match.away_goals}")
    
    match_result = 'draw' if match.home_goals == match.away_goals else ('home' if match.home_goals > match.away_goals else 'away')
    print(f"   Ganador: {match_result}")
    
    # Total participantes (no admin)
    total_participants = User.query.filter_by(is_admin=False).count()
    print(f"\n👥 Total participantes (no admin): {total_participants}")
    
    # TODAS las predicciones (lo que hace el código actual)
    print(f"\n❌ CÓDIGO ACTUAL (BUGUEADO):")
    all_predictions = Prediction.query.filter_by(match_id=match.id).all()
    print(f"   Total predicciones consultadas: {len(all_predictions)}")
    
    for pred in all_predictions:
        user = User.query.get(pred.user_id)
        pred_result = 'draw' if pred.home_goals == pred.away_goals else ('home' if pred.home_goals > pred.away_goals else 'away')
        acerto = '✅' if pred_result == match_result else '❌'
        admin_flag = '🔴 ADMIN' if user.is_admin else ''
        print(f"   {acerto} {user.name}: {pred.home_goals}-{pred.away_goals} → {pred_result} {admin_flag}")
    
    correct_count_buggy = sum(1 for p in all_predictions 
                               if ('draw' if p.home_goals == p.away_goals 
                                   else ('home' if p.home_goals > p.away_goals else 'away')) == match_result)
    percentage_buggy = (correct_count_buggy / total_participants) * 100
    
    print(f"\n   Acertaron ganador: {correct_count_buggy}")
    print(f"   Porcentaje (buggy): {correct_count_buggy}/{total_participants} = {percentage_buggy:.2f}%")
    
    if percentage_buggy < 5:
        bonus_buggy = 5
    elif percentage_buggy < 10:
        bonus_buggy = 4
    elif percentage_buggy < 15:
        bonus_buggy = 3
    elif percentage_buggy < 20:
        bonus_buggy = 2
    elif percentage_buggy < 25:
        bonus_buggy = 1
    else:
        bonus_buggy = 0
    
    print(f"   Bonus batacazo (buggy): {bonus_buggy} puntos")
    
    # PREDICCIONES CORRECTAS (sin admin)
    print(f"\n✅ CÓDIGO CORRECTO (sin admin):")
    non_admin_predictions = Prediction.query.filter_by(match_id=match.id).join(User).filter(
        User.is_admin == False
    ).all()
    print(f"   Total predicciones (solo no-admin): {len(non_admin_predictions)}")
    
    for pred in non_admin_predictions:
        user = User.query.get(pred.user_id)
        pred_result = 'draw' if pred.home_goals == pred.away_goals else ('home' if pred.home_goals > pred.away_goals else 'away')
        acerto = '✅' if pred_result == match_result else '❌'
        print(f"   {acerto} {user.name}: {pred.home_goals}-{pred.away_goals} → {pred_result}")
    
    correct_count_fixed = sum(1 for p in non_admin_predictions 
                              if ('draw' if p.home_goals == p.away_goals 
                                  else ('home' if p.home_goals > p.away_goals else 'away')) == match_result)
    percentage_fixed = (correct_count_fixed / total_participants) * 100
    
    print(f"\n   Acertaron ganador: {correct_count_fixed}")
    print(f"   Porcentaje (correcto): {correct_count_fixed}/{total_participants} = {percentage_fixed:.2f}%")
    
    if percentage_fixed < 5:
        bonus_fixed = 5
    elif percentage_fixed < 10:
        bonus_fixed = 4
    elif percentage_fixed < 15:
        bonus_fixed = 3
    elif percentage_fixed < 20:
        bonus_fixed = 2
    elif percentage_fixed < 25:
        bonus_fixed = 1
    else:
        bonus_fixed = 0
    
    print(f"   Bonus batacazo (correcto): {bonus_fixed} puntos")
    
    print(f"\n📊 COMPARACIÓN:")
    print(f"   Sistema actual: 10 (ganador) + {bonus_buggy} (batacazo) + 5 (score) = {10 + bonus_buggy + 5} puntos")
    print(f"   Sistema correcto: 10 (ganador) + {bonus_fixed} (batacazo) + 5 (score) = {10 + bonus_fixed + 5} puntos")
    print(f"   Diferencia: {bonus_fixed - bonus_buggy} punto(s)")
