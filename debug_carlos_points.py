"""
Debug del cálculo de puntos de Carlos López
"""
from app import app
from models import db, User, Match, Prediction

with app.app_context():
    # Buscar Carlos López
    carlos = User.query.filter_by(name='Carlos López').first()
    
    if not carlos:
        print("❌ Carlos López no encontrado")
        print("Usuarios disponibles:")
        for user in User.query.all():
            print(f"  - {user.name} ({user.email})")
    else:
        print(f"✅ Usuario encontrado: {carlos.name} (ID: {carlos.id})")
        
        # Buscar sus pronósticos con resultado cargado
        predictions = Prediction.query.filter_by(user_id=carlos.id).join(Match).filter(
            Match.home_goals.isnot(None),
            Match.away_goals.isnot(None)
        ).all()
        
        print(f"\n📊 Pronósticos con resultado cargado: {len(predictions)}")
        
        for pred in predictions:
            match = pred.match
            print(f"\n{'='*80}")
            print(f"🏆 Partido #{match.id}: {match.home_team} vs {match.away_team}")
            print(f"   Resultado real: {match.home_goals}-{match.away_goals}")
            print(f"   Pronóstico: {pred.home_goals}-{pred.away_goals}")
            print(f"   Puntos otorgados por sistema: {pred.points_awarded}")
            
            # Calcular componentes manualmente
            print(f"\n🔍 DESGLOSE DE PUNTOS:")
            
            # 1. Ganador/Empate
            match_result = 'draw' if match.home_goals == match.away_goals else ('home' if match.home_goals > match.away_goals else 'away')
            user_result = 'draw' if pred.home_goals == pred.away_goals else ('home' if pred.home_goals > pred.away_goals else 'away')
            acerto_ganador = (user_result == match_result)
            
            print(f"   1️⃣ Ganador/Empate:")
            print(f"      Resultado real: {match_result}")
            print(f"      Pronóstico: {user_result}")
            print(f"      Acertó: {'✅ SÍ' if acerto_ganador else '❌ NO'}")
            print(f"      Puntos: {10 if acerto_ganador else 0}")
            
            if not acerto_ganador:
                print(f"\n   ❌ No acertó ganador → 0 puntos totales")
                continue
            
            # 2. Batacazo
            total_participants = User.query.filter_by(is_admin=False).count()
            correct_predictions = Prediction.query.filter_by(match_id=match.id).join(User).filter(
                User.is_admin == False
            ).all()
            
            correct_count = 0
            for p in correct_predictions:
                p_result = 'draw' if p.home_goals == p.away_goals else ('home' if p.home_goals > p.away_goals else 'away')
                if p_result == match_result:
                    correct_count += 1
            
            correct_percentage = (correct_count / total_participants * 100) if total_participants > 0 else 100
            
            batacazo_points = 0
            if correct_percentage < 5:
                batacazo_points = 5
            elif correct_percentage < 10:
                batacazo_points = 4
            elif correct_percentage < 15:
                batacazo_points = 3
            elif correct_percentage < 20:
                batacazo_points = 2
            elif correct_percentage < 25:
                batacazo_points = 1
            
            print(f"\n   2️⃣ Batacazo:")
            print(f"      Total participantes (no admins): {total_participants}")
            print(f"      Acertaron ganador: {correct_count}")
            print(f"      Porcentaje: {correct_percentage:.2f}%")
            print(f"      Puntos bonus: {batacazo_points}")
            
            # 3. Score
            if pred.home_goals == match.home_goals and pred.away_goals == match.away_goals:
                score_points = 5
                print(f"\n   3️⃣ Score:")
                print(f"      ✅ EXACTO: {pred.home_goals}-{pred.away_goals}")
                print(f"      Puntos: 5")
            else:
                total_diff = abs(pred.home_goals - match.home_goals) + abs(pred.away_goals - match.away_goals)
                score_points = max(0, 5 - total_diff)
                print(f"\n   3️⃣ Score:")
                print(f"      Diferencia en goles: {total_diff}")
                print(f"      Puntos: {score_points}")
            
            # Total manual
            total_manual = 10 + batacazo_points + score_points
            
            print(f"\n📊 RESUMEN:")
            print(f"   Ganador:  10 puntos")
            print(f"   Batacazo: {batacazo_points:2d} puntos")
            print(f"   Score:    {score_points:2d} puntos")
            print(f"   ─────────────────")
            print(f"   TOTAL MANUAL:  {total_manual} puntos")
            print(f"   TOTAL SISTEMA: {pred.points_awarded} puntos")
            
            if total_manual != pred.points_awarded:
                print(f"\n   ⚠️ DISCREPANCIA: {total_manual - pred.points_awarded} puntos")
            else:
                print(f"\n   ✅ CÁLCULO CORRECTO")
