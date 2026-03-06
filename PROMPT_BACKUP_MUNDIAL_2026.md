# PROMPT: Backup del Cronograma Mundial 2026

## Contexto

La base de datos actual contiene el cronograma **completo y definitivo** del Mundial 2026, con todos los datos necesarios:

- **104 partidos** distribuidos en 4 fases
- **48 equipos clasificados** con sus códigos FIFA correctos
- **Horarios confirmados** para todos los partidos (UTC)
- **Estructura de eliminación directa** con placeholders (1A, 2B, W27, etc.)

### Distribución de partidos:
- **Fecha 1**: 24 partidos (fase de grupos - primera jornada)
- **Fecha 2**: 24 partidos (fase de grupos - segunda jornada)  
- **Fecha 3**: 24 partidos (fase de grupos - tercera jornada)
- **Fecha 4**: 32 partidos (eliminación directa completa: Octavos, Cuartos, Semis, Final)

### Equipos clasificados (48 totales):
MEX, USA, CAN, ARG, BRA, URU, PAR, COL, ECU, CRC, PAN, HAI, ENG, FRA, ESP, GER, ITA, NED, POR, BEL, SUI, CRO, DEN, POL, AUT, SCO, WAL, NOR, MAR, TUN, ALG, EGY, SEN, GHA, CIV, RSA, CPV, IRN, KSA, QAT, JOR, JPN, KOR, AUS, NZL, CHN, UZB

### Placeholders en Fase 4 (Eliminación Directa):
- **Primeros y segundos de grupo**: 1A, 1B, 1C, 1D, 1E, 1F, 1G, 1H, 2A, 2B, 2C, 2D, 2E, 2F, 2G, 2H
- **Mejores terceros**: 3A/B/C, 3D/E/F, 3G/H/I
- **Ganadores de partidos**: W27, W28, W29, W30, W31, W32, etc.

Estos placeholders se resolverán automáticamente según los resultados de la fase de grupos.

## Objetivo del Backup

Crear un respaldo completo y permanente del cronograma del Mundial 2026 que incluya:

1. Todos los partidos con sus fechas/horarios
2. Todos los equipos (clasificados + placeholders)
3. La estructura de fases
4. Los cierres de pronósticos

Este backup servirá como **referencia oficial** del cronograma del Mundial 2026 y podrá restaurarse en cualquier momento si se necesita volver a esta configuración.

## Nombre del Backup

`backup_mundial_2026_cronograma_completo_YYYYMMDD_HHMMSS.db`

Donde YYYYMMDD_HHMMSS es la fecha/hora de creación del backup.

## Script Sugerido

```python
"""
Backup completo del cronograma del Mundial 2026
Incluye: 104 partidos, 48 equipos clasificados, 4 fases, horarios confirmados
"""
import shutil
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
        import os
        size_kb = os.path.getsize(dest) / 1024
        print(f"\nTamaño del backup: {size_kb:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")

if __name__ == "__main__":
    backup_mundial_2026()
```

## Cuándo Usar Este Backup

- Si se borran o modifican accidentalmente partidos del Mundial 2026
- Si se necesita restaurar el cronograma completo desde cero
- Si se experimenta con otras configuraciones y se quiere volver al original
- Como referencia para verificar horarios o estructura de fases
- Antes de hacer cambios importantes en la base de datos

## Notas Importantes

1. Este backup **NO incluye pronósticos de usuarios**, solo la estructura del torneo
2. Los horarios están en **UTC** (deben ajustarse según zona horaria del usuario)
3. El primer partido es **MEX vs RSA** el 11 de junio de 2026
4. La final es el **9 de agosto de 2026**
5. Los placeholders de Fase 4 se resolverán automáticamente según resultados

## Verificación Post-Backup

Después de crear el backup, verificar:
- ✓ Archivo existe en carpeta `backups/`
- ✓ Tamaño del archivo es razonable (~80-100 KB)
- ✓ Fecha en el nombre corresponde al momento de creación
- ✓ Puede abrirse con SQLite Browser si se necesita inspeccionar

## Ejecución Rápida

Para crear el backup inmediatamente:

```bash
python backup_mundial_2026_cronograma.py
```

El script está listo para ejecutarse y creará automáticamente el backup con toda la información necesaria.

---

**Última actualización:** Marzo 5, 2026  
**Estado:** Cronograma completo del Mundial 2026 con 48 equipos clasificados  
**Script:** `backup_mundial_2026_cronograma.py`
