# -*- coding: utf-8 -*-
"""
Endpoint temporal para resetear la base de datos en Render
ELIMINAR DESPUÉS DE USAR
"""
from flask import Blueprint, jsonify
from extensions import db
from models import Phase, Match, User, Prediction
from datetime import datetime, timezone
import random

reset_bp = Blueprint('reset', __name__)

@reset_bp.route('/secret-reset-db-do-not-share')
def reset_database():
    try:
        # Eliminar y recrear tablas
        db.drop_all()
        db.create_all()
        
        # Crear fases
        phases = [
            Phase(name="Fecha 1", order=1),
            Phase(name="Fecha 2", order=2),
            Phase(name="Fecha 3", order=3),
            Phase(name="Fecha 4 - Eliminación Directa", order=4)
        ]
        for phase in phases:
            db.session.add(phase)
        db.session.commit()
        
        # Obtener fases
        fase1 = Phase.query.filter_by(name="Fecha 1").first()
        fase2 = Phase.query.filter_by(name="Fecha 2").first()
        fase3 = Phase.query.filter_by(name="Fecha 3").first()
        fase4 = Phase.query.filter_by(name="Fecha 4 - Eliminación Directa").first()
        PARTIDOS = [
            # FECHA 1
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
            
            # FECHA 2
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
            
            # FECHA 3
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
        ]
        
        partidos_cargados = 0
        for home, away, fecha_str in PARTIDOS:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M UTC')
            fecha = fecha.replace(tzinfo=timezone.utc)
            cierre = fecha
            
            if partidos_cargados < 24:
                fase = fase1
            elif partidos_cargados < 48:
                fase = fase2
            else:
                fase = fase3
            
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
        
        return jsonify({
            'success': True,
            'message': f'{partidos_cargados} partidos cargados exitosamente',
            'fases': 4,
            'fecha1': Match.query.filter_by(phase_id=fase1.id).count(),
            'fecha2': Match.query.filter_by(phase_id=fase2.id).count(),
            'fecha3': Match.query.filter_by(phase_id=fase3.id).count()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@reset_bp.route('/create-test-users')
def create_test_users():
    try:
        # Crear 10 usuarios ficticios
        usuarios = [
            ('Juan Pérez', 'juan.perez@observatorio.org'),
            ('María García', 'maria.garcia@observatorio.org'),
            ('Carlos López', 'carlos.lopez@observatorio.org'),
            ('Ana Martínez', 'ana.martinez@observatorio.org'),
            ('Pedro Rodríguez', 'pedro.rodriguez@observatorio.org'),
            ('Laura Fernández', 'laura.fernandez@observatorio.org'),
            ('Diego Sánchez', 'diego.sanchez@observatorio.org'),
            ('Sofía Ramírez', 'sofia.ramirez@observatorio.org'),
            ('Miguel Torres', 'miguel.torres@observatorio.org'),
            ('Elena Ruiz', 'elena.ruiz@observatorio.org')
        ]
        
        users_created = []
        for nombre, email in usuarios:
            user = User(
                name=nombre,
                email=email,
                is_admin=False
            )
            user.set_password('password123')
            db.session.add(user)
            users_created.append(nombre)
        
        db.session.commit()
        
        # Crear pronósticos aleatorios para partidos de Fecha 1, 2 y 3
        users = User.query.filter_by(is_admin=False).all()
        matches = Match.query.filter(Match.phase_id.in_([1, 2, 3])).all()
        
        predictions_created = 0
        for user in users:
            # Cada usuario pronostica entre 50% y 100% de los partidos
            num_predictions = random.randint(len(matches) // 2, len(matches))
            selected_matches = random.sample(matches, num_predictions)
            
            for match in selected_matches:
                # Generar goles aleatorios (más probable 0-2 goles)
                weights = [30, 35, 25, 8, 2]  # Pesos para 0, 1, 2, 3, 4 goles
                home_goals = random.choices([0, 1, 2, 3, 4], weights=weights)[0]
                away_goals = random.choices([0, 1, 2, 3, 4], weights=weights)[0]
                
                prediction = Prediction(
                    user_id=user.id,
                    match_id=match.id,
                    home_goals=home_goals,
                    away_goals=away_goals
                )
                db.session.add(prediction)
                predictions_created += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'users_created': len(users_created),
            'users': users_created,
            'predictions_created': predictions_created
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
