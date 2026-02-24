# -*- coding: utf-8 -*-
from flask import Flask
from extensions import db
from models import User, Match, Prediction, Phase

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prode.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print("\n=== SIMULANDO RUTA ALL-PREDICTIONS ===\n")
    
    phases = Phase.query.order_by(Phase.order).all()
    print(f"Fases totales: {len(phases)}")
    
    users = User.query.filter(User.is_admin == False).order_by(User.name).all()
    print(f"Usuarios (no admin): {len(users)}")
    
    predictions = Prediction.query.all()
    print(f"Pronósticos totales: {len(predictions)}")
    
    pred_map = {(p.user_id, p.match_id): p for p in predictions}
    print(f"Pred_map keys: {len(pred_map)}")
    
    phase_data = []
    for phase in phases:
        # Excluir Fecha 4
        if 'Eliminación Directa' in phase.name or phase.name == 'Fecha 4':
            print(f"\nSaltando: {phase.name}")
            continue
        
        matches = Match.query.filter_by(phase_id=phase.id).order_by(Match.kickoff_at).all()
        print(f"\n{phase.name}: {len(matches)} partidos")
        
        if not matches:
            continue
        
        phase_data.append({
            'phase': phase,
            'matches': matches,
            'users': users,
            'pred_map': pred_map
        })
    
    print(f"\n=== RESUMEN ===")
    print(f"phase_data tiene {len(phase_data)} bloques")
    for i, block in enumerate(phase_data):
        print(f"Bloque {i}: {block['phase'].name} - {len(block['matches'])} partidos - {len(block['users'])} usuarios")
        
        # Verificar algunos pronósticos
        if block['users'] and block['matches']:
            user = block['users'][0]
            match = block['matches'][0]
            key = (user.id, match.id)
            p = block['pred_map'].get(key)
            print(f"  Ejemplo: {user.name} - {match.home_team} vs {match.away_team}: {p.home_goals if p else '?'}-{p.away_goals if p else '?'}")
    
    print("\n" + "="*60)
