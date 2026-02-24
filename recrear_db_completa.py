# -*- coding: utf-8 -*-
"""
Script para recrear completamente la base de datos con partidos del Mundial 2026
"""
import sys
from app import app, db
from models import Phase, Match
from datetime import datetime, timezone

# Evitar que Flask inicie el servidor
if __name__ != '__main__':
    sys.exit(0)

with app.app_context():
    print("\n" + "="*70)
    print("RECREANDO BASE DE DATOS COMPLETA")
    print("="*70)
    
    # 1. Eliminar y recrear todas las tablas
    print("\n[1/3] Eliminando tablas antiguas y creando nuevas...")
    db.drop_all()
    db.create_all()
    print("✅ Tablas recreadas")
    
    # 2. Crear las fases
    print("\n[2/3] Creando fases...")
    phases = [
        Phase(name="Fecha 1", order=1),
        Phase(name="Fecha 2", order=2),
        Phase(name="Fecha 3", order=3),
        Phase(name="Fecha 4 - Eliminación Directa", order=4)
    ]
    for phase in phases:
        db.session.add(phase)
    db.session.commit()
    print("✅ 4 fases creadas")
    
    # 3. Cargar partidos del Mundial 2026
    print("\n[3/3] Cargando 104 partidos del Mundial 2026...")
    
    # Obtener las fases de la DB
    fase1 = Phase.query.filter_by(name="Fecha 1").first()
    fase2 = Phase.query.filter_by(name="Fecha 2").first()
    fase3 = Phase.query.filter_by(name="Fecha 3").first()
    fase4 = Phase.query.filter_by(name="Fecha 4 - Eliminación Directa").first()
    
    PARTIDOS_2026 = [
        # FECHA 1 - Jornada 1 de cada grupo (24 partidos)
        ('MEX', 'RSA', '2026-06-11 19:00 UTC'),
        ('KOR', 'POL', '2026-06-12 02:00 UTC'),
        ('CAN', 'WAL', '2026-06-12 19:00 UTC'),
        ('QAT', 'SUI', '2026-06-13 19:00 UTC'),
        ('BRA', 'MAR', '2026-06-13 22:00 UTC'),
        ('HAI', 'SCO', '2026-06-14 01:00 UTC'),
        ('USA', 'PAR', '2026-06-13 01:00 UTC'),
        ('AUS', 'ITA', '2026-06-14 04:00 UTC'),
        ('GER', 'CUW', '2026-06-14 17:00 UTC'),
        ('CIV', 'ECU', '2026-06-14 23:00 UTC'),
        ('NED', 'JPN', '2026-06-14 20:00 UTC'),
        ('DEN', 'TUN', '2026-06-15 02:00 UTC'),
        ('BEL', 'EGY', '2026-06-15 19:00 UTC'),
        ('IRN', 'NZL', '2026-06-16 01:00 UTC'),
        ('ESP', 'CPV', '2026-06-15 16:00 UTC'),
        ('KSA', 'URU', '2026-06-15 22:00 UTC'),
        ('FRA', 'SEN', '2026-06-16 19:00 UTC'),
        ('CHN', 'NOR', '2026-06-16 22:00 UTC'),
        ('ARG', 'ALG', '2026-06-17 01:00 UTC'),
        ('AUT', 'JOR', '2026-06-17 04:00 UTC'),
        ('POR', 'CRC', '2026-06-17 17:00 UTC'),
        ('UZB', 'COL', '2026-06-18 02:00 UTC'),
        ('ENG', 'CRO', '2026-06-17 20:00 UTC'),
        ('GHA', 'PAN', '2026-06-17 23:00 UTC'),
        
        # FECHA 2 - Jornada 2 de cada grupo (24 partidos)
        ('POL', 'RSA', '2026-06-18 16:00 UTC'),
        ('MEX', 'KOR', '2026-06-19 01:00 UTC'),
        ('SUI', 'WAL', '2026-06-18 19:00 UTC'),
        ('CAN', 'QAT', '2026-06-18 22:00 UTC'),
        ('SCO', 'MAR', '2026-06-19 22:00 UTC'),
        ('BRA', 'HAI', '2026-06-20 01:00 UTC'),
        ('USA', 'AUS', '2026-06-19 19:00 UTC'),
        ('ITA', 'PAR', '2026-06-20 04:00 UTC'),
        ('GER', 'CIV', '2026-06-20 20:00 UTC'),
        ('ECU', 'CUW', '2026-06-21 00:00 UTC'),
        ('NED', 'DEN', '2026-06-20 17:00 UTC'),
        ('TUN', 'JPN', '2026-06-21 04:00 UTC'),
        ('BEL', 'IRN', '2026-06-21 19:00 UTC'),
        ('NZL', 'EGY', '2026-06-22 01:00 UTC'),
        ('ESP', 'KSA', '2026-06-21 16:00 UTC'),
        ('URU', 'CPV', '2026-06-21 22:00 UTC'),
        ('FRA', 'CHN', '2026-06-22 21:00 UTC'),
        ('NOR', 'SEN', '2026-06-23 00:00 UTC'),
        ('ARG', 'AUT', '2026-06-22 17:00 UTC'),
        ('JOR', 'ALG', '2026-06-23 03:00 UTC'),
        ('POR', 'UZB', '2026-06-23 17:00 UTC'),
        ('COL', 'CRC', '2026-06-24 02:00 UTC'),
        ('ENG', 'GHA', '2026-06-23 20:00 UTC'),
        ('PAN', 'CRO', '2026-06-23 23:00 UTC'),
        
        # FECHA 3 - Jornada 3 de cada grupo (24 partidos - finales simultáneas)
        ('SUI', 'CAN', '2026-06-24 19:00 UTC'),
        ('WAL', 'QAT', '2026-06-24 19:00 UTC'),
        ('SCO', 'BRA', '2026-06-24 22:00 UTC'),
        ('MAR', 'HAI', '2026-06-24 22:00 UTC'),
        ('POL', 'MEX', '2026-06-25 01:00 UTC'),
        ('RSA', 'KOR', '2026-06-25 01:00 UTC'),
        ('CUW', 'CIV', '2026-06-25 20:00 UTC'),
        ('ECU', 'GER', '2026-06-25 20:00 UTC'),
        ('JPN', 'DEN', '2026-06-25 23:00 UTC'),
        ('TUN', 'NED', '2026-06-25 23:00 UTC'),
        ('ITA', 'USA', '2026-06-26 02:00 UTC'),
        ('PAR', 'AUS', '2026-06-26 02:00 UTC'),
        ('NOR', 'FRA', '2026-06-26 19:00 UTC'),
        ('SEN', 'CHN', '2026-06-26 19:00 UTC'),
        ('CPV', 'KSA', '2026-06-27 00:00 UTC'),
        ('URU', 'ESP', '2026-06-27 00:00 UTC'),
        ('EGY', 'IRN', '2026-06-27 03:00 UTC'),
        ('NZL', 'BEL', '2026-06-27 03:00 UTC'),
        ('PAN', 'ENG', '2026-06-27 21:00 UTC'),
        ('CRO', 'GHA', '2026-06-27 21:00 UTC'),
        ('COL', 'POR', '2026-06-27 23:30 UTC'),
        ('CRC', 'UZB', '2026-06-27 23:30 UTC'),
        ('ALG', 'AUT', '2026-06-28 02:00 UTC'),
        ('JOR', 'ARG', '2026-06-28 02:00 UTC'),
        
        # FECHA 4 - ELIMINACIÓN DIRECTA (32 partidos)
        # Octavos de final (16 partidos)
        ('1A', '2B', '2026-06-29 19:00 UTC'),
        ('1C', '2D', '2026-06-29 22:00 UTC'),
        ('1E', '2F', '2026-06-30 19:00 UTC'),
        ('1G', '2H', '2026-06-30 22:00 UTC'),
        ('1B', '2A', '2026-07-01 19:00 UTC'),
        ('1D', '2C', '2026-07-01 22:00 UTC'),
        ('1F', '2E', '2026-07-02 19:00 UTC'),
        ('1H', '2G', '2026-07-02 22:00 UTC'),
        ('1I', '2J', '2026-07-03 19:00 UTC'),
        ('1K', '2L', '2026-07-03 22:00 UTC'),
        ('1J', '2I', '2026-07-04 19:00 UTC'),
        ('1L', '2K', '2026-07-04 22:00 UTC'),
        ('1A', '3C/D/E', '2026-07-05 19:00 UTC'),
        ('1B', '3A/C/D', '2026-07-05 22:00 UTC'),
        ('1C', '3A/B/E', '2026-07-06 19:00 UTC'),
        ('1D', '3A/B/C', '2026-07-06 22:00 UTC'),
        # Cuartos de final (8 partidos)
        ('W1', 'W2', '2026-07-09 19:00 UTC'),
        ('W3', 'W4', '2026-07-09 22:00 UTC'),
        ('W5', 'W6', '2026-07-10 19:00 UTC'),
        ('W7', 'W8', '2026-07-10 22:00 UTC'),
        ('W9', 'W10', '2026-07-11 19:00 UTC'),
        ('W11', 'W12', '2026-07-11 22:00 UTC'),
        ('W13', 'W14', '2026-07-12 19:00 UTC'),
        ('W15', 'W16', '2026-07-12 22:00 UTC'),
        # Semifinales (4 partidos)
        ('W17', 'W18', '2026-07-14 22:00 UTC'),
        ('W19', 'W20', '2026-07-15 22:00 UTC'),
        ('W21', 'W22', '2026-07-16 22:00 UTC'),
        ('W23', 'W24', '2026-07-17 22:00 UTC'),
        # Tercer lugar y Final (4 partidos)
        ('L25', 'L26', '2026-07-18 19:00 UTC'),
        ('W25', 'W26', '2026-07-18 22:00 UTC'),
        ('L27', 'L28', '2026-07-19 19:00 UTC'),
        ('W27', 'W28', '2026-07-19 22:00 UTC'),
    ]
    
    partidos_cargados = 0
    for home, away, fecha_str in PARTIDOS_2026:
        # Parsear fecha
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M UTC')
        fecha = fecha.replace(tzinfo=timezone.utc)
        cierre = fecha  # Cierra a la misma hora del partido
        
        # Determinar fase basado en el contador
        if partidos_cargados < 24:
            fase = fase1
        elif partidos_cargados < 48:
            fase = fase2
        elif partidos_cargados < 72:
            fase = fase3
        else:
            fase = fase4
        
        # Crear partido
        match = Match(
            home_team=home,
            away_team=away,
            kickoff_at=fecha,
            closes_at=cierre,
            phase_id=fase.id
        )
        db.session.add(match)
        partidos_cargados += 1
    
    db.session.commit()
    
    print(f"✅ {partidos_cargados} partidos cargados exitosamente")
    
    # Verificar distribución
    print("\n" + "="*70)
    print("VERIFICACIÓN FINAL")
    print("="*70)
    print(f"Fecha 1: {Match.query.filter_by(phase_id=fase1.id).count()} partidos")
    print(f"Fecha 2: {Match.query.filter_by(phase_id=fase2.id).count()} partidos")
    print(f"Fecha 3: {Match.query.filter_by(phase_id=fase3.id).count()} partidos")
    print(f"Fecha 4: {Match.query.filter_by(phase_id=fase4.id).count()} partidos")
    print(f"TOTAL: {Match.query.count()} partidos")
    print("\n✅ BASE DE DATOS RECREADA EXITOSAMENTE\n")
    print("="*70)

sys.exit(0)
