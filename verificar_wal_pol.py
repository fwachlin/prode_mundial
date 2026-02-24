# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('instance/prode.db')
cursor = conn.cursor()

print("\n=== Partidos con WAL (Wales) ===\n")
cursor.execute("SELECT id, home_team, away_team FROM matches WHERE home_team LIKE '%WAL%' OR away_team LIKE '%WAL%'")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r[0]:3d} | Home: '{r[1]}' | Away: '{r[2]}'")

print("\n=== Partidos con POL (Poland) ===\n")
cursor.execute("SELECT id, home_team, away_team FROM matches WHERE home_team LIKE '%POL%' OR away_team LIKE '%POL%'")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r[0]:3d} | Home: '{r[1]}' | Away: '{r[2]}'")

print("\n=== Primeros 10 partidos de la fase de grupos ===\n")
cursor.execute("SELECT id, home_team, away_team FROM matches ORDER BY id LIMIT 10")
rows = cursor.fetchall()
for r in rows:
    print(f"ID: {r[0]:3d} | Home: '{r[1]}' | Away: '{r[2]}'")

conn.close()
print("\n" + "="*60)
