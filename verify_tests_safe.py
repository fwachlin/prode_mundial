#!/usr/bin/env python
"""
Script de verificación de seguridad de tests

Confirma que los tests están configurados para NO afectar la base de datos real.

Ejecutar ANTES de pytest para estar seguro:
    python verify_tests_safe.py && pytest tests/
"""

import sys
import os

def verify_conftest_safety():
    """Verifica que conftest.py esté configurado de manera segura"""
    print("🔍 Verificando configuración de tests...")
    
    conftest_path = os.path.join('tests', 'conftest.py')
    
    if not os.path.exists(conftest_path):
        print("❌ ERROR: No se encuentra tests/conftest.py")
        return False
    
    with open(conftest_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificaciones críticas
    checks = [
        ("'sqlite:///:memory:'", "Base de datos en memoria"),
        ("'TESTING': True", "Modo testing activado"),
        ("from flask import Flask", "Crea app nueva (no importa app.py)"),
        ("test_app = Flask", "Instancia independiente"),
    ]
    
    failed_checks = []
    
    for check_string, description in checks:
        if check_string in content:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description} - NO ENCONTRADO")
            failed_checks.append(description)
    
    # Verificar que NO importa la app real
    if 'from app import app' in content or 'import app' in content:
        print(f"  ❌ PELIGRO: conftest.py importa app.py directamente")
        failed_checks.append("Import directo de app")
    else:
        print(f"  ✅ NO importa app.py directamente")
    
    return len(failed_checks) == 0


def verify_no_db_file_in_tests():
    """Verifica que los tests no mencionen archivos de DB"""
    print("\n🔍 Verificando que tests no usen archivos de DB...")
    
    test_files = []
    for root, dirs, files in os.walk('tests'):
        for file in files:
            if file.endswith('.py') and file.startswith('test_'):
                test_files.append(os.path.join(root, file))
    
    dangerous_patterns = [
        'instance/prode.db',
        'prode.db',
        'sqlite:///instance',
    ]
    
    issues_found = []
    
    for test_file in test_files:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for pattern in dangerous_patterns:
            if pattern in content:
                issues_found.append(f"{test_file} contiene '{pattern}'")
    
    if issues_found:
        print("  ❌ Archivos de DB mencionados en tests:")
        for issue in issues_found:
            print(f"    - {issue}")
        return False
    else:
        print("  ✅ Ningún test menciona archivos de DB")
        return True


def verify_db_exists():
    """Verifica que la base de datos real existe (no fue borrada)"""
    print("\n🔍 Verificando que base de datos real existe...")
    
    db_path = os.path.join('instance', 'prode.db')
    
    if not os.path.exists(db_path):
        print(f"  ⚠️  ADVERTENCIA: {db_path} no existe")
        print("     Esto podría ser normal si es primera ejecución")
        return True  # No falla, solo advierte
    
    file_size = os.path.getsize(db_path)
    
    if file_size < 1000:  # DB vacía es sospechosa
        print(f"  ⚠️  ADVERTENCIA: {db_path} es muy pequeña ({file_size} bytes)")
        return True
    
    print(f"  ✅ {db_path} existe ({file_size:,} bytes)")
    return True


def main():
    print("=" * 70)
    print("🛡️  VERIFICACIÓN DE SEGURIDAD DE TESTS")
    print("=" * 70)
    
    all_ok = True
    
    all_ok = verify_conftest_safety() and all_ok
    all_ok = verify_no_db_file_in_tests() and all_ok
    all_ok = verify_db_exists() and all_ok
    
    print("\n" + "=" * 70)
    
    if all_ok:
        print("✅ VERIFICACIÓN EXITOSA: Es seguro ejecutar pytest")
        print("   Los tests NO afectarán la base de datos real")
        print("\n   Ejecuta: pytest tests/")
        print("=" * 70)
        return 0
    else:
        print("❌ VERIFICACIÓN FALLIDA: NO ejecutar pytest")
        print("   Revisa la configuración antes de continuar")
        print("=" * 70)
        return 1


if __name__ == '__main__':
    sys.exit(main())
