#!/usr/bin/env python3
"""
🔒 VERIFICACIÓN DE SEGURIDAD PRE-COMMIT
Este script verifica que no se suban scripts destructivos accidentalmente
"""

import os
import sys

# Scripts que NO DEBEN existir en el proyecto
SCRIPTS_PROHIBIDOS = [
    '1_recrear_base_de_datos.py',
    'recrear_db_completa.py',
    'eliminar_todos_los_partidos.py',
]

# Palabras peligrosas en commits
PALABRAS_PELIGROSAS = [
    'db.drop_all()',
    'delete().delete()',
    '.delete_all()',
]

def verificar_scripts_prohibidos():
    """Verifica que no existan scripts prohibidos"""
    encontrados = []
    
    for script in SCRIPTS_PROHIBIDOS:
        if os.path.exists(script):
            encontrados.append(script)
    
    return encontrados

def main():
    print("🔒 Verificando seguridad del proyecto...")
    
    # Verificar scripts prohibidos
    prohibidos = verificar_scripts_prohibidos()
    
    if prohibidos:
        print("\n❌ ERROR: Scripts peligrosos detectados:")
        for script in prohibidos:
            print(f"   - {script}")
        print("\n⚠️  Estos scripts fueron eliminados por seguridad.")
        print("⚠️  NO los subas al repositorio.")
        sys.exit(1)
    
    print("✅ No se detectaron scripts peligrosos")
    print("✅ Verificación de seguridad completada\n")
    sys.exit(0)

if __name__ == '__main__':
    main()
