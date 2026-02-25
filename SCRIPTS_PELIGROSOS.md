# 🔒 SCRIPTS PELIGROSOS - NO EJECUTAR SIN CONFIRMACIÓN

Esta carpeta contiene scripts que BORRAN o RECREAN la base de datos.

## ⚠️ NUNCA ejecutar estos scripts:

- `1_recrear_base_de_datos.py` - **BORRA TODO**
- `recrear_db_completa.py` - **BORRA TODO**
- `eliminar_todos_los_partidos.py` - **BORRA PARTIDOS**

## ✅ Scripts seguros para usar:

- `ver_db.py` - Ver contenido (solo lectura)
- `check_users.py` - Ver usuarios (solo lectura)
- `sync_db_from_render.py` - Sincronizar DE Render a local (no afecta Render)

## 🔄 Si necesitas restaurar datos:

1. Ve a Render Dashboard → Database → Backups
2. Restaura el backup más reciente
3. Ejecuta localmente: `python sync_db_from_render.py`

## 🆘 Si borraste datos por error:

1. Ejecuta: `python auto_backup.py restore`
2. Esto restaurará el último backup automático

## 💾 Backups automáticos:

Cada vez que ejecutas `python app.py`, se crea un backup automático en `backups/`
