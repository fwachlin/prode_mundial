"""Test WAL específicamente"""
from fifa_countries import get_fifa_code, get_country_iso2, get_country_name

print("=== TEST WAL ===")
print(f"get_country_iso2('WAL'): '{get_country_iso2('WAL')}'")
print(f"get_country_name('WAL'): '{get_country_name('WAL')}'")
print(f"get_fifa_code('Gales'): '{get_fifa_code('Gales')}'")

print("\n=== TEST ENG ===")
print(f"get_country_iso2('ENG'): '{get_country_iso2('ENG')}'")
print(f"get_country_name('ENG'): '{get_country_name('ENG')}'")

print("\n=== TEST SCO ===")
print(f"get_country_iso2('SCO'): '{get_country_iso2('SCO')}'")
print(f"get_country_name('SCO'): '{get_country_name('SCO')}'")

# Verificar si el problema es con códigos que no existen
print("\n=== TEST Código inválido ===")
print(f"get_country_iso2('XYZ'): '{get_country_iso2('XYZ')}'")
print(f"get_country_name('XYZ'): '{get_country_name('XYZ')}'")
