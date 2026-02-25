"""
🎯 SCRIPT COMPLETO DE GENERACIÓN DE DATOS FICTICIOS
Genera base de datos completa con:
- 4 fases
- 104 partidos del Mundial 2026
- 11 usuarios ficticios
- Pronósticos variados para fechas 1, 2, y 3 (con algunos sin hacer)
"""

from datetime import datetime, timezone, timedelta
from app import app
from extensions import db
from models import User, Phase, Match, Prediction, AllowedEmail
import random

# Nombres ficticios realistas
USUARIOS_FICTICIOS = [
    ("Ana Martínez", "ana.martinez@prode.com"),
    ("Carlos López", "carlos.lopez@prode.com"),
    ("Diego Sánchez", "diego.sanchez@prode.com"),
    ("Elena Ruiz", "elena.ruiz@prode.com"),
    ("Fernando Torres", "fernando.torres@prode.com"),
    ("Gabriela Díaz", "gabriela.diaz@prode.com"),
    ("Javier Morales", "javier.morales@prode.com"),
    ("Laura Fernández", "laura.fernandez@prode.com"),
    ("María García", "maria.garcia@prode.com"),
    ("Miguel Torres", "miguel.torres@prode.com"),
    ("Pedro Rodríguez", "pedro.rodriguez@prode.com"),
]

