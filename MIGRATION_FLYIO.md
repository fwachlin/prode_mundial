# Guía de Migración a Fly.io

## Fecha límite: 26 de marzo de 2026 (Render suspende la base de datos)

---

## 📋 Requisitos previos

1. **Cuenta en Fly.io**
   - Crear cuenta en https://fly.io/
   - NO requiere tarjeta de crédito para el plan gratuito

2. **Instalar Fly.io CLI**
   
   **En Windows (PowerShell):**
   ```powershell
   iwr https://fly.io/install.ps1 -useb | iex
   ```
   
   Cerrar y reabrir PowerShell después de la instalación.

3. **Verificar instalación:**
   ```powershell
   fly version
   ```

4. **Login en Fly.io:**
   ```bash
   fly auth login
   ```
   Se abrirá el navegador para autenticarte.

---

## 🚀 Proceso de Migración

### Paso 1: Crear aplicación en Fly.io

```bash
# En el directorio del proyecto
cd e:\prode_mundial

# Lanzar la aplicación (esto crea la app y el archivo fly.toml)
fly launch --name prode-mundial-2026
```

**Responde a las preguntas:**
- Would you like to set up a PostgreSQL database? → **YES**
- Select configuration: → **Development - Single node, 1x shared CPU, 256MB RAM, 1GB disk**
- Would you like to set up an Upstash Redis database? → **NO**
- Would you like to deploy now? → **NO** (primero hacemos backup)

### Paso 2: Backup de la base de datos Render

Antes de migrar, descarga todos los datos de Render:

```bash
# Desde tu máquina local, conectar a Render y hacer dump
# (usa las credenciales de Render PostgreSQL)
python backup_from_render.py
```

O manualmente con `pg_dump`:
```bash
pg_dump -h <RENDER_HOST> -U <RENDER_USER> -d <RENDER_DB> -F c -f render_backup.dump
```

### Paso 3: Configurar variables de entorno en Fly.io

```bash
# Secret key para Flask
fly secrets set SECRET_KEY="tu-clave-secreta-super-segura-cambiar-esto"

# Google Analytics (opcional)
fly secrets set GA_MEASUREMENT_ID="G-XXXXXXXXXX"
```

Fly.io ya configura automáticamente `DATABASE_URL` cuando creas la base de datos PostgreSQL.

### Paso 4: Verificar configuración de la base de datos

```bash
# Ver información de la base de datos
fly postgres list

# Ver detalles de la base de datos prode-mundial-2026-db
fly postgres config show -a prode-mundial-2026-db
```

### Paso 5: Crear tablas en la base de datos Fly.io

```bash
# Conectar a la base de datos Fly.io
fly postgres connect -a prode-mundial-2026-db
```

Una vez conectado, ejecutar:
```sql
-- Verificar conexión
\l

-- Salir
\q
```

### Paso 6: Restaurar datos desde Render

**Opción A: Usar script de sync (recomendado)**

1. Crear `sync_render_to_flyio.py`:
```python
# Similar a sync_render_rapido.py pero apuntando a Fly.io
# Conectar a Render (origen) y Fly.io (destino)
# Copiar: allowed_emails, users, phases, matches, predictions, comment
```

2. Ejecutar:
```bash
python sync_render_to_flyio.py
```

**Opción B: Usar pg_restore**

```bash
# Obtener la connection string de Fly.io
fly postgres connect -a prode-mundial-2026-db

# Restaurar el dump
pg_restore -h <FLYIO_HOST> -U <FLYIO_USER> -d <FLYIO_DB> -c render_backup.dump
```

### Paso 7: Deploy de la aplicación

```bash
# Deploy inicial
fly deploy

# Ver logs en tiempo real
fly logs
```

### Paso 8: Verificar que funciona

```bash
# Abrir la aplicación en el navegador
fly open

# Ver el dashboard
fly dashboard
```

**Verificaciones:**
1. La página carga correctamente
2. Puedes hacer login con tus usuarios
3. Los partidos aparecen
4. Los pronósticos se muestran
5. El tablón funciona

### Paso 9: Configurar dominio (opcional)

Si tienes un dominio propio:

```bash
fly certs add tudominio.com
```

Luego configura los registros DNS según las instrucciones que te da Fly.io.

---

## 🗄️ Gestión de la Base de Datos Fly.io

### Conectar a la base de datos:
```bash
fly postgres connect -a prode-mundial-2026-db
```

### Ver tablas:
```sql
\dt
```

### Hacer backup manual:
```bash
fly postgres backup create -a prode-mundial-2026-db
```

### Ver backups:
```bash
fly postgres backup list -a prode-mundial-2026-db
```

---

## 📊 Monitoreo

### Ver logs en tiempo real:
```bash
fly logs
```

### Ver estado de la aplicación:
```bash
fly status
```

### Ver métricas:
```bash
fly dashboard
```

---

## 🔄 Actualizaciones futuras

Cada vez que hagas cambios en el código:

```bash
# 1. Commit los cambios a git
git add .
git commit -m "Descripción del cambio"

# 2. Deploy a Fly.io
fly deploy

# 3. Verificar logs
fly logs
```

---

## 🆘 Solución de Problemas

### La app no inicia:
```bash
fly logs
# Revisa los logs para ver el error específico
```

### Error de base de datos:
```bash
# Verificar que DATABASE_URL esté configurada
fly ssh console
env | grep DATABASE_URL
```

### Reiniciar la aplicación:
```bash
fly apps restart prode-mundial-2026
```

### Escalar recursos (si necesitas más memoria):
```bash
fly scale memory 512  # Aumentar a 512MB
```

---

## 💰 Límites del Plan Gratuito Fly.io

- **3 GB de disco** para PostgreSQL (suficiente)
- **256 MB RAM** por VM (suficiente para Flask)
- **160 GB de transferencia/mes** (más que suficiente)
- **Up to 3 shared-cpu-1x VMs** (usas 1)

Tu aplicación debería estar cómodamente dentro de estos límites.

---

## 📅 Cronograma Sugerido

- **Hoy (6 de marzo)**: Setup inicial, crear cuenta Fly.io
- **7-8 de marzo**: Deploy de prueba, verificar que funciona
- **9-10 de marzo**: Migrar datos desde Render
- **11-15 de marzo**: Testing completo, ajustes
- **16-20 de marzo**: Monitoreo, backup final de Render
- **21-25 de marzo**: Transición completa, actualizar DNS si tienes dominio
- **26 de marzo**: Render suspende la base de datos (ya no la necesitas)

---

## ✅ Checklist Final

- [ ] Cuenta Fly.io creada
- [ ] CLI instalado y funcionando
- [ ] App creada en Fly.io
- [ ] Base de datos PostgreSQL creada
- [ ] Secrets configurados (SECRET_KEY)
- [ ] Backup de Render descargado
- [ ] Datos migrados a Fly.io
- [ ] Deploy exitoso
- [ ] Login funciona
- [ ] Partidos visibles
- [ ] Pronósticos funcionan
- [ ] Tablón funciona
- [ ] Backup automático configurado

---

**Última actualización:** 6 de marzo de 2026  
**Estado:** Listo para migración  
**Deadline:** 26 de marzo de 2026
