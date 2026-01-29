from app import app
from extensions import db
from models import User, Match, Prediction
import random

def create_predictions():
    """Crear pronósticos aleatorios para todos los usuarios en todos los partidos"""
    
    with app.app_context():
        users = User.query.filter_by(is_admin=False).all()
        matches = Match.query.all()
        
        if not users:
            print("❌ No hay usuarios en la base de datos")
            return
        
        if not matches:
            print("❌ No hay partidos en la base de datos")
            return
        
        created = 0
        skipped = 0
        
        print(f"👥 Usuarios encontrados: {len(users)}")
        print(f"⚽ Partidos encontrados: {len(matches)}")
        print(f"\n🎲 Generando pronósticos aleatorios...\n")
        
        for user in users:
            user_predictions = 0
            
            for match in matches:
                # Verificar si ya existe un pronóstico
                existing = Prediction.query.filter_by(
                    user_id=user.id,
                    match_id=match.id
                ).first()
                
                if existing:
                    skipped += 1
                    continue
                
                # Solo crear pronóstico si el partido aún no cerró
                if match.is_open():
                    # Generar resultado aleatorio (favoreciendo resultados realistas)
                    home_goals = random.choices([0, 1, 2, 3, 4], weights=[10, 30, 35, 20, 5])[0]
                    away_goals = random.choices([0, 1, 2, 3, 4], weights=[10, 30, 35, 20, 5])[0]
                    
                    prediction = Prediction(
                        user_id=user.id,
                        match_id=match.id,
                        home_goals=home_goals,
                        away_goals=away_goals
                    )
                    
                    db.session.add(prediction)
                    created += 1
                    user_predictions += 1
            
            print(f"✅ {user.name}: {user_predictions} pronósticos creados")
        
        db.session.commit()
        
        print(f"\n📊 Resumen Final:")
        print(f"   ✅ Pronósticos creados: {created}")
        print(f"   ⚠️  Ya existían: {skipped}")
        print(f"\n🎉 Listo! Ahora puedes probar el sistema de rankings y comparaciones")

if __name__ == '__main__':
    create_predictions()