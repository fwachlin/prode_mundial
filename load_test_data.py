from app import app, db
from models import Match, Prediction, User, Phase, AllowedEmail
from datetime import datetime, timezone, timedelta

def load_test_data():
    """Cargar datos de prueba completos"""
    with app.app_context():
        # Limpiar datos anteriores
        print("🧹 Limpiando datos anteriores...")
        Match.query.delete()
        Prediction.query.delete()
        User.query.filter(User.email != 'admin@prode.com').delete()
        db.session.commit()
        
        # Obtener Fecha 1
        phase_1 = Phase.query.filter_by(order=1).first()
        
        # Fecha base: ayer a las 14:00 UTC (partidos ya pasados)
        base_time = datetime.now(timezone.utc).replace(hour=14, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        # Crear partidos con resultados ya cargados
        matches_data = [
            ("Qatar", "Ecuador", base_time, 0, 2),
            ("Senegal", "Holanda", base_time + timedelta(hours=3), 0, 2),
            ("Inglaterra", "Irán", base_time + timedelta(hours=6), 6, 2),
            ("EEUU", "Gales", base_time + timedelta(hours=9), 1, 1),
            ("Argentina", "Arabia Saudita", base_time + timedelta(hours=12), 1, 2),
            ("México", "Polonia", base_time + timedelta(hours=15), 0, 0),
            ("Francia", "Dinamarca", base_time + timedelta(hours=18), 4, 1),
            ("Perú", "Túnez", base_time + timedelta(hours=21), 0, 1),
            ("España", "Costa Rica", base_time + timedelta(hours=24), 7, 0),
            ("Alemania", "Japón", base_time + timedelta(hours=27), 1, 2),
            ("Bélgica", "Canadá", base_time + timedelta(hours=30), 1, 0),
            ("Marruecos", "Croacia", base_time + timedelta(hours=33), 0, 0),
        ]
        
        print("📋 Creando partidos...")
        matches = []
        for home, away, kickoff, home_goals, away_goals in matches_data:
            closes = kickoff - timedelta(minutes=10)
            match = Match(
                home_team=home,
                away_team=away,
                kickoff_at=kickoff,
                closes_at=closes,
                phase_id=phase_1.id,
                home_goals=home_goals,
                away_goals=away_goals
            )
            db.session.add(match)
            matches.append(match)
        
        db.session.commit()
        print(f"✅ {len(matches)} partidos creados con resultados")
        
        # Crear usuarios ficticios
        print("\n👥 Creando usuarios ficticios...")
        users_emails = [
            'juan@prode.com',
            'maria@prode.com',
            'carlos@prode.com',
            'ana@prode.com',
            'luis@prode.com',
        ]
        
        # Agregar emails a la lista de permitidos
        for email in users_emails:
            if not AllowedEmail.query.filter_by(email=email).first():
                db.session.add(AllowedEmail(email=email))
        db.session.commit()
        
        # Crear usuarios
        users = []
        for i, email in enumerate(users_emails, 1):
            if User.query.filter_by(email=email).first():
                continue
            
            user = User(
                name=f'Usuario {i}',
                email=email,
                is_admin=False,
                is_enabled=True
            )
            user.set_password('password123')
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"✅ {len(users)} usuarios creados")
        
        # Crear pronósticos variados para cada usuario
        print("\n🎯 Creando pronósticos...")
        
        predictions_created = 0
        for user_idx, user in enumerate(users):
            for match_idx, match in enumerate(matches):
                # Cada usuario tiene diferentes patrones de predicción
                # para que los puntajes varíen
                pattern = (user_idx + match_idx) % 4
                
                if pattern == 0:
                    # Acertar exacto (resultado + score)
                    home_pred = match.home_goals
                    away_pred = match.away_goals
                elif pattern == 1:
                    # Acertar ganador pero no score (diferencia pequeña)
                    if match.home_goals > match.away_goals:
                        home_pred = match.home_goals + 1
                        away_pred = match.away_goals
                    elif match.away_goals > match.home_goals:
                        home_pred = match.home_goals
                        away_pred = match.away_goals + 1
                    else:
                        home_pred = match.home_goals + 1
                        away_pred = match.away_goals
                elif pattern == 2:
                    # Acertar ganador pero con diferencia grande
                    if match.home_goals > match.away_goals:
                        home_pred = match.home_goals + 2
                        away_pred = match.away_goals - 1
                    elif match.away_goals > match.home_goals:
                        home_pred = match.home_goals - 1
                        away_pred = match.away_goals + 2
                    else:
                        home_pred = match.home_goals + 2
                        away_pred = match.away_goals + 1
                else:
                    # Errar completamente el resultado
                    home_pred = (match.home_goals + 2) % 6
                    away_pred = (match.away_goals + 3) % 6
                
                prediction = Prediction(
                    user_id=user.id,
                    match_id=match.id,
                    home_goals=max(0, home_pred),  # ← Asegurar que no sean negativos
                    away_goals=max(0, away_pred)   # ← Asegurar que no sean negativos
                )
                
                db.session.add(prediction)
                predictions_created += 1
        
        # ← IMPORTANTE: Commit ANTES de calcular puntos
        db.session.commit()
        
        # Ahora calcular puntos (después del commit)
        for prediction in Prediction.query.all():
            prediction.points_awarded = prediction.calculate_points()
        
        db.session.commit()
        print(f"✅ {predictions_created} pronósticos creados y puntos calculados")
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("📊 RESUMEN DE DATOS DE PRUEBA")
        print("="*60)
        print(f"\n👤 Admin:")
        print(f"   Email: admin@prode.com")
        print(f"   Contraseña: admin123")
        
        print(f"\n👥 Usuarios ficticios:")
        for email in users_emails:
            print(f"   Email: {email}")
            print(f"   Contraseña: password123")
        
        print(f"\n📋 Partidos: {len(matches)} (todos con resultados)")
        print(f"🎯 Pronósticos: {predictions_created}")
        
        # Mostrar puntajes por usuario
        print(f"\n🏆 Puntajes por usuario (RANKING):")
        user_scores = []
        for user in User.query.filter(User.is_admin == False).all():
            total_points = sum(p.points_awarded or 0 for p in user.predictions)
            user_scores.append((user.name, total_points))
        
        # Ordenar por puntos descendente
        user_scores.sort(key=lambda x: x[1], reverse=True)
        for i, (name, points) in enumerate(user_scores, 1):
            print(f"   {i}. {name}: {points} puntos")

if __name__ == '__main__':
    load_test_data()