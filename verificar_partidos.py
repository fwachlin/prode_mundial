# -*- coding: utf-8 -*-
from app import app
from models import Match, Phase

with app.app_context():
    total = Match.query.count()
    print(f"Total de partidos en DB: {total}")
    
    for phase in Phase.query.order_by(Phase.order).all():
        count = Match.query.filter_by(phase_id=phase.id).count()
        print(f"  {phase.name}: {count} partidos")
