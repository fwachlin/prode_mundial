# 🎯 GUÍA RÁPIDA - Prode Mundial 2026

## 🚀 Inicio Rápido

### 1. Activar entorno virtual

```powershell
& e:\prode_mundial\venv\Scripts\Activate.ps1
```

### 2. Generar datos ficticios (primera vez)

```powershell
python generar_datos_completos.py
```

Esto crea:
- 11 usuarios ficticios (contraseña: `prode123`)
- 104 partidos del Mundial 2026
- ~675 pronósticos en fechas 1, 2, y 3

### 3. Ejecutar aplicación

```powershell
python app.py
```

Abrir: http://127.0.0.1:5000

### 4. Credenciales

**Admin:**
- Email: admin@prode.com
- Contraseña: admin123

**Usuarios ficticios:**
- Email: ana.martinez@prode.com (o cualquier otro)
- Contraseña: prode123

## 📁 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `app.py` | Aplicación principal Flask |
| `models.py` | Modelos de base de datos |
| `generar_datos_completos.py` | Genera datos ficticios completos |
| `auto_backup.py` | Sistema de backups automáticos |
| `sync_db_from_render.py` | Sincronizar desde producción |
| `check_users.py` | Ver usuarios en DB |
| `ver_db.py` | Ver todo el contenido de la DB |

## 🔒 Protecciones Implementadas

### Backups Automáticos
- Cada vez que ejecutas `python app.py`, se crea un backup
- Backups en `backups/` (últimos 10 se mantienen)

### Restaurar Backup
```powershell
python auto_backup.py restore
```

### Scripts Peligrosos
⚠️ **NUNCA ejecutar sin confirmación:**
- `1_recrear_base_de_datos.py` - **BORRA TODO**
- `recrear_db_completa.py` - **BORRA TODO**
- `eliminar_todos_los_partidos.py` - **BORRA PARTIDOS**

Ver `SCRIPTS_PELIGROSOS.md` para más info.

## 🧪 Tests

```powershell
# Todos los tests
pytest tests/

# Tests específicos
pytest tests/test_points.py
pytest tests/test_auth.py
```

## 🐛 Problemas Comunes

### "No hay pronósticos/usuarios"
```powershell
python generar_datos_completos.py
```

### "Base de datos vacía después de ejecutar Flask"
- Verifica que NO tengas `DATABASE_URL` en variables de entorno
- Ejecuta: `$env:DATABASE_URL=$null`

### "El fix de batacazo no se aplicó"
- Recarga resultados en admin panel
- O ejecuta: `python recalc_match1.py` (si existe)

## 📊 Verificar Estado

```powershell
# Ver usuarios
python check_users.py

# Ver base completa
python ver_db.py

# Verificar Render (producción)
$env:DATABASE_URL='postgresql://...'
python check_render_db.py
```

## 🔄 Workflow de Desarrollo

1. **Hacer cambios** en código
2. **Ejecutar tests**: `pytest tests/`
3. **Probar local**: `python app.py`
4. **Commit**: `git add . && git commit -m "Descripción"`
5. **Push**: `git push origin main`
6. Render despliega automáticamente

## 📝 Documentación Completa

- `PROJECT_RULES.md` - Reglas críticas del proyecto
- `SYSTEM_STATE.md` - Estado actual del sistema
- `TESTING_GUIDE.md` - Guía de tests
- `DATABASE_INFO.md` - Info de base de datos
- `DISASTER_RECOVERY.md` - Recuperación de desastres

## 💡 Tips

- ✅ Siempre leer PROJECT_RULES.md antes de cambios grandes
- ✅ Ejecutar tests después de cada cambio
- ✅ Usar `generar_datos_completos.py` para resetear datos locales
- ✅ Los backups automáticos te protegen de errores
- ❌ NUNCA ejecutar scripts destructivos sin leer el código

## 🆘 Ayuda

Si algo sale mal:
1. Verifica `DISASTER_RECOVERY.md`
2. Restaura último backup: `python auto_backup.py restore`
3. Regenera datos: `python generar_datos_completos.py`

---

**Última actualización:** 25 de Febrero, 2026
