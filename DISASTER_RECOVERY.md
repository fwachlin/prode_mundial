# 🚨 PLAN DE RECUPERACIÓN DE DESASTRES - ACTUALIZADO

## 📋 HISTORIAL DE INCIDENTES

### ⚠️ Incidente #1: 25/Feb/2026 - 17:00 UTC
- **Causa:** Ejecución accidental de script destructivo
- **Daño:** Pérdida total de usuarios y pronósticos (local y producción)
- **Resolución:** Regeneración con `generar_datos_completos.py` + upload a Render
- **Duración:** ~20 minutos
- **Lección aprendida:** Necesidad de eliminar scripts destructivos

### ⚠️ Incidente #2: 25/Feb/2026 - 17:54 UTC
- **Causa:** Ejecución accidental de script destructivo (segunda vez)
- **Daño:** Pérdida total de usuarios y pronósticos (local y producción)
- **Resolución:** Regeneración con `generar_datos_completos.py` + upload a Render
- **Duración:** ~10 minutos
- **Acciones correctivas implementadas:**
  - ✅ Scripts destructivos ELIMINADOS permanentemente del proyecto
  - ✅ Confirmación doble agregada a `generar_datos_completos.py`
  - ✅ Documentación `PELIGRO_NO_EJECUTAR.md` creada
  - ✅ Script `verificar_seguridad.py` para pre-commit checks

---

## 🔒 PROTECCIONES IMPLEMENTADAS (25/Feb/2026 - 18:00 UTC)

### ❌ Scripts ELIMINADOS Permanentemente
Estos scripts fueron eliminados del proyecto por causar pérdidas de datos:

1. `1_recrear_base_de_datos.py` - Borraba toda la DB sin confirmación
2. `recrear_db_completa.py` - Borraba toda la DB sin protección adecuada
3. `eliminar_todos_los_partidos.py` - Borraba todos los partidos sin backup

**Si ves estos archivos nuevamente, ELIMÍNALOS inmediatamente.**

### ✅ Scripts PROTEGIDOS con Confirmación Doble

**`generar_datos_completos.py`** - Ahora requiere:
1. Primera confirmación: escribir "REGENERAR" exactamente
2. Segunda confirmación: escribir "SI BORRA TODO" exactamente
3. Advertencias claras de que BORRA TODOS LOS DATOS

**`upload_to_render.py`** - Ya tenía protección:
1. Confirmación: escribir "CONFIRMAR" exactamente
2. Advertencia de que afecta producción

### 📄 Nuevos Archivos de Seguridad

- **`PELIGRO_NO_EJECUTAR.md`** - Lista scripts eliminados y guía de uso seguro
- **`verificar_seguridad.py`** - Verifica que no se suban scripts peligrosos (futuro pre-commit hook)

---

## ⚡ PROTOCOLO DE RESPUESTA RÁPIDA

### 🆘 PÉRDIDA DE DATOS DETECTADA

#### PASO 0: MANTENER LA CALMA
Los datos pueden recuperarse. No entres en pánico. Lee este documento completo.

#### PASO 1: Verificar el Daño
```powershell
# Verificar usuarios
python check_users.py

# Verificar tablas completas
python ver_db.py
```

**Posibles resultados:**
- Solo admin existe → Pérdida total
- Algunos usuarios faltan → Pérdida parcial
- Datos corruptos → Necesita regeneración

#### PASO 2: Verificar Backups Locales
```powershell
# Listar backups disponibles
dir backups/

# Debe mostrar archivos como:
# prode_backup_20260225_170940.db
```

#### PASO 3: Restaurar desde Backup Local
```powershell
# Restaurar último backup
python auto_backup.py restore

# Verificar restauración exitosa
python check_users.py
```

**Si restauración exitosa:** Continuar a PASO 6

**Si backup solo tiene admin:** Continuar a PASO 4

#### PASO 4: Regenerar Datos (Solo si backups no sirven)
```powershell
python generar_datos_completos.py
```

**Confirmaciones requeridas:**
1. Escribir: `REGENERAR`
2. Escribir: `SI BORRA TODO`

**Esto genera:**
- 11 usuarios ficticios (contraseña: prode123)
- 104 partidos del Mundial 2026
- 675 pronósticos distribuidos (85% cobertura)

