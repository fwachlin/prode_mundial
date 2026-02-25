from app import app
from models import db, User

with app.app_context():
    users = User.query.all()
    print(f'\n📊 Total usuarios: {len(users)}\n')
    
    for u in users:
        print(f'  - {u.name} ({u.email}) - Admin: {u.is_admin}, Enabled: {u.is_enabled}')
