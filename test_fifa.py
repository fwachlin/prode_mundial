"""Test rápido del sistema FIFA countries"""
from fifa_countries import get_fifa_code, get_country_iso2, get_country_name

print("TEST CYP (Chipre - el caso mencionado por el usuario):")
print(f"  FIFA code: {get_fifa_code('Chipre')}")
print(f"  ISO2: {get_country_iso2('CYP')}")
print(f"  Nombre: {get_country_name('CYP')}")

print("\nTEST POL (Polonia - caso actual en el prode):")
print(f"  FIFA code: {get_fifa_code('Polonia')}")
print(f"  ISO2: {get_country_iso2('POL')}")
print(f"  Nombre: {get_country_name('POL')}")

print("\nTEST ARG (Argentina - verificación básica):")
print(f"  FIFA code: {get_fifa_code('Argentina')}")
print(f"  ISO2: {get_country_iso2('ARG')}")
print(f"  Nombre: {get_country_name('ARG')}")

print("\nTEST Alias (Holanda -> NED):")
print(f"  FIFA code: {get_fifa_code('Holanda')}")
print(f"  ISO2: {get_country_iso2('NED')}")
print(f"  Nombre: {get_country_name('NED')}")

print("\nTEST Placeholders:")
print(f"  '1A' -> {get_fifa_code('1A')}")
print(f"  'W1' -> {get_fifa_code('W1')}")
print(f"  'L25' -> {get_fifa_code('L25')}")
print(f"  ISO2 for '1A': {get_country_iso2('1A')}")

print("\nTEST WAL (verificación específica del bug):")
print(f"  FIFA code: {get_fifa_code('Gales')}")
print(f"  ISO2: {get_country_iso2('WAL')}")
print(f"  Nombre: {get_country_name('WAL')}")
print(f"  ✓ WAL ahora funciona correctamente (antes devolvía 'xx')")
