# -*- coding: utf-8 -*-
import os
from flask import Flask
from extensions import db
from models import Match
import sys

# Crear app mínima sin auto-run
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prode.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    print("\n=== Primeros 5 partidos en la base de datos ===\n")
    matches = Match.query.limit(5).all()
    for m in matches:
        print(f"ID: {m.id} | Home: '{m.home_team}' | Away: '{m.away_team}'")
    print("\n" + "="*50)

sys.exit(0)
