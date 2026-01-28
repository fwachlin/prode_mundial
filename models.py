from datetime import datetime, timezone
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)

    is_admin = db.Column(db.Boolean, default=False)
    is_enabled = db.Column(db.Boolean, default=True)
    
    predictions = db.relationship('Prediction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class AllowedEmail(db.Model):
    """Emails permitidos para registrarse"""
    __tablename__ = "allowed_emails"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f"<AllowedEmail {self.email}>"

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)


class Phase(db.Model):
    """Fases del mundial"""
    __tablename__ = "phases"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # "Fecha 1", "Fecha 2", etc.
    order = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4
    
    matches = db.relationship('Match', backref='phase', lazy=True)
    
    def __repr__(self):
        return f"<Phase {self.name}>"


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)

    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)

    kickoff_at = db.Column(db.DateTime(timezone=True), nullable=False)
    closes_at  = db.Column(db.DateTime(timezone=True), nullable=False)

    home_goals = db.Column(db.Integer, nullable=True)
    away_goals = db.Column(db.Integer, nullable=True)
    
    phase_id = db.Column(db.Integer, db.ForeignKey("phases.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            "home_team", "away_team", "kickoff_at",
            name="unique_match"
        ),
    )

    def is_open(self):
        """
        El pronóstico está abierto si ahora (UTC) es menor que closes_at.
        Se protege contra datetimes naive por datos legacy.
        """
        closes_at = self.closes_at

        if closes_at.tzinfo is None:
            closes_at = closes_at.replace(tzinfo=timezone.utc)

        return datetime.now(timezone.utc) < closes_at

    def __repr__(self):
        return (
            f"<Match {self.home_team} vs {self.away_team} "
            f"@ {self.kickoff_at.isoformat()}>"
        )
    


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=False)

    home_goals = db.Column(db.Integer, nullable=False)
    away_goals = db.Column(db.Integer, nullable=False)

    points_awarded = db.Column(db.Integer, nullable=True, default=None)  # ← Cambiar a nullable=True
    
    match = db.relationship('Match', backref='predictions')
    
    def calculate_points(self):
        """
        Calcular puntos según el sistema completo:
        - Ganador/Empate: 10 puntos
        - Batacazo: bonus de 5, 4, 3, 2 o 1 punto
        - Score: 5 puntos menos penalización
        """
        match = self.match
        
        # Si el resultado no está cargado, no hay puntos
        if match.home_goals is None or match.away_goals is None:
            return 0
        
        total_points = 0
        
        # ====== 1. GANADOR/EMPATE: 10 puntos ======
        user_result = self._get_result(self.home_goals, self.away_goals)
        match_result = self._get_result(match.home_goals, match.away_goals)
        
        if user_result == match_result:
            total_points += 10
        else:
            # Si no acertó el ganador, devuelve 0
            return 0
        
        # ====== 2. BATACAZO: bonus si pocos aciertan ======
        # Contar cuántos acertaron el ganador
        total_predictions = Prediction.query.filter_by(match_id=match.id).count()
        correct_predictions = Prediction.query.filter_by(match_id=match.id).all()
        correct_count = sum(1 for p in correct_predictions if self._get_result(p.home_goals, p.away_goals) == match_result)
        
        if total_predictions > 0:
            correct_percentage = (correct_count / total_predictions) * 100
            
            if correct_percentage < 5:
                total_points += 5
            elif correct_percentage < 10:
                total_points += 4
            elif correct_percentage < 15:
                total_points += 3
            elif correct_percentage < 20:
                total_points += 2
            elif correct_percentage < 25:
                total_points += 1
        
        # ====== 3. SCORE: 5 puntos menos penalización ======
        if self.home_goals == match.home_goals and self.away_goals == match.away_goals:
            # Acertó exacto
            total_points += 5
        else:
            # Calcular diferencia de goles
            home_diff = abs(self.home_goals - match.home_goals)
            away_diff = abs(self.away_goals - match.away_goals)
            total_diff = home_diff + away_diff
            
            score_points = max(0, 5 - total_diff)
            total_points += score_points
        
        return total_points
    
    def _get_result(self, home_goals, away_goals):
        """
        Retorna: 'home' si gana local, 'away' si gana visitante, 'draw' si empata
        """
        if home_goals > away_goals:
            return 'home'
        elif home_goals < away_goals:
            return 'away'
        else:
            return 'draw'