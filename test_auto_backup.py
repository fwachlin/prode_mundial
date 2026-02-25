"""
🧪 Probar sistema de backups automáticos
"""
from app import app
from models import db, User, Match, Prediction
from datetime import datetime, timezone, timedelta
import os

print("=" * 80)
print("🧪 PRUEBA DE BACKUPS AUTOMÁTICOS")
print("=" * 80)

# Contar backups automáticos antes
auto_dir = 'backups/auto'
if os.path.exists(auto_dir):
    before_count = len([f for f in os.listdir(auto_dir) if f.endswith('.db')])
else:
    before_count = 0

print(f"\n📊 Backups automáticos antes: {before_count}")

with app.app_context():
    # Obtener un usuario de prueba y un partido
    user = User.query.filter_by(is_admin=False).first()
    match = Match.query.filter(Match.home_goals == None).first()
    
    if not user or not match:
        print("❌ No hay datos de prueba disponibles")
        print("   Ejecuta: python generar_datos_completos.py")
        exit(1)
    
    print(f"\n👤 Usuario de prueba: {user.name}")
    print(f"⚽ Partido de prueba: {match.home_team} vs {match.away_team}")
    
    # Crear o modificar pronóstico
    prediction = Prediction.query.filter_by(user_id=user.id, match_id=match.id).first()
    
    if prediction:
        print(f"\n🔄 Modificando pronóstico existente...")
        prediction.home_goals = 2
        prediction.away_goals = 1
    else:
        print(f"\n✨ Creando nuevo pronóstico...")
        prediction = Prediction(
            user_id=user.id,
            match_id=match.id,
            home_goals=1,
            away_goals=0
        )
        db.session.add(prediction)
    
    db.session.commit()
    print("✅ Pronóstico guardado en DB")
    
    # Llamar backup automático
    print("\n🔒 Ejecutando backup automático...")
    from auto_backup import backup_on_change
    backup_path = backup_on_change("pronostico_test")
    
    if backup_path:
        print(f"✅ Backup creado: {backup_path}")
    else:
        print("⚠️ Backup no creado (posible DB pequeña)")

# Contar backups después
if os.path.exists(auto_dir):
    after_count = len([f for f in os.listdir(auto_dir) if f.endswith('.db')])
    print(f"\n📊 Backups automáticos después: {after_count}")
    
    if after_count > before_count:
        print("✅ ¡Backup automático funcionando correctamente!")
        
        # Mostrar últimos 3 backups
        print("\n📂 Últimos backups automáticos:")
        backups = [(f, os.path.getmtime(os.path.join(auto_dir, f))) 
                   for f in os.listdir(auto_dir) if f.endswith('.db')]
        backups.sort(key=lambda x: x[1], reverse=True)
        
        for filename, mtime in backups[:3]:
            timestamp = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"   - {filename} ({timestamp})")
    else:
        print("⚠️ No se detectó nuevo backup")
else:
    print("❌ Carpeta backups/auto no existe")

print("\n" + "=" * 80)
print("🎉 PRUEBA COMPLETADA")
print("=" * 80 + "\n")
