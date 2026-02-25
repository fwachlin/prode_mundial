# 🆘 GUÍA DE RECUPERACIÓN DE DESASTRES

## Situación: Base de datos borrada accidentalmente

### ✅ PASO 1: Verificar si hay backup local

```powershell
python auto_backup.py restore
```

Esto restaurará el último backup automático si existe.

### ✅ PASO 2: Verificar Render tiene backups

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Selecciona tu servicio PostgreSQL
3. Ve a la pestaña "Backups"
4. Si hay backups disponibles, haz clic en "Restore"

### ✅ PASO 3: Sincronizar desde Render

Una vez restaurado Render, sincroniza a local:

```powershell
$env:DATABASE_URL='postgresql://...'
python sync_db_from_render.py
```

## 🔒 Protecciones Implementadas

### 1. Backup Automático
- Cada vez que ejecutas `python app.py`, se crea backup automático
- Backups se guardan en `backups/` (ignorado por git)
- Se mantienen los últimos 10 backups

### 2. Scripts Peligrosos Documentados
- Ver `SCRIPTS_PELIGROSOS.md` para lista de scripts que borran datos
- **NUNCA** ejecutar sin estar 100% seguro

### 3. .gitignore Actualizado
- `backups/` NO se sube a GitHub
- `instance/` NO se sube a GitHub

## 📋 Checklist de Prevención

Antes de ejecutar CUALQUIER script:

- [ ] ¿El script tiene "recrear", "eliminar" o "borrar" en el nombre?
- [ ] ¿Leíste el código completo del script?
- [ ] ¿Tienes un backup reciente?
- [ ] ¿Esto es en producción o desarrollo?
- [ ] **Si tienes dudas, NO LO EJECUTES**

## 🔍 Verificar estado de la base de datos

```powershell
# Local
python check_users.py

# Render
$env:DATABASE_URL='postgresql://...'
python check_render_db.py
```

## 📞 Contactos de Emergencia

- **Render Support**: https://render.com/support
- **Dashboard Render**: https://dashboard.render.com

## 📝 Lecciones Aprendidas

1. ✅ NUNCA ejecutar scripts sin leer el código
2. ✅ SIEMPRE tener backups automáticos
3. ✅ SIEMPRE verificar qué hace un script antes de ejecutarlo
4. ✅ Los scripts destructivos deberían requerir confirmación explícita
