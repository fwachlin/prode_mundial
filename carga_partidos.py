from datetime import datetime, timedelta, timezone
from app import create_app
from extensions import db
from models import Match

app = create_app()

PARTIDOS = [
    {
        "home": "Argentina",
        "away": "Brasil",
        "kickoff": datetime(2026, 1, 15, 22, 0, tzinfo=timezone.utc),
    },
    {
        "home": "Francia",
        "away": "Alemania",
        "kickoff": datetime(2026, 6, 16, 18, 0, tzinfo=timezone.utc),
    },
]

with app.app_context():
    for p in PARTIDOS:
        kickoff = p["kickoff"]
        closes = kickoff - timedelta(minutes=10)

        existente = Match.query.filter_by(
            home_team=p["home"],
            away_team=p["away"],
            kickoff_at=kickoff
        ).first()

        if existente:
            print(f"Ya existe: {p['home']} vs {p['away']} ({kickoff})")
            continue

        m = Match(
            home_team=p["home"],
            away_team=p["away"],
            kickoff_at=kickoff,
            closes_at=closes
        )
        db.session.add(m)
        print(f"Agregado: {p['home']} vs {p['away']}")

    db.session.commit()