#### PASO 5: Subir a Render (Si producción también perdió datos)
```powershell
# Configurar conexión a Render
$env:DATABASE_URL='postgresql://prode_mundial:4FM5AsLilp3l74lYtdcUL9weMP0QQVBS@dpg-d6f159ngi27c7395f1n0-a.oregon-postgres.render.com/prode_mundial_4uj0'

# Ejecutar upload
python upload_to_render.py

# Escribir cuando pregunte: CONFIRMAR
```

**Esperar:** 3-5 minutos (675 pronósticos toman tiempo)

#### PASO 6: Verificación Post-Recuperación

**Local:**
```powershell
python check_users.py
# Debe mostrar: 12 usuarios (1 admin + 11 ficticios)

python ver_db.py
# Debe mostrar: 104 partidos, 675 pronósticos, 4 fases
```

**Render/Producción:**
1. Abrir sitio web en navegador
2. Login: admin@prode.com / admin123
3. Ir a `/admin/dashboard`
4. Verificar:
   - Usuarios: 11 (excluye admin del conteo)
   - Partidos: 104
   - Pronósticos: 675

#### PASO 7: Crear Backup Inmediato
```powershell
# Backup del estado restaurado
python auto_backup.py

# Si Render está bien, backup desde Render
python backup_from_render.py
```

---

## 🛡️ PREVENCIÓN: REGLAS DE ORO

### ❌ NUNCA

1. **NUNCA ejecutar scripts sin leer el código completo**
   - Especialmente si tienen "recrear", "eliminar", "borrar" en el nombre

2. **NUNCA saltarte confirmaciones**
   - "s", "y", "si" NO son válidos
   - Solo respuestas EXACTAS: "CONFIRMAR", "REGENERAR", "SI BORRA TODO"

3. **NUNCA ejecutar `generar_datos_completos.py` con datos reales**
   - Este script BORRA TODO
   - Solo para desarrollo/testing

4. **NUNCA confiar en que "Ctrl+Z" funciona en bases de datos**
   - Las operaciones de DB son permanentes
   - Siempre backup primero

### ✅ SIEMPRE

1. **SIEMPRE hacer backup antes de operaciones riesgosas**
   ```powershell
   python auto_backup.py
   python backup_from_render.py  # Si vas a modificar producción
   ```

2. **SIEMPRE leer advertencias completas**
   - Si un script muestra advertencia ⚠️, léela TODA

3. **SIEMPRE verificar antes y después**
   ```powershell
   # Antes
   python check_users.py
   
   # Después
   python check_users.py
   ```

4. **SIEMPRE probar en local antes de producción**
   - Cambios de código → Local primero
   - Si funciona local → Deploy a Render

5. **SIEMPRE usar confirmaciones EXACTAS**
   - Escribir "CONFIRMAR" completo, no "c" o "confirmar"
   - Esto previene ejecuciones accidentales

---

## 📊 SCRIPTS SEGUROS POR CATEGORÍA

### 🟢 100% SEGURO (Solo Lectura)
```powershell
python check_users.py        # Lista usuarios
python ver_db.py             # Muestra todo el contenido
python verificar_datos.py    # Valida integridad
python verificar_seguridad.py # Verifica scripts peligrosos
```

### 🟡 SEGURO (Backups - No modifica origen)
```powershell
python auto_backup.py              # Backup local manual
python auto_backup.py restore      # Restaurar último backup
python backup_from_render.py       # Render → Local (NO afecta Render)
```

### 🟠 CUIDADO (Requiere Confirmación Explícita)
```powershell
python upload_to_render.py         # Local → Render (requiere "CONFIRMAR")
                                   # Afecta producción, usa con precaución
```

### 🔴 PELIGROSO (Requiere 2 Confirmaciones)
```powershell
python generar_datos_completos.py  # BORRA TODO y regenera
                                   # Requiere "REGENERAR" y "SI BORRA TODO"
                                   # SOLO para desarrollo
```

---

## 📅 RUTINA DE BACKUPS RECOMENDADA

### Backups Automáticos (Ya Implementados)
- ✅ **Cada inicio de Flask** (`python app.py`)
- ✅ Carpeta: `backups/`
- ✅ Retención: Últimos 10 backups
- ✅ Formato: `prode_backup_YYYYMMDD_HHMMSS.db`

### Backups Manuales (Responsabilidad del Admin)

**Diario durante Mundial:**
```powershell
python backup_from_render.py
```

