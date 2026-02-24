"""
Script para cargar todos los partidos del Mundial 2026
Basado en el fixture oficial de FIFA - Usando códigos FIFA de 3 letras
"""

from datetime import datetime, timezone, timedelta
from app import app
from extensions import db
from models import Match

# Lista completa de los 72 partidos de fase de grupos del Mundial 2026
# Formato: (Home FIFA Code, Away FIFA Code, Fecha UTC)

PARTIDOS_2026 = [
    # ============================================
    # FECHA 1 - Primera jornada (24 partidos)
    # ============================================
    # GRUPO A
    ("MEX", "RSA", "2026-06-11 19:00"),
    ("KOR", "POL", "2026-06-12 02:00"),
    # GRUPO B
    ("CAN", "WAL", "2026-06-12 19:00"),
    ("QAT", "SUI", "2026-06-13 19:00"),
    # GRUPO C
    ("BRA", "MAR", "2026-06-13 22:00"),
    ("HAI", "SCO", "2026-06-14 01:00"),
    # GRUPO D
    ("USA", "PAR", "2026-06-13 01:00"),
    ("AUS", "ITA", "2026-06-14 04:00"),
    # GRUPO E
    ("GER", "CUW", "2026-06-14 17:00"),
    ("CIV", "ECU", "2026-06-14 23:00"),
    # GRUPO F
    ("NED", "JPN", "2026-06-14 20:00"),
    ("DEN", "TUN", "2026-06-15 02:00"),
    # GRUPO G
    ("BEL", "EGY", "2026-06-15 19:00"),
    ("IRN", "NZL", "2026-06-16 01:00"),
    # GRUPO H
    ("ESP", "CPV", "2026-06-15 16:00"),
    ("KSA", "URU", "2026-06-15 22:00"),
    # GRUPO I
    ("FRA", "SEN", "2026-06-16 19:00"),
    ("CHN", "NOR", "2026-06-16 22:00"),
    # GRUPO J
    ("ARG", "ALG", "2026-06-17 01:00"),
    ("AUT", "JOR", "2026-06-17 04:00"),
    # GRUPO K
    ("POR", "CRC", "2026-06-17 17:00"),
    ("UZB", "COL", "2026-06-18 02:00"),
    # GRUPO L
    ("ENG", "CRO", "2026-06-17 20:00"),
    ("GHA", "PAN", "2026-06-17 23:00"),
    
    # ============================================
    # FECHA 2 - Segunda jornada (24 partidos)
    # ============================================
    # GRUPO A
    ("POL", "RSA", "2026-06-18 16:00"),
    ("MEX", "KOR", "2026-06-19 01:00"),
    # GRUPO B
    ("SUI", "WAL", "2026-06-18 19:00"),
    ("CAN", "QAT", "2026-06-18 22:00"),
    # GRUPO C
    ("SCO", "MAR", "2026-06-19 22:00"),
    ("BRA", "HAI", "2026-06-20 01:00"),
    # GRUPO D
    ("USA", "AUS", "2026-06-19 19:00"),
    ("ITA", "PAR", "2026-06-20 04:00"),
    # GRUPO E
    ("GER", "CIV", "2026-06-20 20:00"),
    ("ECU", "CUW", "2026-06-21 00:00"),
    # GRUPO F
    ("NED", "DEN", "2026-06-20 17:00"),
    ("TUN", "JPN", "2026-06-21 04:00"),
    # GRUPO G
    ("BEL", "IRN", "2026-06-21 19:00"),
    ("NZL", "EGY", "2026-06-22 01:00"),
    # GRUPO H
    ("ESP", "KSA", "2026-06-21 16:00"),
    ("URU", "CPV", "2026-06-21 22:00"),
    # GRUPO I
    ("FRA", "CHN", "2026-06-22 21:00"),
    ("NOR", "SEN", "2026-06-23 00:00"),
    # GRUPO J
    ("ARG", "AUT", "2026-06-22 17:00"),
    ("JOR", "ALG", "2026-06-23 03:00"),
    # GRUPO K
    ("POR", "UZB", "2026-06-23 17:00"),
    ("COL", "CRC", "2026-06-24 02:00"),
    # GRUPO L
    ("ENG", "GHA", "2026-06-23 20:00"),
    ("PAN", "CRO", "2026-06-23 23:00"),
    
    # ============================================
    # FECHA 3 - Tercera jornada (24 partidos)
    # ============================================
    # GRUPO B
    ("SUI", "CAN", "2026-06-24 19:00"),
    ("WAL", "QAT", "2026-06-24 19:00"),
    # GRUPO C
    ("SCO", "BRA", "2026-06-24 22:00"),
    ("MAR", "HAI", "2026-06-24 22:00"),
    # GRUPO A
    ("POL", "MEX", "2026-06-25 01:00"),
    ("RSA", "KOR", "2026-06-25 01:00"),
    # GRUPO E
    ("CUW", "CIV", "2026-06-25 20:00"),
    ("ECU", "GER", "2026-06-25 20:00"),
    # GRUPO F
    ("JPN", "DEN", "2026-06-25 23:00"),
    ("TUN", "NED", "2026-06-25 23:00"),
    # GRUPO D
    ("ITA", "USA", "2026-06-26 02:00"),
    ("PAR", "AUS", "2026-06-26 02:00"),
    # GRUPO I
    ("NOR", "FRA", "2026-06-26 19:00"),
    ("SEN", "CHN", "2026-06-26 19:00"),
    # GRUPO H
    ("CPV", "KSA", "2026-06-27 00:00"),
    ("URU", "ESP", "2026-06-27 00:00"),
    # GRUPO G
    ("EGY", "IRN", "2026-06-27 03:00"),
    ("NZL", "BEL", "2026-06-27 03:00"),
    # GRUPO L
    ("PAN", "ENG", "2026-06-27 21:00"),
    ("CRO", "GHA", "2026-06-27 21:00"),
    # GRUPO K
    ("COL", "POR", "2026-06-27 23:30"),
    ("CRC", "UZB", "2026-06-27 23:30"),
    # GRUPO J
    ("ALG", "AUT", "2026-06-28 02:00"),
    ("JOR", "ARG", "2026-06-28 02:00"),
    
    # FECHA 4 - ELIMINACIÓN DIRECTA
    # Octavos de Final (32 equipos → 16 equipos)
    ("1A", "2B", "2026-06-29 19:00"),  # Octavos 1
    ("1C", "2D", "2026-06-29 22:00"),  # Octavos 2
    ("1E", "2F", "2026-06-30 19:00"),  # Octavos 3
    ("1G", "2H", "2026-06-30 22:00"),  # Octavos 4
    ("1B", "2A", "2026-07-01 19:00"),  # Octavos 5
    ("1D", "2C", "2026-07-01 22:00"),  # Octavos 6
    ("1F", "2E", "2026-07-02 19:00"),  # Octavos 7
    ("1H", "2G", "2026-07-02 22:00"),  # Octavos 8
    ("1I", "2J", "2026-07-03 19:00"),  # Octavos 9
    ("1K", "2L", "2026-07-03 22:00"),  # Octavos 10
    ("1J", "2I", "2026-07-04 19:00"),  # Octavos 11
    ("1L", "2K", "2026-07-04 22:00"),  # Octavos 12
    ("1A", "3C/D/E", "2026-07-05 19:00"),  # Octavos 13
    ("1B", "3A/C/D", "2026-07-05 22:00"),  # Octavos 14
    ("1C", "3A/B/E", "2026-07-06 19:00"),  # Octavos 15
    ("1D", "3A/B/C", "2026-07-06 22:00"),  # Octavos 16
    
    # Cuartos de Final (16 equipos → 8 equipos)
    ("W1", "W2", "2026-07-09 19:00"),  # Cuartos 1
    ("W3", "W4", "2026-07-09 22:00"),  # Cuartos 2
    ("W5", "W6", "2026-07-10 19:00"),  # Cuartos 3
    ("W7", "W8", "2026-07-10 22:00"),  # Cuartos 4
    ("W9", "W10", "2026-07-11 19:00"),  # Cuartos 5
    ("W11", "W12", "2026-07-11 22:00"),  # Cuartos 6
    ("W13", "W14", "2026-07-12 19:00"),  # Cuartos 7
    ("W15", "W16", "2026-07-12 22:00"),  # Cuartos 8
    
    # Semifinales (8 equipos → 4 equipos)
    ("W17", "W18", "2026-07-14 22:00"),  # Semifinal 1
    ("W19", "W20", "2026-07-15 22:00"),  # Semifinal 2
    ("W21", "W22", "2026-07-16 22:00"),  # Semifinal 3
    ("W23", "W24", "2026-07-17 22:00"),  # Semifinal 4
    
    # Final 4 (4 equipos → Campeón)
    ("L25", "L26", "2026-07-18 19:00"),  # 3er lugar Semifinal 1
    ("W25", "W26", "2026-07-18 22:00"),  # Final 1
    ("L27", "L28", "2026-07-19 19:00"),  # 3er lugar Semifinal 2
    ("W27", "W28", "2026-07-19 22:00"),  # Final 2 - FINAL DEL TORNEO
]

