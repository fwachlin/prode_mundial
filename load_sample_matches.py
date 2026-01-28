from app import app, db
from models import Match, Phase
from datetime import datetime, timezone, timedelta

def load_sample_matches():
    """Cargar partidos de ejemplo para probar"""
    with app.app_context():
        # Verificar si ya hay partidos
        if Match.query.count() > 0:
            print("Ya hay partidos en la base de datos")
            return
        
        # Obtener Fecha 1
        phase_1 = Phase.query.filter_by(order=1).first()
        if not phase_1:
            print("❌ Fecha 1 no existe. Ejecuta: python init_phases.py")
            return
        
        # Fecha/hora de inicio: mañana a las 14:00 UTC
        base_time = datetime.now(timezone.utc).replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=1)
        
        # Lista de partidos de ejemplo (Grupo A, B, C, D)
        matches_data = [
            # Grupo A
            ("Qatar", "Ecuador", base_time),
            ("Senegal", "Holanda", base_time + timedelta(hours=3)),
            
            # Grupo B
            ("Inglaterra", "Irán", base_time + timedelta(hours=6)),
            ("EEUU", "Gales", base_time + timedelta(hours=9)),
            
            # Grupo C
            ("Argentina", "Arabia Saudita", base_time + timedelta(hours=12)),
            ("México", "Polonia", base_time + timedelta(hours=15)),
            
            # Grupo D
            ("Francia", "Dinamarca", base_time + timedelta(hours=18)),
            ("Perú", "Túnez", base_time + timedelta(hours=21)),
            
            # Grupo E
            ("España", "Costa Rica", base_time + timedelta(hours=24)),
            ("Alemania", "Japón", base_time + timedelta(hours=27)),
            
            # Grupo F
            ("Bélgica", "Canadá", base_time + timedelta(hours=30)),
            ("Marruecos", "Croacia", base_time + timedelta(hours=33)),
        ]
        
        created = 0
        for home, away, kickoff in matches_data:
            # Cierre 10 minutos antes del kickoff
            closes = kickoff - timedelta(minutes=10)
            
            match = Match(
                home_team=home,
                away_team=away,
                kickoff_at=kickoff,
                closes_at=closes,
                phase_id=phase_1.id
            )
            
            db.session.add(match)
            created += 1
        
        db.session.commit()
        
        print(f"✅ {created} partidos de ejemplo creados para {phase_1.name}")
        print("\nPartidos cargados:")
        for i, (home, away, kickoff) in enumerate(matches_data, 1):
            print(f"  {i}. {home} vs {away} - {kickoff.strftime('%Y-%m-%d %H:%M UTC')}")

if __name__ == '__main__':
    load_sample_matches()