**Antes de:**
- ✅ Cargar resultados de partidos importantes
- ✅ Cambios grandes en código
- ✅ Ejecutar cualquier script que modifique datos
- ✅ Actualizar versión de Flask/SQLAlchemy
- ✅ Cambiar estructura de base de datos

**Después de:**
- ✅ Cargar resultados de una fecha completa
- ✅ Deploy importante a producción
- ✅ Agregar usuarios reales al sistema

---

## 🔍 DIAGNÓSTICO: ¿Qué Causó la Pérdida?

### Causas Conocidas

1. **Scripts Destructivos Ejecutados** ✅ RESUELTO
   - Causa: `1_recrear_base_de_datos.py`, etc.
   - Solución: Scripts eliminados permanentemente

2. **`generar_datos_completos.py` sin confirmación** ✅ RESUELTO
   - Causa: Se ejecutaba directo sin advertencias
   - Solución: Ahora requiere 2 confirmaciones explícitas

3. **Render Free sin backups automáticos** ⚠️ LIMITACIÓN CONOCIDA
   - Causa: Plan Free de Render no tiene backups
   - Solución: Backups manuales con `backup_from_render.py`
   - Mejora futura: Considerar plan Starter ($7/mes) con backups

4. **Migración fallida** (No ha ocurrido aún)
   - Prevención: Implementar Flask-Migrate en futuro
   - Backup antes de cualquier migración

---

## 💾 ESTRUCTURA DE BACKUPS

### Carpeta Local: `backups/`
```
backups/
├── prode_backup_20260225_163330.db
├── prode_backup_20260225_163343.db
├── ...
└── prode_backup_20260225_170940.db  ← Último
```

**Características:**
- Ignorada en `.gitignore` (no se sube a GitHub)
- Mantiene últimos 10 backups automáticamente
- Limpieza automática de backups antiguos

### Render (Producción)
- ⚠️ **Plan Free:** NO tiene backups automáticos
- 💡 **Plan Starter ($7/mes):** Backups diarios por 7 días
- 🔄 **Solución actual:** Backups manuales con `backup_from_render.py`

---

## 🚀 MEJORAS FUTURAS

### Implementadas ✅
- [x] Sistema de backups automáticos locales
- [x] Scripts de sync bidireccional (Local ↔ Render)
- [x] Eliminación de scripts peligrosos
- [x] Confirmaciones dobles en scripts críticos
- [x] Documentación completa de recuperación

### Pendientes 🔄

**Corto Plazo:**
- [ ] Pre-commit hook con `verificar_seguridad.py`
- [ ] Flag `--dry-run` en scripts importantes
- [ ] Logs de operaciones destructivas

**Mediano Plazo:**
- [ ] Upgrade a Render Starter para backups automáticos
- [ ] Flask-Migrate para migraciones seguras
- [ ] Sistema de "undo" para cambios recientes

**Largo Plazo:**
- [ ] Replicación de base de datos
- [ ] Auditoría completa de cambios
- [ ] Alertas por email en operaciones críticas

---

## 📞 EN CASO DE EMERGENCIA

**Si este documento no resuelve tu problema:**

1. ✅ Revisa carpeta `backups/` para backups más antiguos
2. ✅ Verifica si hay backup manual que hayas creado antes
3. ✅ Considera regenerar con `generar_datos_completos.py`
4. ✅ En último caso, acepta pérdida y regenera desde cero

**Consuelo:** Con los cambios implementados (scripts eliminados + confirmaciones dobles), las probabilidades de que esto vuelva a ocurrir son extremadamente bajas.

---

## ✅ CHECKLIST POST-INCIDENTE

Después de resolver un incidente, verificar:

- [ ] Datos restaurados correctamente (local y Render)
- [ ] 12 usuarios (1 admin + 11 ficticios)
- [ ] 104 partidos en 4 fases
- [ ] 675 pronósticos
- [ ] Backup fresco creado
- [ ] Documentación actualizada con lecciones aprendidas
- [ ] Protecciones adicionales implementadas si es necesario

---

**Última actualización:** 25 de Febrero, 2026 - 18:15 UTC  
**Versión:** 2.0 (Post-Incidente #2)  
**Incidentes totales:** 2 (ambos resueltos, prevención implementada)  
**Estado:** ✅ Sistema seguro con confirmaciones dobles y scripts peligrosos eliminados
