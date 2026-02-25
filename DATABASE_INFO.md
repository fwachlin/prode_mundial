# 📊 Información de Base de Datos

## Base de Datos Local

**Ubicación:** `instance/prode.db`

Esta es la ÚNICA base de datos local que usa la aplicación en desarrollo.

## 🎯 Generar Datos Ficticios Completos

Para regenerar la base de datos con datos de prueba:

```powershell
python generar_datos_completos.py
```

Esto crea:
- ✅ 4 fases (Fecha 1, 2, 3 y Eliminación Directa)
- ✅ 104 partidos del Mundial 2026
- ✅ 11 usuarios ficticios
- ✅ ~675 pronósticos (85% de cobertura - algunos usuarios sin pronosticar algunos partidos)

**Credenciales de usuarios ficticios:**
- Email: ana.martinez@prode.com (o cualquier otro email ficticio)
- Contraseña: prode123

### ⚠️ IMPORTANTE

- **NO crear archivos `.db` en la raíz del proyecto**
- **NO renombrar `prode.db`** - La app está configurada para usar este nombre
- La carpeta `instance/` está en `.gitignore` y NO se debe commitear

## Sincronización desde Render

Para sincronizar datos de producción a local:

```powershell
# 1. Obtener DATABASE_URL desde Render dashboard
# 2. Ejecutar:
$env:DATABASE_URL='postgresql://...'
python sync_db_from_render.py
```

Esto descargará todos los datos de Render y los copiará a `instance/prode.db`.

## Estructura de Archivos

```
prode_mundial/
├── instance/
│   └── prode.db          ← Base de datos local (SQLite)
├── sync_db_from_render.py ← Script de sincronización
└── app.py                ← Configuración apunta a instance/prode.db
```

## Variables de Entorno

### Desarrollo Local
No requiere `DATABASE_URL` - usa SQLite automáticamente en `instance/prode.db`

### Producción (Render)
Requiere `DATABASE_URL` configurada en Render dashboard → usa PostgreSQL

## Verificar Base de Datos

```powershell
# Ver usuarios
python check_users.py

# Ver contenido completo
python ver_db.py
```

## ⚠️ Si algo sale mal

1. **La app no encuentra datos:**
   - Verificar que existe `instance/prode.db`
   - Ejecutar `sync_db_from_render.py` si es necesario

2. **Bases de datos duplicadas:**
   - Solo debe existir `instance/prode.db`
   - Eliminar cualquier otro `.db` en la raíz

3. **Sincronización falla:**
   - Verificar que `DATABASE_URL` esté correcta (desde Render dashboard)
   - Credenciales pueden expirar periódicamente

## Última Sincronización

**Fecha:** 25 de Febrero, 2026
**Usuarios:** 12
**Partidos:** 104
**Pronósticos:** 541
