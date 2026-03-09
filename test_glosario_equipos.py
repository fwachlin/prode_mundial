"""Test para verificar que el glosario muestra solo equipos participantes"""
from app import app
from models import Match
from fifa_countries import FIFA_COUNTRIES

with app.app_context():
    # Obtener códigos únicos de equipos
    all_matches = Match.query.all()
    team_codes = set()
    for match in all_matches:
        if match.home_team:
            team_codes.add(match.home_team)
        if match.away_team:
            team_codes.add(match.away_team)
    
    print(f"Total de partidos: {len(all_matches)}")
    print(f"Total de equipos únicos: {len(team_codes)}")
    print(f"\nEquipos participantes (ordenados):")
    for code in sorted(team_codes):
        if code in FIFA_COUNTRIES:
            iso2, name = FIFA_COUNTRIES[code]
            print(f"  {code}: {name} (ISO2: {iso2})")
        else:
            print(f"  {code}: [NO ENCONTRADO EN FIFA_COUNTRIES]")
    
    # Verificar CYP si está en los partidos
    print(f"\n¿CYP está en partidos? {('CYP' in team_codes)}")
    print(f"¿WAL está en partidos? {('WAL' in team_codes)}")
    print(f"¿POL está en partidos? {('POL' in team_codes)}")
