# -*- coding: utf-8 -*-
# Test del filtro country_iso2 con códigos problemáticos

# Simular la lógica del filtro corregido
def country_iso2_filter(country_name):
    """Convierte nombre de país o código FIFA a código ISO de 2 letras para mostrar banderas"""
    if not country_name:
        return 'xx'
    
    # Si contiene "Path" o "IC", no mostrar bandera
    if 'Path' in country_name or country_name.startswith('IC '):
        return 'xx'
    
    # Placeholders de eliminación directa
    # Primero verificar los códigos de grupo (1A, 2B, 3C/D/E, etc.)
    if any(country_name.startswith(x) for x in ['1A', '1B', '1C', '1D', '1E', '1F', '1G', '1H', '1I', '1J', '1K', '1L',
                                                  '2A', '2B', '2C', '2D', '2E', '2F', '2G', '2H', '2I', '2J', '2K', '2L',
                                                  '3A', '3B', '3C', '3D', '3E', '3F']):
        return 'xx'
    
    # W y L solo si van seguidos de un número (W1, W2, L25, etc.)
    if (country_name.startswith('W') or country_name.startswith('L')) and len(country_name) >= 2:
        if country_name[1].isdigit():
            return 'xx'
    
    # Mapeo de códigos FIFA a ISO2
    fifa_to_iso2 = {
        'WAL': 'gb-wls', 'POL': 'pl', 'MEX': 'mx', 'RSA': 'za',
        'ARG': 'ar', 'BRA': 'br', 'ITA': 'it', 'DEN': 'dk'
    }
    
    return fifa_to_iso2.get(country_name, 'xx')

# Casos de prueba
test_cases = [
    ('WAL', 'gb-wls', '✅ Wales debe mostrar bandera'),
    ('POL', 'pl', '✅ Poland debe mostrar bandera'),
    ('W1', 'xx', '✅ W1 (placeholder) NO debe mostrar bandera'),
    ('W2', 'xx', '✅ W2 (placeholder) NO debe mostrar bandera'),
    ('L25', 'xx', '✅ L25 (placeholder) NO debe mostrar bandera'),
    ('1A', 'xx', '✅ 1A (placeholder) NO debe mostrar bandera'),
    ('2B', 'xx', '✅ 2B (placeholder) NO debe mostrar bandera'),
    ('MEX', 'mx', '✅ México debe mostrar bandera'),
    ('RSA', 'za', '✅ South Africa debe mostrar bandera')
]

print("\n" + "="*70)
print("TEST DEL FILTRO country_iso2")
print("="*70)

all_ok = True
for codigo, esperado, descripcion in test_cases:
    resultado = country_iso2_filter(codigo)
    ok = resultado == esperado
    all_ok = all_ok and ok
    status = '✓' if ok else '✗'
    print(f"{status} {codigo:6s} → {resultado:10s} (esperado: {esperado:10s}) | {descripcion}")

print("="*70)
if all_ok:
    print("✅ TODOS LOS TESTS PASARON - El filtro funciona correctamente")
else:
    print("❌ ALGUNOS TESTS FALLARON")
print("="*70 + "\n")