# Partidos del Mundial 2026 (104 partidos)
PARTIDOS_MUNDIAL_2026 = [
    # ============================================
    # FECHA 1 - Primera jornada (24 partidos)
    # ============================================
    (1, "MEX", "RSA", "2026-06-11 19:00"),
    (1, "KOR", "POL", "2026-06-12 02:00"),
    (1, "CAN", "WAL", "2026-06-12 19:00"),
    (1, "QAT", "SUI", "2026-06-13 19:00"),
    (1, "BRA", "MAR", "2026-06-13 22:00"),
    (1, "HAI", "SCO", "2026-06-14 01:00"),
    (1, "USA", "PAR", "2026-06-13 01:00"),
    (1, "AUS", "ITA", "2026-06-14 04:00"),
    (1, "GER", "CUW", "2026-06-14 17:00"),
    (1, "CIV", "ECU", "2026-06-14 23:00"),
    (1, "NED", "JPN", "2026-06-14 20:00"),
    (1, "DEN", "TUN", "2026-06-15 02:00"),
    (1, "BEL", "EGY", "2026-06-15 19:00"),
    (1, "IRN", "NZL", "2026-06-16 01:00"),
    (1, "ESP", "CPV", "2026-06-15 16:00"),
    (1, "KSA", "URU", "2026-06-15 22:00"),
    (1, "FRA", "SEN", "2026-06-16 19:00"),
    (1, "CHN", "NOR", "2026-06-16 22:00"),
    (1, "ARG", "ALG", "2026-06-17 01:00"),
    (1, "AUT", "JOR", "2026-06-17 04:00"),
    (1, "POR", "CRC", "2026-06-17 17:00"),
    (1, "UZB", "COL", "2026-06-18 02:00"),
    (1, "ENG", "CRO", "2026-06-17 20:00"),
    (1, "GHA", "PAN", "2026-06-17 23:00"),
    
    # ============================================
    # FECHA 2 - Segunda jornada (24 partidos)
    # ============================================
    (2, "POL", "RSA", "2026-06-18 16:00"),
    (2, "MEX", "KOR", "2026-06-19 01:00"),
    (2, "SUI", "WAL", "2026-06-19 19:00"),
    (2, "CAN", "QAT", "2026-06-20 01:00"),
    (2, "SCO", "MAR", "2026-06-19 22:00"),
    (2, "BRA", "HAI", "2026-06-20 04:00"),
    (2, "ITA", "PAR", "2026-06-20 19:00"),
    (2, "USA", "AUS", "2026-06-21 01:00"),
    (2, "ECU", "CUW", "2026-06-20 16:00"),
    (2, "GER", "CIV", "2026-06-20 22:00"),
    (2, "TUN", "JPN", "2026-06-21 19:00"),
    (2, "NED", "DEN", "2026-06-22 01:00"),
    (2, "NZL", "EGY", "2026-06-21 16:00"),
    (2, "BEL", "IRN", "2026-06-21 22:00"),
    (2, "URU", "CPV", "2026-06-22 19:00"),
    (2, "ESP", "KSA", "2026-06-23 01:00"),
    (2, "NOR", "SEN", "2026-06-22 16:00"),
    (2, "FRA", "CHN", "2026-06-22 22:00"),
    (2, "JOR", "ALG", "2026-06-23 19:00"),
    (2, "ARG", "AUT", "2026-06-24 01:00"),
    (2, "COL", "CRC", "2026-06-23 16:00"),
    (2, "POR", "UZB", "2026-06-23 22:00"),
    (2, "PAN", "CRO", "2026-06-24 19:00"),
    (2, "ENG", "GHA", "2026-06-25 01:00"),
    
    # ============================================
    # FECHA 3 - Tercera jornada (24 partidos)
    # ============================================
    (3, "RSA", "KOR", "2026-06-25 19:00"),
    (3, "POL", "MEX", "2026-06-25 19:00"),
    (3, "WAL", "QAT", "2026-06-26 19:00"),
    (3, "SUI", "CAN", "2026-06-26 19:00"),
    (3, "MAR", "HAI", "2026-06-27 19:00"),
    (3, "SCO", "BRA", "2026-06-27 19:00"),
    (3, "PAR", "AUS", "2026-06-28 19:00"),
    (3, "ITA", "USA", "2026-06-28 19:00"),
    (3, "CUW", "CIV", "2026-06-29 19:00"),
    (3, "ECU", "GER", "2026-06-29 19:00"),
    (3, "JPN", "DEN", "2026-06-30 19:00"),
    (3, "TUN", "NED", "2026-06-30 19:00"),
    (3, "EGY", "IRN", "2026-07-01 19:00"),
    (3, "NZL", "BEL", "2026-07-01 19:00"),
    (3, "CPV", "KSA", "2026-07-02 19:00"),
    (3, "URU", "ESP", "2026-07-02 19:00"),
    (3, "SEN", "CHN", "2026-07-03 19:00"),
    (3, "NOR", "FRA", "2026-07-03 19:00"),
    (3, "ALG", "AUT", "2026-07-04 19:00"),
    (3, "JOR", "ARG", "2026-07-04 19:00"),
    (3, "CRC", "UZB", "2026-07-05 19:00"),
    (3, "COL", "POR", "2026-07-05 19:00"),
    (3, "CRO", "GHA", "2026-07-06 19:00"),
    (3, "PAN", "ENG", "2026-07-06 19:00"),
    
    # ============================================
    # FECHA 4 - Eliminación Directa (32 partidos)
    # ============================================
    # Octavos de Final (16 partidos)
    (4, "1A", "2B", "2026-07-11 19:00"),
    (4, "1B", "2A", "2026-07-12 01:00"),
    (4, "1C", "2D", "2026-07-12 19:00"),
    (4, "1D", "2C", "2026-07-13 01:00"),
    (4, "1E", "2F", "2026-07-13 19:00"),
    (4, "1F", "2E", "2026-07-14 01:00"),
    (4, "1G", "2H", "2026-07-14 19:00"),
    (4, "1H", "2G", "2026-07-15 01:00"),
    (4, "1I", "2J", "2026-07-15 19:00"),
    (4, "1J", "2I", "2026-07-16 01:00"),
    (4, "1K", "2L", "2026-07-16 19:00"),
    (4, "1L", "2K", "2026-07-17 01:00"),
    (4, "3A/B/C", "3D/E/F", "2026-07-17 19:00"),
    (4, "3D/E/F", "3A/B/C", "2026-07-18 01:00"),
    (4, "3G/H/I", "3J/K/L", "2026-07-18 19:00"),
    (4, "3J/K/L", "3G/H/I", "2026-07-19 01:00"),
    
    # Cuartos de Final (8 partidos)
    (4, "W1", "W2", "2026-07-23 19:00"),
    (4, "W3", "W4", "2026-07-24 01:00"),
    (4, "W5", "W6", "2026-07-24 19:00"),
    (4, "W7", "W8", "2026-07-25 01:00"),
    (4, "W9", "W10", "2026-07-25 19:00"),
    (4, "W11", "W12", "2026-07-26 01:00"),
    (4, "W13", "W14", "2026-07-26 19:00"),
    (4, "W15", "W16", "2026-07-27 01:00"),
    
    # Semifinales (4 partidos)
    (4, "W17", "W18", "2026-07-30 01:00"),
    (4, "W19", "W20", "2026-07-31 01:00"),
    (4, "W21", "W22", "2026-08-01 01:00"),
    (4, "W23", "W24", "2026-08-02 01:00"),
    
    # Tercer Puesto (2 partidos)
    (4, "L25", "L26", "2026-08-05 19:00"),
    (4, "L27", "L28", "2026-08-06 19:00"),
    
    # Final (2 partidos)
    (4, "W25", "W26", "2026-08-08 19:00"),
    (4, "W27", "W28", "2026-08-09 19:00"),
]

def generar_pronostico_realista():
    """Generar un pronóstico aleatorio con distribución realista"""
    # Distribución más realista de goles
    home_goals = random.choices([0, 1, 2, 3, 4, 5], weights=[15, 30, 25, 15, 10, 5])[0]
    away_goals = random.choices([0, 1, 2, 3, 4, 5], weights=[15, 30, 25, 15, 10, 5])[0]
    return home_goals, away_goals

