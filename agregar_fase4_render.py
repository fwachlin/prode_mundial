"""
Script para agregar los 32 partidos de la Fase 4 (Eliminación Directa) - VERSIÓN PARA RENDER
Para ejecutar en Render después de haber cargado los 72 partidos de fase de grupos
"""

from datetime import datetime, timezone, timedelta
import os
from app import app
from extensions import db
from models import Match, Phase

# 32 partidos de eliminación directa
PARTIDOS_FASE4 = [
    # Octavos de Final (16 partidos)
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
    
    # Cuartos de Final (8 partidos)
    ("W1", "W2", "2026-07-09 19:00"),  # Cuartos 1
    ("W3", "W4", "2026-07-09 22:00"),  # Cuartos 2
    ("W5", "W6", "2026-07-10 19:00"),  # Cuartos 3
    ("W7", "W8", "2026-07-10 22:00"),  # Cuartos 4
    ("W9", "W10", "2026-07-11 19:00"),  # Cuartos 5
    ("W11", "W12", "2026-07-11 22:00"),  # Cuartos 6
    ("W13", "W14", "2026-07-12 19:00"),  # Cuartos 7
    ("W15", "W16", "2026-07-12 22:00"),  # Cuartos 8
    
    # Semifinales (4 partidos)
    ("W17", "W18", "2026-07-14 22:00"),  # Semifinal 1
    ("W19", "W20", "2026-07-15 22:00"),  # Semifinal 2
    ("W21", "W22", "2026-07-16 22:00"),  # Semifinal 3
    ("W23", "W24", "2026-07-17 22:00"),  # Semifinal 4
    
    # Final 4 (4 partidos)
    ("L25", "L26", "2026-07-18 19:00"),  # 3er lugar Semifinal 1
    ("W25", "W26", "2026-07-18 22:00"),  # Final 1
    ("L27", "L28", "2026-07-19 19:00"),  # 3er lugar Semifinal 2
    ("W27", "W28", "2026-07-19 22:00"),  # Final 2 - FINAL DEL TORNEO
]

def agregar_fase4_produccion():
    """Agrega los 32 partidos de la Fase 4 (Eliminación Directa) - sin interacción"""
    with app.app_context():
        # Obtener la Fase 4
        fase4 = Phase.query.filter_by(name='Fecha 4 - Eliminación Directa').first()
        
        if not fase4:
            print("❌ ERROR: No se encontró la Fase 4 en la base de datos")
            print("Ejecuta primero init_phases.py para crear las fases")
            return
        
        # Verificar cuántos partidos hay actualmente
        total_antes = Match.query.count()
        print(f"📊 Partidos actuales en la base de datos: {total_antes}")
        
        # Verificar si ya existen partidos de Fase 4
        partidos_fase4_existentes = Match.query.filter_by(phase_id=fase4.id).count()
        print(f"📊 Partidos de Fase 4 existentes: {partidos_fase4_existentes}")
        
        # Contar partidos agregados
        partidos_agregados = 0
        
        # Agregar cada partido de Fase 4
        for home, away, kickoff_str in PARTIDOS_FASE4:
            # Verificar si ya existe este partido
            existing = Match.query.filter_by(
                home_team=home,
                away_team=away,
                phase_id=fase4.id
            ).first()
            
            if existing:
                print(f"⏭️  OMITIDO (ya existe): {home} vs {away}")
                continue
            
            # Convertir string de fecha a objeto datetime UTC
            kickoff = datetime.strptime(kickoff_str, "%Y-%m-%d %H:%M")
            kickoff = kickoff.replace(tzinfo=timezone.utc)
            
            # La ventana de pronósticos cierra 10 minutos antes del partido
            closes = kickoff - timedelta(minutes=10)
            
            # Crear partido
            match = Match(
                home_team=home,
                away_team=away,
                kickoff_at=kickoff,
                closes_at=closes,
                phase_id=fase4.id
            )
            
            db.session.add(match)
            partidos_agregados += 1
            print(f"✅ {home} vs {away} - {kickoff_str} UTC")
        
        # Guardar cambios
        db.session.commit()
        
        total_despues = Match.query.count()
        print(f"\n✅ {partidos_agregados} partidos de Fase 4 agregados exitosamente!")
        print(f"📊 Total de partidos antes: {total_antes}")
        print(f"📊 Total de partidos ahora: {total_despues}")
        print(f"📊 Partidos de Fase 4: {Match.query.filter_by(phase_id=fase4.id).count()}")

if __name__ == '__main__':
    agregar_fase4_produccion()
