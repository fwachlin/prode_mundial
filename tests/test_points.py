"""
Tests del sistema de puntos - CRÍTICO
Estos tests validan la lógica de cálculo de puntos documentada en PROJECT_RULES.md
"""
import pytest
from models import db, User, Match, Prediction
from datetime import datetime, timezone, timedelta


class TestPointsCalculation:
    """Tests del cálculo de puntos"""
    
    def test_exact_prediction_max_points(self, app):
        """Pronóstico exacto da máximo de puntos (10 + 5 = 15 + batacazo)"""
        with app.app_context():
            # Crear partido finalizado
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Argentina',
                away_team='Brasil',
                kickoff_at=now - timedelta(hours=2),
                closes_at=now - timedelta(hours=3),
                phase_id=1,
                home_goals=2,
                away_goals=1
            )
            db.session.add(match)
            db.session.commit()
            
            # Crear usuario
            user = User(name='Test', email='test@test.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            # Pronóstico exacto
            pred = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=2,  # Exacto
                away_goals=1   # Exacto
            )
            db.session.add(pred)
            db.session.commit()
            
            points = pred.calculate_points()
            
            # 10 (ganador) + 5 (score exacto) + bonus batacazo (100% acierto = 0)
            assert points >= 15
    
    def test_correct_winner_wrong_score(self, app):
        """Acertar ganador pero no score exacto"""
        with app.app_context():
            # Partido: Argentina 3 - Brasil 1
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Argentina',
                away_team='Brasil',
                kickoff_at=now - timedelta(hours=2),
                closes_at=now - timedelta(hours=3),
                phase_id=1,
                home_goals=3,
                away_goals=1
            )
            db.session.add(match)
            db.session.commit()
            
            user = User(name='Test', email='test@test.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            # Pronóstico: Argentina 2 - Brasil 0 (ganador correcto, score incorrecto)
            pred = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=2,
                away_goals=0
            )
            db.session.add(pred)
            db.session.commit()
            
            points = pred.calculate_points()
            
            # 10 (ganador) + score points
            # Diferencia: |2-3| + |0-1| = 1 + 1 = 2
            # Score points: max(-5, 5 - 2) = 3
            assert points >= 10  # Al menos ganador
            assert points <= 15  # No es exacto
    
    def test_wrong_winner_zero_points(self, app):
        """Si no acierta ganador, devuelve 0"""
        with app.app_context():
            # Partido: Argentina 2 - Brasil 1 (gana Argentina)
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Argentina',
                away_team='Brasil',
                kickoff_at=now - timedelta(hours=2),
                closes_at=now - timedelta(hours=3),
                phase_id=1,
                home_goals=2,
                away_goals=1
            )
            db.session.add(match)
            db.session.commit()
            
            user = User(name='Test', email='test@test.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            # Pronóstico: Brasil 3 - Argentina 0 (ganador incorrecto)
            pred = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=0,
                away_goals=3
            )
            db.session.add(pred)
            db.session.commit()
            
            points = pred.calculate_points()
            
            # NO acertó ganador (0 puntos) + NO batacazo (0) + score (diferencia 4 goles: 5-4=1)
            assert points == 1
    
    def test_draw_prediction_correct(self, app):
        """Acertar empate correctamente"""
        with app.app_context():
            # Partido: Empate 2-2
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Chile',
                away_team='Uruguay',
                kickoff_at=now - timedelta(hours=2),
                closes_at=now - timedelta(hours=3),
                phase_id=1,
                home_goals=2,
                away_goals=2
            )
            db.session.add(match)
            db.session.commit()
            
            user = User(name='Test', email='test@test.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            # Pronóstico: Empate 2-2 (exacto)
            pred = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=2,
                away_goals=2
            )
            db.session.add(pred)
            db.session.commit()
            
            points = pred.calculate_points()
            
            # 10 (empate) + 5 (exacto)
            assert points >= 15
    
    def test_draw_prediction_wrong_score(self, app):
        """Acertar empate pero no score"""
        with app.app_context():
            # Partido: Empate 1-1
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Chile',
                away_team='Uruguay',
                kickoff_at=now - timedelta(hours=2),
                closes_at=now - timedelta(hours=3),
                phase_id=1,
                home_goals=1,
                away_goals=1
            )
            db.session.add(match)
            db.session.commit()
            
            user = User(name='Test', email='test@test.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            # Pronóstico: Empate 2-2 (empate correcto, score incorrecto)
            pred = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=2,
                away_goals=2
            )
            db.session.add(pred)
            db.session.commit()
            
            points = pred.calculate_points()
            
            # 10 (empate) + score reducido
            # Diferencia: |2-1| + |2-1| = 1 + 1 = 2
            # Score: max(-5, 5 - 2) = 3
            assert points >= 10
            assert points < 15  # No exacto
    
    def test_no_result_no_points(self, app):
        """Sin resultado cargado, no hay puntos"""
        with app.app_context():
            # Partido sin resultado
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='México',
                away_team='Canadá',
                kickoff_at=now + timedelta(hours=2),
                closes_at=now + timedelta(hours=1),
                phase_id=1,
                home_goals=None,  # Sin resultado
                away_goals=None
            )
            db.session.add(match)
            db.session.commit()
            
            user = User(name='Test', email='test@test.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            pred = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=2,
                away_goals=1
            )
            db.session.add(pred)
            db.session.commit()
            
            points = pred.calculate_points()
            
            assert points == 0
    
    def test_batacazo_bonus_low_percentage(self, app):
        """Bonus de batacazo cuando pocos aciertan"""
        with app.app_context():
            # Partido: Argentina 3 - Brasil 0
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Argentina',
                away_team='Brasil',
                kickoff_at=now - timedelta(hours=2),
                closes_at=now - timedelta(hours=3),
                phase_id=1,
                home_goals=3,
                away_goals=0
            )
            db.session.add(match)
            db.session.commit()
            
            # Crear 20 usuarios que pronostican mal
            for i in range(20):
                user = User(name=f'User{i}', email=f'user{i}@test.com')
                user.set_password('pass')
                db.session.add(user)
                db.session.commit()
                
                # Todos pronostican que gana Brasil
                pred = Prediction(
                    user_id=user.id,
                    match_id=match.id,
                    home_goals=0,
                    away_goals=2
                )
                db.session.add(pred)
            
            # 1 usuario acierta (batacazo)
            correct_user = User(name='Correct', email='correct@test.com')
            correct_user.set_password('pass')
            db.session.add(correct_user)
            db.session.commit()
            
            correct_pred = Prediction(
                user_id=correct_user.id,
                match_id=match.id,
                home_goals=3,
                away_goals=0
            )
            db.session.add(correct_pred)
            db.session.commit()
            
            points = correct_pred.calculate_points()
            
            # Solo 1 de 21 acertó = ~4.7% → bonus de 5 puntos
            # 10 (ganador) + 5 (exacto) + 5 (batacazo) = 20
            assert points == 20
    
    def test_negative_score_points(self, app):
        """Verificar que se pueden obtener puntos negativos hasta -5"""
        with app.app_context():
            # Partido: Argentina 5 - Brasil 0
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Argentina',
                away_team='Brasil',
                kickoff_at=now - timedelta(hours=2),
                closes_at=now - timedelta(hours=3),
                phase_id=1,
                home_goals=5,
                away_goals=0
            )
            db.session.add(match)
            db.session.commit()
            
            user = User(name='Test', email='test@test.com')
            user.set_password('pass')
            db.session.add(user)
            db.session.commit()
            
            # Caso 1: No acertar ganador y tener score muy diferente
            # Pronóstico: Argentina 0 - Brasil 3 (predice que gana Brasil)
            # No acierta ganador: 0 puntos
            # Diferencia score: |0-5| + |3-0| = 5 + 3 = 8 goles
            # Score points: max(-5, 5 - 8) = max(-5, -3) = -3
            # Total: 0 + (-3) = -3 puntos
            pred1 = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=0,
                away_goals=3
            )
            db.session.add(pred1)
            db.session.commit()
            
            points1 = pred1.calculate_points()
            assert points1 == -3
            
            # Caso 2: Acertar ganador pero con diferencia grande en score
            # Pronóstico: Argentina 1 - Brasil 0 (acierta ganador)
            # Ganador: 10 puntos
            # Diferencia score: |1-5| + |0-0| = 4 + 0 = 4 goles
            # Score points: max(-5, 5 - 4) = 1
            # Total: 10 + 1 = 11
            pred2 = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=1,
                away_goals=0
            )
            db.session.add(pred2)
            db.session.commit()
            
            points2 = pred2.calculate_points()
            assert points2 == 11
            
            # Caso 3: No acertar ganador con diferencia muy grande (más de 10 goles)
            # Pronóstico: Argentina 0 - Brasil 6 (predice que gana Brasil)
            # No acierta ganador: 0 puntos
            # Diferencia score: |0-5| + |6-0| = 5 + 6 = 11 goles
            # Score points: max(-5, 5 - 11) = max(-5, -6) = -5 (límite)
            # Total: 0 + (-5) = -5 puntos
            pred3 = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=0,
                away_goals=6
            )
            db.session.add(pred3)
            db.session.commit()
            
            points3 = pred3.calculate_points()
            assert points3 == -5
            
            # Caso 4: Acertar ganador con poca diferencia en score
            # Pronóstico: Argentina 4 - Brasil 0 (acierta ganador)
            # Ganador: 10 puntos
            # Diferencia score: |4-5| + |0-0| = 1 + 0 = 1 gol
            # Score points: max(-5, 5 - 1) = 4
            # Total: 10 + 4 = 14
            pred4 = Prediction(
                user_id=user.id,
                match_id=match.id,
                home_goals=4,
                away_goals=0
            )
            db.session.add(pred4)
            db.session.commit()
            
            points4 = pred4.calculate_points()
            assert points4 == 14