def cargar_partidos():
    """Carga todos los partidos del Mundial 2026 en la base de datos"""
    with app.app_context():
        # Importar Phase model
        from models import Phase
        
        # Obtener las fases
        fase1 = Phase.query.filter_by(name="Fecha 1").first()
        fase2 = Phase.query.filter_by(name="Fecha 2").first()
        fase3 = Phase.query.filter_by(name="Fecha 3").first()
        fase4 = Phase.query.filter_by(name="Fecha 4 - Eliminación Directa").first()
        
        if not fase1 or not fase2 or not fase3 or not fase4:
            print("❌ ERROR: Las fases no están creadas. Ejecuta primero: python init_phases.py")
            return
        
        # Eliminar todos los partidos existentes
        Match.query.delete()
        db.session.commit()
        print("Partidos anteriores eliminados\n")
        
        partidos_cargados = 0
        
        for home, away, kickoff_str in PARTIDOS_2026:
            # Convertir string de fecha a objeto datetime UTC
            kickoff = datetime.strptime(kickoff_str, "%Y-%m-%d %H:%M")
            kickoff = kickoff.replace(tzinfo=timezone.utc)
            
            # Determinar la fase según el número de partido
            # Fase de grupos: 72 partidos divididos en 3 fechas de 24 partidos cada una
            # Fecha 4: Eliminación directa (partidos 73 en adelante)
            if partidos_cargados < 24:
                phase = fase1  # Fecha 1: Partidos 1-24
            elif partidos_cargados < 48:
                phase = fase2  # Fecha 2: Partidos 25-48
            elif partidos_cargados < 72:
                phase = fase3  # Fecha 3: Partidos 49-72
            else:
                phase = fase4  # Eliminación Directa: Partidos 73+
            
            # La ventana de pronósticos cierra 10 minutos antes del partido
            closes = kickoff - timedelta(minutes=10)
            
            # Crear partido
            match = Match(
                home_team=home,
                away_team=away,
                kickoff_at=kickoff,
                closes_at=closes,
                phase_id=phase.id
            )
            
            db.session.add(match)
            partidos_cargados += 1
            print(f"OK {home} vs {away} - {kickoff_str} UTC ({phase.name})")
        
        db.session.commit()
        print(f"\nOK {partidos_cargados} partidos cargados exitosamente!")
        print(f"Total de partidos en la base de datos: {Match.query.count()}")

if __name__ == '__main__':
    cargar_partidos()
