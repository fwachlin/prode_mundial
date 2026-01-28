from app import app, db
from models import Match
with app.app_context():
    Match.query.delete()
    db.session.commit()
    print("✅ Partidos eliminados")