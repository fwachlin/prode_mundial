# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('instance/prode.db')
cursor = conn.cursor()

print("\n=== VERIFICACIÓN DE DATOS ===\n")

# Usuarios
cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 0")
num_users = cursor.fetchone()[0]
print(f"Usuarios (no admin): {num_users}")

# Partidos
cursor.execute("SELECT COUNT(*) FROM matches")
num_matches = cursor.fetchone()[0]
print(f"Partidos totales: {num_matches}")

# Pronósticos
cursor.execute("SELECT COUNT(*) FROM predictions")
num_predictions = cursor.fetchone()[0]
print(f"Pronósticos totales: {num_predictions}")

# Primeros 5 usuarios
print("\n=== Primeros 5 usuarios ===")
cursor.execute("SELECT id, name, email, is_admin FROM users LIMIT 5")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | {row[1]} | {row[2]} | Admin: {row[3]}")

# Primeros 10 pronósticos
print("\n=== Primeros 10 pronósticos ===")
cursor.execute("""
    SELECT p.id, u.name, m.home_team, m.away_team, p.home_goals, p.away_goals
    FROM predictions p
    JOIN users u ON p.user_id = u.id
    JOIN matches m ON p.match_id = m.id
    LIMIT 10
""")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | {row[1]:20s} | {row[2]} vs {row[3]} | {row[4]}-{row[5]}")

conn.close()
print("\n" + "="*60)
