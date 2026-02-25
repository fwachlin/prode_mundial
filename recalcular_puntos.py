"""
Script para recalcular todos los puntos después de corregir la fórmula de cálculo.

USO:
    python recalcular_puntos.py

IMPORTANTE: Ejecutar después de desplegar las correcciones en producción.
"""
from app import app
from models import db, Match, Prediction

def recalcular_todos_los_puntos():
    """Recalcula los puntos de todos los pronósticos en partidos con resultado"""
    with app.app_context():
        # Obtener todos los partidos con resultado cargado
        matches_con_resultado = Match.query.filter(
            Match.home_goals.isnot(None),
            Match.away_goals.isnot(None)
        ).all()
        
        if not matches_con_resultado:
            print("❌ No hay partidos con resultados cargados")
            return
        
        print(f"📊 Encontrados {len(matches_con_resultado)} partidos con resultado")
        print("🔄 Recalculando puntos...\n")
        
        total_predictions = 0
        partidos_procesados = 0
        
        for match in matches_con_resultado:
            partidos_procesados += 1
            predictions = match.predictions
            
            if not predictions:
                print(f"  {partidos_procesados}. {match.home_team} {match.home_goals}-{match.away_goals} {match.away_team} - Sin pronósticos")
                continue
            
            print(f"  {partidos_procesados}. {match.home_team} {match.home_goals}-{match.away_goals} {match.away_team} - {len(predictions)} pronósticos")
            
            # Recalcular puntos para cada pronóstico
            for pred in predictions:
                puntos_viejos = pred.points_awarded
                puntos_nuevos = pred.calculate_points()
                pred.points_awarded = puntos_nuevos
                total_predictions += 1
                
                if puntos_viejos != puntos_nuevos:
                    print(f"     ├─ {pred.user.name}: {puntos_viejos} → {puntos_nuevos} puntos")
        
        # Guardar cambios
        db.session.commit()
        
        print(f"\n✅ Recalculados {total_predictions} pronósticos en {partidos_procesados} partidos")
        print("💾 Cambios guardados en la base de datos")

if __name__ == '__main__':
    print("=" * 70)
    print("🔧 RECALCULACIÓN DE PUNTOS - Prode Mundial 2026")
    print("=" * 70)
    print("\nEste script recalcula los puntos de todos los pronósticos usando")
    print("la fórmula corregida (batacazos sobre total participantes + score")
    print("para quienes fallan ganador).\n")
    
    respuesta = input("¿Continuar con la recalculación? (s/n): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        recalcular_todos_los_puntos()
    else:
        print("\n❌ Recalculación cancelada")