def main():
    with app.app_context():
        print("\n" + "="*80)
        print("🎯 GENERACIÓN COMPLETA DE BASE DE DATOS FICTICIA")
        print("="*80)
        
        # PASO 1: Limpiar base de datos (excepto admin)
        print("\n[1/6] 🗑️  Limpiando datos anteriores...")
        Prediction.query.delete()
        Match.query.delete()
        Phase.query.delete()
        User.query.filter_by(is_admin=False).delete()
        AllowedEmail.query.delete()
        db.session.commit()
        print("✅ Base de datos limpiada")
        
        # PASO 2: Crear fases
        print("\n[2/6] 📅 Creando 4 fases...")
        fases = [
            Phase(name="Fecha 1", order=1),
            Phase(name="Fecha 2", order=2),
            Phase(name="Fecha 3", order=3),
            Phase(name="Fecha 4 - Eliminación Directa", order=4)
        ]
        for fase in fases:
            db.session.add(fase)
        db.session.commit()
        print(f"✅ {len(fases)} fases creadas")
        
        # PASO 3: Crear usuarios ficticios
        print(f"\n[3/6] 👥 Creando {len(USUARIOS_FICTICIOS)} usuarios ficticios...")
        usuarios = []
        for nombre, email in USUARIOS_FICTICIOS:
            # Crear email permitido
            allowed = AllowedEmail(email=email)
            db.session.add(allowed)
            
            # Crear usuario
            user = User(name=nombre, email=email, is_admin=False)
            user.set_password("prode123")  # Misma contraseña para todos
            db.session.add(user)
            usuarios.append(user)
        
        db.session.commit()
        print(f"✅ {len(usuarios)} usuarios creados (contraseña: prode123)")
        
        # PASO 4: Crear partidos
        print(f"\n[4/6] ⚽ Creando {len(PARTIDOS_MUNDIAL_2026)} partidos...")
        partidos = []
        for phase_id, home, away, fecha_str in PARTIDOS_MUNDIAL_2026:
            # Parsear fecha
            kickoff_at = datetime.fromisoformat(fecha_str).replace(tzinfo=timezone.utc)
            closes_at = kickoff_at - timedelta(minutes=10)
            
            match = Match(
                home_team=home,
                away_team=away,
                kickoff_at=kickoff_at,
                closes_at=closes_at,
                phase_id=phase_id
            )
            db.session.add(match)
            partidos.append(match)
        
        db.session.commit()
        print(f"✅ {len(partidos)} partidos creados")
        
        # Contar por fase
        fase_counts = {}
        for phase_id, _, _, _ in PARTIDOS_MUNDIAL_2026:
            fase_counts[phase_id] = fase_counts.get(phase_id, 0) + 1
        
        for fase_id, count in sorted(fase_counts.items()):
            fase_name = fases[fase_id-1].name
            print(f"   - {fase_name}: {count} partidos")
        
        # PASO 5: Crear pronósticos (solo fechas 1, 2, y 3 - con algunos faltantes)
        print(f"\n[5/6] 🎲 Generando pronósticos ficticios...")
        print("   (Solo fechas 1, 2, y 3 - algunos usuarios sin pronosticar)")
        
        # Obtener partidos de fechas 1, 2, 3
        matches_fase123 = Match.query.filter(Match.phase_id.in_([1, 2, 3])).all()
        
        total_pronosticos = 0
        total_posibles = len(usuarios) * len(matches_fase123)
        
        for user in usuarios:
            user_predictions = 0
            
            for match in matches_fase123:
                # Probabilidad del 85% de hacer el pronóstico
                # Esto deja ~15% de pronósticos sin hacer
                if random.random() < 0.85:
                    home_goals, away_goals = generar_pronostico_realista()
                    
                    prediction = Prediction(
                        user_id=user.id,
                        match_id=match.id,
                        home_goals=home_goals,
                        away_goals=away_goals
                    )
                    db.session.add(prediction)
                    user_predictions += 1
                    total_pronosticos += 1
            
            print(f"   {user.name}: {user_predictions}/{len(matches_fase123)} pronósticos")
        
        db.session.commit()
        print(f"✅ {total_pronosticos} pronósticos creados de {total_posibles} posibles ({total_pronosticos/total_posibles*100:.1f}%)")
        
        # PASO 6: Resumen final
        print("\n" + "="*80)
        print("📊 RESUMEN FINAL")
        print("="*80)
        print(f"✅ Fases: {Phase.query.count()}")
        print(f"✅ Usuarios: {User.query.filter_by(is_admin=False).count()} (no admin)")
        print(f"✅ Partidos: {Match.query.count()}")
        print(f"   - Fecha 1: {Match.query.filter_by(phase_id=1).count()}")
        print(f"   - Fecha 2: {Match.query.filter_by(phase_id=2).count()}")
        print(f"   - Fecha 3: {Match.query.filter_by(phase_id=3).count()}")
        print(f"   - Fecha 4: {Match.query.filter_by(phase_id=4).count()}")
        print(f"✅ Pronósticos: {Prediction.query.count()}")
        print(f"✅ Emails permitidos: {AllowedEmail.query.count()}")
        print("\n🎉 ¡Base de datos ficticia generada exitosamente!")
        print("\n💡 Credenciales de usuarios:")
        print("   Email: cualquiera de los emails ficticios")
        print("   Contraseña: prode123")
        print("="*80 + "\n")

if __name__ == '__main__':
    main()
