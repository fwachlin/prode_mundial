"""Script para verificar las fases existentes"""
from app import app
from models import Phase

with app.app_context():
    phases = Phase.query.all()
    print(f"\n📊 Total de fases: {len(phases)}")
    for phase in phases:
        print(f"  ID: {phase.id} | Nombre: '{phase.name}'")
