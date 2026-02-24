# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('instance/prode.db')
cursor = conn.cursor()

print("\n=== VERIFICACIÓN DE USUARIOS ===\n")

# Ver todos los usuarios con su campo is_admin
cursor.execute("SELECT id, name, email, is_admin FROM users ORDER BY id")
users = cursor.fetchall()

print(f"Total usuarios: {len(users)}")
print("\nListado completo:")
for u in users:
    print(f"ID: {u[0]:2d} | {u[1]:20s} | is_admin: {u[3]} (tipo: {type(u[3]).__name__})")

# Contar por is_admin
cursor.execute("SELECT is_admin, COUNT(*) FROM users GROUP BY is_admin")
counts = cursor.fetchall()
print("\nResumen:")
for row in counts:
    print(f"  is_admin = {row[0]} : {row[1]} usuarios")

conn.close()
print("\n" + "="*60)
