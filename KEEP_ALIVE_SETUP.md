# 🔄 Sistema de Keep-Alive para Supabase

## Problema
Supabase pausa proyectos gratuitos sin actividad por más de 7 días.

## Solución
GitHub Actions ejecuta automáticamente un script cada 3 días que hace una query simple a la base de datos, manteniéndola activa.

## Configuración (Una sola vez)

### 1. Agregar SECRET en GitHub

1. Ve a tu repositorio en GitHub: https://github.com/fwachlin/prode_mundial
2. Click en **Settings** (configuración)
3. En el menú izquierdo, click en **Secrets and variables** → **Actions**
4. Click en **New repository secret**
5. Nombre del secret: `DATABASE_URL`
6. Valor: Tu connection string de Supabase (el mismo que usas en Render)
   - Formato: `postgresql://postgres.xxxxx:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres`
7. Click en **Add secret**

### 2. Habilitar GitHub Actions

1. Ve a la pestaña **Actions** en tu repositorio
2. Si aparece un botón para habilitar workflows, haz click en él
3. Listo! El workflow ya está configurado

## Funcionamiento

- **Automático**: Se ejecuta cada 3 días a las 3:00 AM UTC
- **Manual**: También puedes ejecutarlo manualmente desde la pestaña Actions → "Mantener Supabase Activo" → "Run workflow"
- **Gratis**: GitHub Actions incluye 2000 minutos/mes gratis (esto usa ~1 minuto/mes)

## Archivos

- `keep_alive_db.py`: Script Python que hace la query
- `.github/workflows/keep-alive.yml`: Workflow de GitHub Actions

## Verificación

Para verificar que funciona:

1. Ve a la pestaña **Actions** en GitHub
2. Busca el workflow "Mantener Supabase Activo"
3. Ejecuta manualmente: **Run workflow** → **Run workflow**
4. Espera 30 segundos y actualiza la página
5. Deberías ver ✅ green check si funcionó

## Próximos Emails de Supabase

Después de configurar esto, **NO** deberías recibir más emails de pausa de Supabase, ya que habrá actividad cada 3 días.

Si recibes otro email, ejecuta el workflow manualmente desde Actions y verifica el log para ver si hay errores.
