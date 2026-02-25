from app import app
from models import Match
from datetime import timezone

with app.app_context():
    primer_partido = Match.query.order_by(Match.kickoff_at).first()
    print(f'Primer partido: {primer_partido.home_team} vs {primer_partido.away_team}')
    print(f'kickoff_at: {primer_partido.kickoff_at}')
    print(f'tzinfo: {primer_partido.kickoff_at.tzinfo}')
    if primer_partido.kickoff_at.tzinfo:
        print(f'ISO format: {primer_partido.kickoff_at.isoformat()}')
    else:
        print(f'ISO format (naive): {primer_partido.kickoff_at.isoformat()}')
        print(f'ISO format (forced UTC): {primer_partido.kickoff_at.replace(tzinfo=timezone.utc).isoformat()}')
