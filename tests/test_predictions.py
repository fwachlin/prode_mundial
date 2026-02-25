"""
Tests del sistema de pronósticos
"""
import pytest
from models import db, Prediction


class TestPredictionsAccess:
    """Tests de acceso a pronósticos"""
    
    def test_predictions_requires_login(self, client):
        """Acceso a pronósticos requiere login"""
        response = client.get('/predictions', follow_redirects=False)
        assert response.status_code == 302  # Redirect a login
    
    def test_admin_cannot_predict(self, client, admin_user):
        """Administradores no pueden hacer pronósticos"""
        # Login como admin
        client.post('/auth/login', data={
            'email': 'admin@example.com',
            'password': 'admin1234'
        })
        
        response = client.get('/predictions', follow_redirects=True)
        assert b'administradores no pueden' in response.data


class TestCreatePrediction:
    """Tests de creación de pronósticos"""
    
    def test_create_prediction_success(self, client, regular_user, open_match):
        """Crear pronóstico en partido abierto"""
        # Login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test1234'
        })
        
        # Crear pronóstico
        response = client.post('/predictions', data={
            'match_id': open_match,
            'home_goals': 2,
            'away_goals': 1
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verificar que se creó
        with client.application.app_context():
            pred = Prediction.query.filter_by(
                user_id=regular_user,
                match_id=open_match
            ).first()
            assert pred is not None
            assert pred.home_goals == 2
            assert pred.away_goals == 1
    
    def test_update_prediction(self, client, regular_user, prediction, open_match):
        """Modificar pronóstico existente"""
        # Login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test1234'
        })
        
        # Modificar pronóstico
        response = client.post('/predictions', data={
            'match_id': open_match,
            'home_goals': 3,  # Cambiar de 2 a 3
            'away_goals': 2   # Cambiar de 1 a 2
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verificar que se actualizó
        with client.application.app_context():
            pred = Prediction.query.filter_by(
                user_id=regular_user,
                match_id=open_match
            ).first()
            assert pred.home_goals == 3
            assert pred.away_goals == 2
    
    def test_cannot_predict_closed_match(self, client, regular_user, closed_match):
        """No se puede pronosticar en partido cerrado"""
        # Login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test1234'
        })
        
        # Intentar crear pronóstico
        response = client.post('/predictions', data={
            'match_id': closed_match,
            'home_goals': 2,
            'away_goals': 1
        }, follow_redirects=True)
        
        assert b'cerrado' in response.data
        
        # Verificar que NO se creó
        with client.application.app_context():
            pred = Prediction.query.filter_by(
                user_id=regular_user,
                match_id=closed_match
            ).first()
            assert pred is None
    
    def test_negative_goals_rejected(self, client, regular_user, open_match):
        """Goles negativos son rechazados"""
        # Login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'test1234'
        })
        
        # Intentar con goles negativos
        response = client.post('/predictions', data={
            'match_id': open_match,
            'home_goals': -1,
            'away_goals': 2
        }, follow_redirects=True)
        
        assert b'no pueden ser negativos' in response.data


class TestViewPredictions:
    """Tests de visualización de pronósticos"""
    
    def test_view_all_predictions(self, client, regular_user):
        """Ver todos los pronósticos (ruta pública)"""
        response = client.get('/all-predictions')
        assert response.status_code == 200
    
    def test_rankings_public(self, client):
        """Rankings son públicos"""
        response = client.get('/rankings')
        assert response.status_code == 200
    
    def test_rankings_exclude_admins(self, client, admin_user, regular_user, app):
        """Rankings excluyen administradores"""
        with app.app_context():
            # Crear pronóstico para regular user y admin
            from datetime import datetime, timezone, timedelta
            from models import Match, Prediction
            
            now = datetime.now(timezone.utc)
            match = Match(
                home_team='Test1',
                away_team='Test2',
                kickoff_at=now + timedelta(hours=2),
                closes_at=now - timedelta(hours=1),
                phase_id=1,
                home_goals=2,
                away_goals=1
            )
            db.session.add(match)
            db.session.commit()
            
            # Pronóstico de usuario regular
            pred1 = Prediction(
                user_id=regular_user,
                match_id=match.id,
                home_goals=2,
                away_goals=1,
                points_awarded=15
            )
            db.session.add(pred1)
            db.session.commit()
        
        response = client.get('/rankings')
        
        # Verificar que NO aparece el admin
        assert b'Admin User' not in response.data
        assert b'Test User' in response.data
