# Scripts de Backup desde Supabase

Este directorio contiene scripts para hacer backup de la base de datos Supabase (producción).

## 📋 Scripts Disponibles

### 1. `backup_supabase_to_local.py`
Copia toda la base de datos de Supabase a tu SQLite local

**Uso:**
```powershell
python backup_supabase_to_local.py
```

**Qué hace:**
- Se conecta a Supabase usando la variable `DATABASE_URL`
- Hace backup del archivo `instance/prode.db` actual (si existe)
- Limpia las tablas locales
- Copia todos los datos de Supabase a local
- Respeta las foreign keys y el orden de inserción

**Cuándo usar:**
- Quieres trabajar con datos de producción en local
- Necesitas debuggear un problema específico con datos reales
- Quieres restaurar tu base de datos local a un estado conocido

### 2. `export_supabase_to_json.py`
Exporta toda la base de datos de Supabase a archivos JSON

**Uso:**
```powershell
python export_supabase_to_json.py
```

**Qué hace:**
- Se conecta a Supabase usando la variable `DATABASE_URL`
- Crea una carpeta en `backups/supabase_backup_YYYYMMDD_HHMMSS/`
- Exporta cada tabla a un archivo JSON separado
- Crea un archivo `_backup_info.json` con metadata

**Cuándo usar:**
- Quieres un backup legible en formato JSON
- Necesitas inspeccionar los datos manualmente
- Quieres un backup portable que no depende de SQLite
- Quieres versionar los datos en git (con cuidado de no incluir datos sensibles)

## 🔧 Requisitos

### Variables de Entorno

Debes tener configurada la variable `DATABASE_URL` con la URL de conexión a Supabase:

```powershell
# Windows PowerShell
$env:DATABASE_URL = "postgresql://user:password@host.supabase.co:5432/postgres"
```

### Dependencias

Ambos scripts usan librerías que ya tienes instaladas:
- `sqlalchemy` - Para conexión a bases de datos
- `psycopg2` - Driver PostgreSQL

## 📂 Estructura de Backups

```
prode_mundial/
├── backups/                          # Carpeta de backups JSON
│   ├── supabase_backup_20260317_150230/
│   │   ├── _backup_info.json        # Metadata del backup
│   │   ├── groups.json
│   │   ├── teams.json
│   │   ├── phases.json
│   │   ├── matches.json
│   │   ├── allowed_emails.json
│   │   ├── users.json
│   │   ├── predictions.json
│   │   └── comment.json
│   └── supabase_backup_20260318_093045/
│       └── ...
│
├── instance/
│   ├── prode.db                      # Base de datos local
│   ├── prode_backup_20260317_150230.db  # Backup automático
│   └── prode_backup_20260318_093045.db
│
├── backup_supabase_to_local.py       # Script 1: Supabase → SQLite
└── export_supabase_to_json.py        # Script 2: Supabase → JSON
```

## ⚠️ Advertencias

1. **Cierra Flask antes de ejecutar backup_supabase_to_local.py:**
   - SQLite no permite múltiples escrituras simultáneas
   - Si Flask está usando `prode.db`, el script fallará

2. **No commitees backups con datos sensibles:**
   - Los archivos JSON pueden contener contraseñas hasheadas
   - Los emails de usuarios son información personal
   - Agrega `backups/` al `.gitignore`

3. **Los backups automáticos ocupan espacio:**
   - `backup_supabase_to_local.py` crea un backup cada vez que se ejecuta
   - Limpia backups antiguos manualmente si es necesario

## 🚀 Ejemplo de Uso Completo

```powershell
# 1. Configurar DATABASE_URL
$env:DATABASE_URL = "postgresql://postgres:[TU-PASSWORD]@[TU-PROYECTO].supabase.co:5432/postgres"

# 2. Hacer backup a SQLite local (para trabajar con datos)
python backup_supabase_to_local.py

# 3. Hacer backup a JSON (para archivo/inspección)
python export_supabase_to_json.py

# 4. Verificar que funcionó
python check_users_count.py
```

## 📝 Notas

- Ambos scripts muestran progreso en tiempo real con emojis ✅ ❌ ⚠️
- Los backups incluyen timestamp para no sobrescribir accidentalmente
- El orden de tablas respeta las foreign keys
- Los archivos JSON usan UTF-8 y formateo legible (indent=2)

## 🔄 Restaurar desde Backup

### Desde SQLite backup:
```powershell
# Simplemente renombra/copia el archivo
Copy-Item instance\prode_backup_20260317_150230.db instance\prode.db
```

### Desde JSON:
Tendrías que crear un script de importación (no incluido aún).
