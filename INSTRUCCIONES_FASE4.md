# Instrucciones para agregar los 32 partidos de Fase 4 en Render

## Problema
Tu base de datos local tiene 104 partidos (72 de fase de grupos + 32 de eliminación directa), pero en Render solo hay 72 partidos (solo fase de grupos).

## Solución

### Opción 1: Ejecutar script en Render Shell

1. Ve a tu aplicación en Render (https://dashboard.render.com)
2. Selecciona tu servicio web
3. En el menú izquierdo, haz clic en "Shell"
4. Ejecuta el siguiente comando:

```bash
python agregar_fase4_render.py
```

Esto agregará los 32 partidos faltantes de la Fase 4.

### Opción 2: Crear un endpoint temporal

Si no tienes acceso al Shell de Render, puedes crear un endpoint temporal para ejecutar el script:

1. El archivo `agregar_fase4_render.py` ya está listo
2. Haz push a GitHub
3. Espera que Render depliegue
4. Accede a: `https://tu-app.onrender.com/admin/agregar-fase4` (necesitas estar logueado como admin)
5. Después de ejecutar, elimina el endpoint por seguridad

### Verificación

Después de ejecutar el script, verifica:
- Total de partidos: debe ser 104
- Partidos de Fase 4: debe ser 32
- En la vista de admin, deberías ver todos los partidos de eliminación directa (1A vs 2B, W1 vs W2, etc.)

## Archivos relacionados

- `agregar_fase4.py` - Script con confirmación interactiva (para uso local)
- `agregar_fase4_render.py` - Script sin interacción (para Render)
- `carga_partidos_mundial_2026.py` - Script completo con todos los 104 partidos (alternativa: borrar todo y volver a cargar)
