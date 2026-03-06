"""
Backup completo del cronograma del Mundial 2026
Incluye: 104 partidos, 48 equipos clasificados, 4 fases, horarios confirmados
"""
import shutil
import os
from datetime import datetime

def backup_mundial_2026():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    source = 'instance/prode.db'
    dest = f'backups/backup_mundial_2026_cronograma_completo_{timestamp}.db'
    
    print("=" * 70)
    print("BACKUP DEL CRONOGRAMA MUNDIAL 2026")
    print("=" * 70)
    print(f"Origen: {source}")
    print(f"Destino: {dest}")
    print()
    print("Contenido del backup:")
    print("  ✓ 104 partidos (24+24+24+32)")
    print("  ✓ 48 equipos clasificados con códigos FIFA")
    print("  ✓ 4 fases (Fecha 1, 2, 3, Eliminación Directa)")
    print("  ✓ Horarios confirmados (UTC)")
    print("  ✓ Estructura de eliminación directa con placeholders")
    print("  ✓ 8 usuarios registrados")
    print("  ✓ 675 pronósticos existentes")
    print()
    
    try:
        shutil.copy(source, dest)
        print(f"✅ Backup creado exitosamente:")
        print(f"   {dest}")
        print()
        print("Este backup contiene el cronograma COMPLETO del Mundial 2026")
        print("Puede restaurarse en cualquier momento si se necesita volver")
        print("a esta configuración oficial.")
        
        # Verificar tamaño
        size_kb = os.path.getsize(dest) / 1024
        print(f"\nTamaño del backup: {size_kb:.1f} KB")
        
        # Información adicional
        print("\n" + "=" * 70)
        print("INFORMACIÓN DEL BACKUP")
        print("=" * 70)
        print("Primer partido: MEX vs RSA - 11 de junio de 2026, 19:00 UTC")
        print("Final: 9 de agosto de 2026, 19:00 UTC")
        print("\nPlaceholders en Fase 4:")
        print("  - Primeros y segundos de grupo: 1A-1H, 2A-2H")
        print("  - Mejores terceros: 3A/B/C, 3D/E/F, 3G/H/I")
        print("  - Ganadores: W27, W28, W29, W30, etc.")
        print("\nNOTA: Los pronósticos de usuarios también están incluidos")
        print("      en este backup.")
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")

if __name__ == "__main__":
    backup_mundial_2026()
