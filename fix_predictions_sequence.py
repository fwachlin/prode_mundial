"""
Script para sincronizar la secuencia de autoincremento de la tabla predictions
Soluciona el error de clave duplicada en PostgreSQL.
"""
from extensions import db
from app import app
from sqlalchemy import text

if __name__ == "__main__":
    with app.app_context():
        # Ajusta el nombre de la secuencia si usas otro nombre en tu base
        sql = text("SELECT setval('predictions_id_seq', (SELECT COALESCE(MAX(id), 1) FROM predictions));")
        db.session.execute(sql)
        db.session.commit()
        print("Secuencia predictions_id_seq sincronizada correctamente.")
