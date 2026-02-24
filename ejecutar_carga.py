# -*- coding: utf-8 -*-
import subprocess
import sys

result = subprocess.run([sys.executable, 'carga_partidos_mundial_2026.py'], 
                       capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
if result.stderr:
    print(result.stderr)
print(f"\nCodigo de salida: {result.returncode}")
