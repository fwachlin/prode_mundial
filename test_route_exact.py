# -*- coding: utf-8 -*-
from flask import Flask
from extensions import db
from models import User, Match, Prediction, Phase

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prode.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print("\n=== SIMULANDO EXACTAMENTE LA RUTA ALL-PREDICTIONS ===\n")
    
    # Exactamente como en la ruta
    phases = Phase.query.order_by(Phase.order).all()
    print(f"1. Phases: {len(phases)}")
    
    users = User.query.filter_by(is_admin=False).order_by(User.name).all()
    print(f"2. Users (is_admin=False): {len(users)}")
    if users:
        print("   Primeros 3:")
        for u in users[:3]:
            print(f"     - {u.name} (is_admin={u.is_admin})")
    else:
        print("   ¡NO HAY USUARIOS!")
    
    predictions = Prediction.query.all()
    print(f"3. Predictions: {len(predictions)}")
    
    pred_map = {(p.user_id, p.match_id): p for p in predictions}
    print(f"4. Pred_map: {len(pred_map)} items")
    
    phase_data = []
    for phase in phases:
        if 'Eliminación Directa' in phase.name or phase.name == 'Fecha 4':
            continue
        matches = Match.query.filter_by(phase_id=phase.id).order_by(Match.kickoff_at).all()
        if not matches:
            continue
        phase_data.append({
            'phase': phase,
            'matches': matches,
            'users': users,
            'pred_map': pred_map
        })
    
    print(f"5. Phase_data blocks: {len(phase_data)}")
    
    if phase_data:
        print("\n   Detalles del primer bloque:")
        first = phase_data[0]
        print(f"     Phase: {first['phase'].name}")
        print(f"     Matches: {len(first['matches'])}")
        print(f"     Users: {len(first['users'])}")
        print(f"     Pred_map keys: {len(first['pred_map'])}")
        
        if first['users']:
            print(f"\n     Primeros 3 usuarios del bloque:")
            for u in first['users'][:3]:
                print(f"       - {u.name}")
    
    print("\n" + "="*60)
