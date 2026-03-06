# Inicio Rápido - Migración a Fly.io

Este documento te guía paso a paso para migrar de Render a Fly.io antes del 26 de marzo de 2026.

## ⚡ Pasos Rápidos (30 minutos)

### 1️⃣ Instalar Fly.io CLI (5 min)

**Windows PowerShell como Administrador:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

Cierra y abre PowerShell, luego verifica:
```bash
fly version
```

### 2️⃣ Login en Fly.io (2 min)

```bash
fly auth login
```

### 3️⃣ Lanzar la aplicación (5 min)

```bash
cd e:\prode_mundial
fly launch --name prode-mundial-2026
```

**Responder:**
- PostgreSQL database? → **YES**
- Configuration: → **Development** (256MB RAM, 1GB disk)
- Redis? → **NO**
- Deploy now? → **NO**

### 4️⃣ Configurar secrets (2 min)

```bash
fly secrets set SECRET_KEY="clave-super-secreta-cambiar-esto-ahora"
```

### 5️⃣ Migrar datos desde Render (10 min)

**A. Configurar variables de entorno:**

En PowerShell:
```powershell
# URL de Render (obtener desde Render dashboard)
$env:RENDER_DATABASE_URL="postgresql://user:pass@host:5432/db"

# URL de Fly.io (obtener con: fly postgres connect -a prode-mundial-2026-db)
$env:FLYIO_DATABASE_URL="postgresql://user:pass@host:5432/db"
```

**B. Ejecutar migración:**
```bash
python sync_render_to_flyio.py
```

**C. Verificar migración:**
```bash
python verify_flyio_migration.py
```

### 6️⃣ Deploy (3 min)

```bash
fly deploy
```

Espera a que termine (2-3 minutos).

### 7️⃣ Verificar (3 min)

```bash
# Abrir en navegador
fly open

# Ver logs
fly logs
```

**Checklist rápido:**
- [ ] Página carga
- [ ] Login funciona
- [ ] Partidos visibles
- [ ] Pronósticos funcionan

---

## 🆘 Si algo falla

### Ver logs:
```bash
fly logs
```

### Reiniciar app:
```bash
fly apps restart prode-mundial-2026
```

### Conectar a la base de datos:
```bash
fly postgres connect -a prode-mundial-2026-db
```

---

## 📱 Comandos útiles

```bash
# Ver status
fly status

# Ver apps
fly apps list

# Ver bases de datos
fly postgres list

# Dashboard web
fly dashboard

# SSH a la app
fly ssh console
```

---

## 🔄 Actualizaciones futuras

Cada vez que cambies código:

```bash
git add .
git commit -m "Cambios"
fly deploy
```

---

## 💾 Backups

### Crear backup manual:
```bash
fly postgres backup create -a prode-mundial-2026-db
```

### Ver backups:
```bash
fly postgres backup list -a prode-mundial-2026-db
```

---

## ✅ ¡Listo!

Tu aplicación está ahora en Fly.io y funcionará gratis hasta después del Mundial 2026.

**Próximos pasos:**
1. Guarda las credenciales de acceso de Fly.io
2. Elimina la app de Render después del 26 de marzo
3. Monitorea los logs los primeros días

Para más detalles, consulta [MIGRATION_FLYIO.md](MIGRATION_FLYIO.md)
