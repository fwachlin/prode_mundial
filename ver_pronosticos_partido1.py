# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('instance/prode.db')
cursor = conn.cursor()

# Obtener ID del primer partido (MEX vs RSA)
cursor.execute("SELECT id, home_team, away_team FROM matches ORDER BY kickoff_at LIMIT 1")
match = cursor.fetchone()
match_id = match[0]
print(f"\nPrimer partido: ID {match_id} - {match[1]} vs {match[2]}")

# Ver qué usuarios tienen pronósticos para este partido
print("\nPronósticos para este partido:")
cursor.execute("""
    SELECT u.id, u.name, p.home_goals, p.away_goals
    FROM predictions p
    JOIN users u ON p.user_id = u.id
    WHERE p.match_id = ?
""", (match_id,))

rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"  {row[1]:20s} - {row[2]}-{row[3]}")
else:
    print("  ¡No hay pronósticos para este partido!")

# Ver cuántos pronósticos hay por partido en Fecha 1
print("\nResumen de pronósticos por partido (primeros 10):")
cursor.execute("""
    SELECT m.id, m.home_team, m.away_team, COUNT(p.id) as num_pred
    FROM matches m
    LEFT JOIN predictions p ON m.id = p.match_id
    WHERE m.phase_id = 1
    GROUP BY m.id
    ORDER BY m.kickoff_at
    LIMIT 10
""")

for row in cursor.fetchall():
    print(f"  ID {row[0]:3d} - {row[1]} vs {row[2]:6s} : {row[3]} pronósticos")

conn.close()
