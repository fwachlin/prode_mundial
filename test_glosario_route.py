"""Test para verificar que la ruta del glosario funciona correctamente"""
from app import app

with app.app_context():
    client = app.test_client()
    
    # GET /glosario
    response = client.get('/glosario')
    
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.content_type}")
    
    if response.status_code == 200:
        html = response.data.decode('utf-8')
        
        # Verificar que contiene el título correcto
        if 'Glosario de Equipos' in html:
            print("✓ Título correcto: 'Glosario de Equipos'")
        
        # Verificar que contiene algunos equipos conocidos
        equipos_test = ['ARG', 'BRA', 'MEX', 'WAL', 'POL']
        for equipo in equipos_test:
            if equipo in html:
                print(f"✓ {equipo} está en el glosario")
            else:
                print(f"✗ {equipo} NO está en el glosario")
        
        # Verificar que NO contiene CYP (que no está en los partidos)
        if 'CYP' not in html:
            print("✓ CYP no está en el glosario (correcto, no está en partidos)")
        else:
            print("✗ CYP está en el glosario (incorrecto)")
        
        # Contar cuántos equipos hay
        import re
        country_items = re.findall(r'<span class="country-code">(\w+)</span>', html)
        print(f"\nTotal de equipos en glosario: {len(country_items)}")
        print(f"Equipos: {', '.join(sorted(country_items)[:10])}...")
    else:
        print(f"ERROR: La ruta respondió con código {response.status_code}")
