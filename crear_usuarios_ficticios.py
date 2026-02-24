# -*- coding: utf-8 -*-
"""
Script para crear 10 usuarios ficticios con pronósticos variados
"""
from flask import Flask
from extensions import db
from models import User, Match, Prediction
from werkzeug.security import generate_password_hash
import random
import sys

# Crear app mínima
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prode.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    print("\n" + "="*70)
    print("CREANDO USUARIOS FICTICIOS CON PRONÓSTICOS")
    print("="*70)
    
    # Eliminar usuarios ficticios anteriores (no admin)
    print("\n[1/3] Eliminando usuarios ficticios anteriores...")
    User.query.filter_by(is_admin=False).delete()
    db.session.commit()
    print("✅ Usuarios anteriores eliminados")
    
    # Crear 10 usuarios ficticios
    print("\n[2/3] Creando 10 usuarios ficticios...")
    usuarios = [
        ("Juan Pérez", "juan@observatorio.com"),
        ("María García", "maria@observatorio.com"),
        ("Carlos Rodríguez", "carlos@observatorio.com"),
        ("Ana Martínez", "ana@observatorio.com"),
        ("Luis Fernández", "luis@observatorio.com"),
        ("Laura López", "laura@observatorio.com"),
        ("Diego González", "diego@observatorio.com"),
        ("Sofía Sánchez", "sofia@observatorio.com"),
        ("Miguel Torres", "miguel@observatorio.com"),
        ("Valentina Díaz", "valentina@observatorio.com")
    ]
    
    users_created = []
    for nombre, email in usuarios:
        user = User(
            name=nombre,
            email=email,
            is_admin=False
        )
        user.set_password("password123")
        db.session.add(user)
        users_created.append(user)
    
    db.session.commit()
    print(f"✅ {len(users_created)} usuarios creados")
    
    # Crear pronósticos variados para cada usuario
    print("\n[3/3] Generando pronósticos variados...")
    
    # Obtener todos los partidos de fase de grupos (primeros 72)
    matches = Match.query.order_by(Match.kickoff_at).limit(72).all()
    
    predictions_created = 0
    for user in users_created:
        # Cada usuario hace pronósticos para entre 50% y 100% de los partidos
        num_predictions = random.randint(int(len(matches) * 0.5), len(matches))
        selected_matches = random.sample(matches, num_predictions)
        
        for match in selected_matches:
            # Generar pronósticos variados pero realistas
            # La mayoría de los partidos tienen entre 0-3 goles
            home_goals = random.choices(
                [0, 1, 2, 3, 4], 
                weights=[15, 30, 30, 15, 10]
            )[0]
            
            away_goals = random.choices(
                [0, 1, 2, 3, 4], 
                weights=[15, 30, 30, 15, 10]
            )[0]
            
            prediction = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=home_goals,
                away_goals=away_goals
            )
            db.session.add(prediction)
            predictions_created += 1
    
    db.session.commit()
    print(f"✅ {predictions_created} pronósticos creados")
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    for user in users_created:
        count = Prediction.query.filter_by(user_id=user.id).count()
        print(f"{user.name:20s} - {count:2d} pronósticos")
    
    print("\n✅ PROCESO COMPLETADO EXITOSAMENTE\n")
    print("="*70)

sys.exit(0)
