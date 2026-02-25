# ⚠️ SCRIPTS PELIGROSOS - NO EJECUTAR

## 🚨 ADVERTENCIA CRÍTICA

Los siguientes scripts **HAN SIDO ELIMINADOS** del proyecto después de causar pérdidas de datos catastróficas:

### Scripts Eliminados (25/Feb/2026)

1. ❌ `1_recrear_base_de_datos.py` - ELIMINADO
2. ❌ `recrear_db_completa.py` - ELIMINADO  
3. ❌ `eliminar_todos_los_partidos.py` - ELIMINADO

**Motivo:** Estos scripts borraban todos los datos sin protecciones adecuadas.

---

## ✅ Scripts SEGUROS que SÍ puedes usar:

### Regeneración de Datos (Solo si la DB está vacía)
```bash
python generar_datos_completos.py
```
- Genera 11 usuarios ficticios + 104 partidos + 675 pronósticos
- Solo para desarrollo/testing
- **NO ejecutar en producción con datos reales**

### Backups
```bash
# Crear backup manual (antes de cualquier operación riesgosa)
python auto_backup.py

# Restaurar último backup
python auto_backup.py restore
```

### Sincronización Render
```bash
# Bajar de Render a Local (SEGURO - no afecta Render)
python backup_from_render.py

# Subir de Local a Render (PELIGROSO - requiere confirmación)
python upload_to_render.py
# Requiere escribir "CONFIRMAR" manualmente
```

### Ver estado (SOLO LECTURA - SEGURO)
```bash
python check_users.py
python ver_db.py
python verificar_datos.py
```

---

## 🔒 Reglas de Oro

1. **NUNCA ejecutar scripts que no conoces completamente**
2. **SIEMPRE hacer backup antes de cualquier operación**
3. **NUNCA ejecutar `generar_datos_completos.py` con datos reales**
4. **Si algo borra datos, ELIMINAR el script inmediatamente**

---

## 📞 En caso de pérdida de datos

1. Verificar backups: `dir backups/`
2. Restaurar: `python auto_backup.py restore`
3. Si backups no sirven: `python generar_datos_completos.py`
4. Subir a Render: `python upload_to_render.py` (escribir CONFIRMAR)

---

**Última actualización:** 25 de Febrero, 2026  
**Incidentes de pérdida de datos:** 2 (ambos resueltos)
