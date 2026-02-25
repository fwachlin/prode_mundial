"""Script para listar todas las rutas disponibles en la app"""
from app import app

with app.app_context():
    print("\n📋 Rutas disponibles en la aplicación:\n")
    for rule in app.url_map.iter_rules():
        if 'fase4' in rule.rule.lower() or 'admin' in rule.rule.lower():
            print(f"  {rule.rule:50s} -> {rule.endpoint}")
