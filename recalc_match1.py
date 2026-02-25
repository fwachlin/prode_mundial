"""
Recalcular puntos del partido MEX vs RSA
"""
from app import app
from models import db, Match

with app.app_context():
    match = Match.query.get(1)  # MEX vs RSA
    
    print(f"🏆 Partido: {match.home_team} vs {match.away_team}")
    print(f"   Resultado: {match.home_goals}-{match.away_goals}")
    print(f"\n🔄 Recalculando puntos de {len(match.predictions)} pronósticos...")
    
    for prediction in match.predictions:
        old_points = prediction.points_awarded
        prediction.points_awarded = prediction.calculate_points()
        new_points = prediction.points_awarded
        
        user_name = prediction.user.name
        change = '=' if old_points == new_points else f"+{new_points - old_points}" if new_points > old_points else f"{new_points - old_points}"
        
        print(f"   {user_name}: {old_points} → {new_points} ({change})")
    
    db.session.commit()
    print(f"\n✅ Puntos recalculados y guardados")
