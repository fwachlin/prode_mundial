# 🔒 REGLAS CRÍTICAS DEL PROYECTO - PRODE MUNDIAL

> **IMPORTANTE:** Este archivo documenta decisiones arquitectónicas y reglas de negocio que **NO DEBEN CAMBIAR** sin aprobación explícita. Consulta este archivo antes de hacer cambios significativos al código.

---

## 📋 ÍNDICE

1. [Arquitectura del Proyecto](#1-arquitectura-del-proyecto)
2. [Base de Datos y Modelos](#2-base-de-datos-y-modelos)
3. [Sistema de Autenticación](#3-sistema-de-autenticación)
4. [Sistema de Puntos](#4-sistema-de-puntos)
5. [Reglas de Negocio Críticas](#5-reglas-de-negocio-críticas)
6. [Manejo de Fechas y Zonas Horarias](#6-manejo-de-fechas-y-zonas-horarias)
7. [Roles y Permisos](#7-roles-y-permisos)
8. [Filtros de Template](#8-filtros-de-template)
9. [Despliegue y Entornos](#9-despliegue-y-entornos)
10. [Sistema de Backups](#10-sistema-de-backups)
11. [Scripts de Utilidad](#11-scripts-de-utilidad)

---

## 1. ARQUITECTURA DEL PROYECTO

### Estructura de Blueprints
```
app.py (aplicación principal)
├── auth (Blueprint: /auth)      - Registro, login, logout, cambio de contraseña
├── main (Blueprint: /)          - Index, pronósticos, rankings
└── admin (Blueprint: /admin)    - Dashboard, partidos, usuarios, comentarios
```

**REGLAS:**
- ✅ **Separación de blueprints debe mantenerse** - No mezclar rutas de diferentes módulos
- ✅ **Prefijos de URL no cambiar** - `/auth`, `/admin` están establecidos
- ✅ **Decoradores específicos por blueprint** - `@admin_required` solo en admin

### Extensiones Centralizadas
**Archivo:** `extensions.py`

```python
db = SQLAlchemy()
login_manager = LoginManager()
```

**REGLA CRÍTICA:**
- ⚠️ **NUNCA inicializar `db` directamente en models.py** - Siempre importar de `extensions.py`
- ⚠️ **db.init_app(app) solo en app.py** - Evita imports circulares

---

## 2. BASE DE DATOS Y MODELOS

### Modelos Principales
**Archivo:** `models.py`

| Modelo | Propósito | Campos Críticos |
|--------|-----------|-----------------|
| `User` | Usuarios del sistema | `email` (unique), `is_admin`, `is_enabled`, `password_hash` |
| `AllowedEmail` | Emails permitidos para registro | `email` (unique), `name` |
| `Phase` | Fases del mundial | `name`, `order` |
| `Match` | Partidos del mundial | `home_team`, `away_team`, `kickoff_at`, `closes_at`, `phase_id` |
| `Prediction` | Pronósticos de usuarios | `user_id`, `match_id`, `home_goals`, `away_goals`, `points_awarded` |
| `Comment` | Comentarios en tablón | `user_id`, `content`, `created_at` |

### Reglas de Base de Datos

**POSTGRESQL EN PRODUCCIÓN (Render):**
```python
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
```
- ⚠️ **NO CAMBIAR** - Render usa `postgres://` pero SQLAlchemy requiere `postgresql://`

**SQLITE EN DESARROLLO:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'prode.db')
```
- ✅ Base de datos en `instance/prode.db`
- ✅ Carpeta `instance` ignorada en git

### Constraints Únicos

**Match - UniqueConstraint:**
```python
__table_args__ = (
    db.UniqueConstraint("home_team", "away_team", "kickoff_at", name="unique_match"),
)
```
- ⚠️ **NO PERMITIR partidos duplicados** - Mismo local, visitante y fecha
- ⚠️ **NO ELIMINAR este constraint** - Previene duplicación de datos

---

## 3. SISTEMA DE AUTENTICACIÓN

### Registro de Usuarios

**REGLA CRÍTICA - EMAILS PERMITIDOS:**
```python
allowed = AllowedEmail.query.filter_by(email=email).first()
if not allowed:
    flash(f'El email {email} no está habilitado para registrarse', 'error')
    return redirect(url_for('auth.register'))
```

**ORDEN DE VALIDACIÓN (NO CAMBIAR):**
1. ✅ Validar campos obligatorios
2. ✅ **PRIMERO: Verificar email permitido** (`AllowedEmail`)
3. ✅ SEGUNDO: Verificar email no registrado
4. ✅ TERCERO: Verificar contraseñas coinciden
5. ✅ CUARTO: Validar longitud mínima (4 caracteres)

**POR QUÉ:**
- Si primero verificamos email duplicado, revelamos quién está registrado
- El orden actual protege privacidad de usuarios existentes

### Asignación de Nombres (NUEVO - Feb 2026)

**REGLA CRÍTICA - NOMBRES ASIGNADOS POR ADMIN:**
```python
# El admin define email + nombre en AllowedEmail
allowed = AllowedEmail(email='user@example.com', name='Juan Pérez')

# En registro, el nombre se toma de AllowedEmail
allowed = AllowedEmail.query.filter_by(email=email).first()
name = allowed.name  # ← Nombre asignado por admin
user = User(name=name, email=email, ...)
```

**RAZÓN DEL CAMBIO:**
- Evitar nombres excesivamente largos o estrafalarios
- Control centralizado de identificación de participantes
- Experiencia de registro simplificada (solo email + contraseña)

**IMPORTANTE:**
- ⚠️ El usuario NO puede elegir su nombre al registrarse
- ⚠️ El admin debe asignar nombre al habilitar email en `/admin/allowed-emails`
- ⚠️ Modelo `AllowedEmail` requiere campo `name` (NOT NULL)

### Hash de Contraseñas

```python
# Establecer contraseña
user.set_password(password)  # Usa generate_password_hash

# Verificar contraseña
user.check_password(password)  # Usa check_password_hash
```

- ⚠️ **NUNCA guardar contraseñas en texto plano**
- ⚠️ **NUNCA usar `password_hash` directamente** - Usar métodos del modelo

### Flask-Login

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

- ✅ Usuario en sesión: `current_user`
- ✅ Verificar autenticación: `current_user.is_authenticated`
- ✅ Requiere login: `@login_required`

---

## 4. SISTEMA DE PUNTOS

### Cálculo de Puntos (`Prediction.calculate_points()`)

**SISTEMA COMPLETO DE 3 COMPONENTES:**

#### 4.1. Ganador/Empate (10 puntos)
```python
if user_result == match_result:
    total_points += 10
else:
    return 0  # Si no acierta, devuelve 0 inmediatamente
```
- ⚠️ **SI NO ACIERTA GANADOR, NO HAY PUNTOS** - Retorna 0 de inmediato
- ✅ Resultados posibles: `'home'`, `'away'`, `'draw'`

#### 4.2. Batacazo (1-5 puntos bonus)
**Bonus si pocos usuarios aciertan:**
```python
# CRÍTICO: Contar solo usuarios NO-ADMIN
total_participants = User.query.filter_by(is_admin=False).count()
correct_predictions = Prediction.query.filter_by(match_id=match.id).join(User).filter(
    User.is_admin == False
).all()
correct_count = sum(1 for p in correct_predictions if ...)
correct_percentage = (correct_count / total_participants) * 100

if correct_percentage < 5:  total_points += 5
if correct_percentage < 10: total_points += 4
if correct_percentage < 15: total_points += 3
if correct_percentage < 20: total_points += 2
if correct_percentage < 25: total_points += 1
```
- ⚠️ **CRÍTICO:** Tanto el denominador (total_participants) como el numerador (correct_count) deben excluir admins
- ⚠️ **Solo se otorga si menos del 25% acertó**
- ✅ Recompensa pronósticos difíciles
- ✅ **FIX aplicado 25/Feb/2026:** Ahora filtra correctamente usuarios no-admin en ambas consultas

#### 4.3. Score Exacto (máximo 5 puntos)
```python
if home_goals == match_home and away_goals == match_away:
    total_points += 5  # Exacto
else:
    total_diff = abs(home_goals - match_home) + abs(away_goals - match_away)
    score_points = max(0, 5 - total_diff)
    total_points += score_points
```
- ✅ Exacto: 5 puntos
- ✅ 1 gol de diferencia total: 4 puntos
- ✅ 2 goles de diferencia: 3 puntos
- ✅ 5+ goles de diferencia: 0 puntos

**REGLA CRÍTICA:**
- ⚠️ **NO MODIFICAR FÓRMULAS** sin consenso
- ⚠️ **El cálculo es determinista** - Mismo resultado siempre con mismos datos

---

## 5. REGLAS DE NEGOCIO CRÍTICAS

### 5.1. Cierre de Pronósticos

```python
def is_open(self):
    """El pronóstico está abierto si ahora (UTC) es menor que closes_at"""
    closes_at = self.closes_at
    if closes_at.tzinfo is None:
        closes_at = closes_at.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) < closes_at
```

**REGLAS:**
- ⚠️ **`closes_at` SIEMPRE debe ser ANTES de `kickoff_at`** - Validado en admin
- ✅ Usuario NO puede modificar pronóstico después del cierre
- ✅ Validación en backend Y frontend

### 5.2. Administradores NO Juegan

```python
# En /predictions (main/routes.py)
if current_user.is_admin:
    flash('Los administradores no pueden hacer pronósticos', 'warning')
    return redirect(url_for('main.index'))
```

**REGLAS:**
- ⚠️ **Admins NO aparecen en rankings**
- ⚠️ **Admins NO pueden crear pronósticos**
- ✅ Filtro en consultas: `.filter(User.is_admin == False)`

### 5.3. Carga de Resultados

**Solo admins pueden:**
- ✅ Crear/editar/eliminar partidos
- ✅ Cargar resultados (`home_goals`, `away_goals`)
- ✅ Recalcular puntos de todos los pronósticos del partido

**Flujo crítico:**
```python
# Cuando admin carga resultado
match.home_goals = home_goals
match.away_goals = away_goals

# Recalcular puntos de TODOS los pronósticos
for prediction in match.predictions:
    prediction.points_awarded = prediction.calculate_points()

db.session.commit()
```

### 5.4. Usuarios Deshabilitados

```python
if not user.is_enabled:
    flash('Tu cuenta ha sido deshabilitada', 'error')
    return redirect(url_for('auth.login'))
```
- ✅ Admin puede deshabilitar usuarios sin eliminarlos
- ✅ Usuarios deshabilitados no pueden login
- ✅ Datos y pronósticos se mantienen

---

## 6. MANEJO DE FECHAS Y ZONAS HORARIAS

### Reglas Estrictas de Timezone

**SIEMPRE UTC en Base de Datos:**
```python
from datetime import datetime, timezone

kickoff_at = datetime.fromisoformat(kickoff_str).replace(tzinfo=timezone.utc)
```

**TIPOS DE DATETIME:**
```python
# CORRECTO - Timezone-aware
datetime.now(timezone.utc)

# INCORRECTO - Naive datetime
datetime.now()  # ⚠️ NO USAR
```

**Protección contra Naive Datetimes:**
```python
if closes_at.tzinfo is None:
    closes_at = closes_at.replace(tzinfo=timezone.utc)
```

**REGLAS CRÍTICAS:**
- ⚠️ **SIEMPRE usar `timezone.utc`** en operaciones de fecha
- ⚠️ **Column en DB:** `DateTime(timezone=True)`
- ✅ Convertir a local en frontend (JavaScript)

---

## 7. ROLES Y PERMISOS

### Decorador `@admin_required`

**Archivo:** `admin/decorators.py`

```python
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('No tienes permiso para acceder', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
```

**Aplicación:**
```python
@admin_bp.route('/dashboard')
@login_required
@admin_required  # ← SIEMPRE después de @login_required
def dashboard():
    ...
```

**REGLAS:**
- ⚠️ **ORDEN:** Primero `@login_required`, luego `@admin_required`
- ⚠️ **SIEMPRE validar `is_admin` en rutas sensibles**
- ✅ Redirige a `main.index` si no tiene permiso

### Matriz de Permisos

| Acción | Usuario Regular | Admin |
|--------|----------------|-------|
| Registro (si email permitido) | ✅ | ✅ |
| Login | ✅ | ✅ |
| Hacer pronósticos | ✅ | ❌ |
| Ver rankings | ✅ | ✅ |
| Ver pronósticos de todos | ✅ | ✅ |
| Crear/editar partidos | ❌ | ✅ |
| Cargar resultados | ❌ | ✅ |
| Gestionar usuarios | ❌ | ✅ |
| Agregar emails permitidos | ❌ | ✅ |

---

## 8. FILTROS DE TEMPLATE

### `fifa_code` - Convertir a Códigos FIFA

**Uso:** `{{ team_name|fifa_code }}`

**Casos especiales (NO CAMBIAR):**
```python
# Códigos de grupos (1A, 2B, 3C/D/E, etc.)
if country_name.startswith('1A'): return '1A'

# Winners/Losers (W1, W2, L25, etc.)
if country_name.startswith('W') and country_name[1].isdigit(): return country_name

# Paths de eliminación directa
if 'Path' in country_name: return country_name
```

**REGLA CRÍTICA:**
- ⚠️ **NO modificar lógica de placeholders** - Sistema de eliminación directa depende de esto

### `country_iso2` - Banderas

**Uso:** `{{ team_name|country_iso2 }}`

**Devuelve:**
- Código ISO 3166-1 alpha-2 (ej: `'ar'`, `'br'`)
- `'xx'` para placeholders sin bandera

**REGLA:**
- ✅ Placeholders (1A, 2B, W1, etc.) devuelven `'xx'`
- ✅ Inglaterra usa `'gb-eng'`, Gales `'gb-wls'`, Escocia `'gb-sct'`

---

## 9. DESPLIEGUE Y ENTORNOS

### Producción (Render)

**Variables de entorno requeridas:**
```bash
DATABASE_URL=postgresql://...
SECRET_KEY=clave-secreta-produccion
```

**Archivos críticos:**
- `build.sh` - Script de build para Render
- `requirements.txt` - Dependencias Python
- `gunicorn` - Servidor WSGI en producción

### Desarrollo Local

**Activar entorno:**
```powershell
& e:\prode_mundial\venv\Scripts\Activate.ps1
```

**Ejecutar:**
```powershell
python app.py
```

**Base de datos:**
- SQLite en `instance/prode.db`
- No requiere configuración

---

## 10. SCRIPTS AUXILIARES

### ⚠️ Scripts Legacy (NO USAR en Producción)

| Script | Propósito | ⚠️ Precaución |
|--------|-----------|---------------|
| `1_recrear_base_de_datos.py` | Borra y recrea DB | **DESTRUYE DATOS** |
| `eliminar_todos_los_partidos.py` | Elimina partidos | **DESTRUCTIVO** |
| `recrear_db_completa.py` | Reset completo | **SOLO DESARROLLO** |

### ✅ Scripts de Utilidad Seguros
10. SISTEMA DE BACKUPS

### Backups Automáticos

**Archivo:** `auto_backup.py`

```python
def backup_database():
    """Crear backup antes de cualquier operación"""
    # Se ejecuta automáticamente al iniciar Flask (solo en desarrollo)
    # Mantiene últimos 10 backups
```

**REGLAS:**
- ✅ **Backups automáticos** - Se crean al ejecutar `python app.py`
- ✅ **Solo en desarrollo** - No se ejecutan en producción (Render)
- ✅ **Carpeta `backups/`** - Ignorada en git, no se sube
- ✅ **Mantener últimos 10** - Los más antiguos se eliminan automáticamente

**Restauración:**
```powershell
python auto_backup.py restore
```

**REGLA CRÍTICA:**
- ⚠️ **NUNCA subir backups a git** - Contienen datos sensibles
- ⚠️ **Backups locales solo** - Render tiene sus propios backups automáticos

---

## 11. SCRIPTS DE UTILIDAD

### Scripts Seguros (Solo Lectura)

| Script | Propósito | Uso |
|--------|-----------|-----|
| `ver_db.py`  (Actualización 2)
- ✅ **FIX CRÍTICO:** Batacazo ahora excluye admins en AMBAS consultas (numerador y denominador)
- ✅ Sistema de backups automáticos implementado (`auto_backup.py`)
- ✅ Script de generación completa de datos (`generar_datos_completos.py`)
- ✅ Documentación completa creada (QUICK_START.md, DATABASE_INFO.md, DISASTER_RECOVERY.md)
- ✅ Protecciones contra pérdida de datos implementadas

### 2026-02-25 (Actualización 1)| Ver contenido completo de DB | `python ver_db.py` |
| `check_users.py` | Ver lista de usuarios | `python check_users.py` |
| `check_render_db.py` | Ver estado de DB en Render | Requiere DATABASE_URL |
| `sync_db_from_render.py` | Sincronizar DE Render a local | NO afecta Render |

### Scripts de Generación

| Script | Propósito | Uso |
|--------|-----------|-----|
| `generar_datos_completos.py` | Genera DB ficticia completa | `python generar_datos_completos.py` |
| `init_phases.py` | Crea solo las 4 fases | Solo si no existen |

**Script de Generación Completa:**
```python
# generar_datos_completos.py
# - 4 fases
# - 104 partidos del Mundial 2026
# - 11 usuarios ficticios (contraseña: prode123)
# - ~675 pronósticos (85% cobertura)
```

### ⚠️ Scripts Peligrosos (DESTRUCTIVOS)

**NUNCA ejecutar sin confirmación explícita:**
- `1_recrear_base_de_datos.py` - **BORRA TODA LA DB**
- `recrear_db_completa.py` - **BORRA TODA LA DB**
- `eliminar_todos_los_partidos.py` - **BORRA TODOS LOS PARTIDOS**

**REGLA CRÍTICA:**
- ⚠️ **Leer código completo** antes de ejecutar cualquier script
- ⚠️ **Ver `SCRIPTS_PELIGROSOS.md`** para detalles
- ⚠️ **Tener backup** antes de ejecutar scripts destructivos

---

## 
| Script | Propósito | Uso |
|--------|-----------|-----|
| `ver_db.py` | Ver contenido de tablas | Debugging |
| `verificar_datos.py` | Validar datos | Testing |
| `add_allowed_emails.py` | Agregar emails | Producción OK |
| `create_admin_render.py` | Crear admin en Render | Producción OK |

---

## 🚨 CAMBIOS QUE REQUIEREN APROBACIÓN

### Arquitectura
- [ ] Modificar estructura de blueprints
- [ ] Cambiar sistema de extensiones
- [ ] Agregar nuevos modelos a la DB

### Sistema de Puntos
- [ ] Modificar fórmulas de cálculo
- [ ] Cambiar umbrales de batacazo
- [ ] Alterar lógica de score

### Autenticación
- [ ] Cambiar sistema de emails permitidos
- [ ] Modificar hash de contraseñas
- [ ] Alterar roles y permisos

### Base de Datos
- [ ] Eliminar constraints
- [ ] Cambiar tipos de columnas
- [ ] Modificar relaciones entre modelos

---

## 📝 CHANGELOG DE DECISIONES

### 2026-02-25
- ✅ Sistema de emails permitidos implementado
- ✅ Administradores excluidos de pronósticos y rankings
- ✅ Sistema de puntos con 3 componentes establecido
- ✅ Manejo estricto de timezones UTC

---

## 🔍 ANTES DE HACER CAMBIOS

**Checklist:**
1. ¿Este cambio afecta el cálculo de puntos? → Revisar Sección 4
2. ¿Modifica permisos o roles? → Revisar Sección 7
3. ¿Toca autenticación? → Revisar Sección 3
4. ¿Cambia estructura de DB? → Revisar Sección 2
5. ¿Altera fechas/horarios? → Revisar Sección 6

**Si la respuesta es SÍ a alguna, CONSULTAR este documento primero.**

---

**Última actualización:** 25 de Febrero, 2026
**Versión:** 1.0
