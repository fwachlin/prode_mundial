from app import app, db
from models import Phase

def init_phases():
    """Crear las 4 fases del mundial"""
    with app.app_context():
        # Verificar si ya existen
        if Phase.query.count() > 0:
            print("Las fases ya están creadas")
            return
        
        phases = [
            Phase(name="Fecha 1", order=1),
            Phase(name="Fecha 2", order=2),
            Phase(name="Fecha 3", order=3),
            Phase(name="Fecha 4 - Eliminación Directa", order=4),
        ]
        
        for phase in phases:
            db.session.add(phase)
        
        db.session.commit()
        print("✅ Fases creadas correctamente:")
        for phase in phases:
            print(f"  - {phase.name}")

if __name__ == '__main__':
    init_phases()