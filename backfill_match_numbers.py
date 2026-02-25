"""
Backfill match_number for existing matches.
Assigns sequential numbers ordered by kickoff_at, then id.
Run: python backfill_match_numbers.py
"""
from app import app
from models import db, Match, Phase

with app.app_context():
    phase4 = Phase.query.filter_by(order=4).first()
    if not phase4:
        print("Phase 4 not found.")
        raise SystemExit(1)

    # Clear match_number for non-Phase 4 matches
    cleared = Match.query.filter(Match.phase_id != phase4.id).update({Match.match_number: None})

    # Assign sequential numbers only for Phase 4 (eliminación directa)
    matches = Match.query.filter_by(phase_id=phase4.id).order_by(Match.kickoff_at.asc(), Match.id.asc()).all()
    if not matches:
        db.session.commit()
        print("No Phase 4 matches found. Cleared other match_number values.")
        raise SystemExit(0)

    updated = 0
    number = 1
    for match in matches:
        if match.match_number != number:
            match.match_number = number
            updated += 1
        number += 1

    db.session.commit()
    print(f"Cleared {cleared} non-Phase 4 matches. Updated {updated} Phase 4 matches with sequential match_number.")
