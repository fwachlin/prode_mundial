"""Script para verificar y corregir campos datetime que puedan estar como string"""
from app import app
from models import Match
from datetime import datetime, timezone

with app.app_context():
    matches = Match.query.all()
    fixed = 0
    
    for match in matches:
        # Verificar si kickoff_at o closes_at son strings
        if isinstance(match.kickoff_at, str):
            print(f"⚠️ Match {match.id} tiene kickoff_at como string: {match.kickoff_at}")
            try:
                match.kickoff_at = datetime.fromisoformat(match.kickoff_at.replace('Z', '+00:00'))
                if match.kickoff_at.tzinfo is None:
                    match.kickoff_at = match.kickoff_at.replace(tzinfo=timezone.utc)
                fixed += 1
                print(f"   ✅ Corregido a datetime")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        if isinstance(match.closes_at, str):
            print(f"⚠️ Match {match.id} tiene closes_at como string: {match.closes_at}")
            try:
                match.closes_at = datetime.fromisoformat(match.closes_at.replace('Z', '+00:00'))
                if match.closes_at.tzinfo is None:
                    match.closes_at = match.closes_at.replace(tzinfo=timezone.utc)
                fixed += 1
                print(f"   ✅ Corregido a datetime")
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    if fixed > 0:
        from extensions import db
        db.session.commit()
        print(f"\n✅ Se corrigieron {fixed} campos")
    else:
        print("\n✅ Todos los campos datetime están correctos")
