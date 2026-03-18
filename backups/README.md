# Backups de Supabase

Esta carpeta contiene los backups en formato JSON exportados desde Supabase.

**Contenido ignorado por git:** Los archivos de backup no se suben al repositorio por seguridad.

Para crear un backup nuevo:
```powershell
python export_supabase_to_json.py
```

Cada backup se guarda en una carpeta con timestamp:
- `supabase_backup_YYYYMMDD_HHMMSS/`

Ver: `BACKUP_SCRIPTS_README.md` en la raíz del proyecto para más información.
