# 📊 ESTADO ACTUAL DEL SISTEMA - PRODE MUNDIAL

> **Propósito:** Este documento refleja el estado ACTUAL y CORRECTO del sistema al 25 de febrero de 2026. Usa este archivo como referencia para validar que los cambios no rompan funcionalidad existente.

---

## 📅 FECHA DE SNAPSHOT
**Última actualización:** 25 de Febrero, 2026  
**Mundial:** FIFA World Cup 2026 (Estados Unidos, Canadá, México)  
**Estado del proyecto:** ✅ Producción en Render

---

## 🗄️ BASE DE DATOS

### Estado de Tablas

| Tabla | Descripción | Estado Actual |
|-------|-------------|---------------|
| `users` | Usuarios registrados | ✅ Activa - Con usuarios |
| `allowed_emails` | Emails permitidos para registro | ✅ Activa - Lista configurada |
| `phases` | Fases del mundial (Fechas 1-4) | ✅ Activa - 4 fases creadas |
| `matches` | Partidos del mundial | ✅ Activa - Partidos cargados |
| `predictions` | Pronósticos de usuarios | ✅ Activa - Con pronósticos |
| `comment` | Comentarios en tablón | ✅ Activa - Funcional |
| `groups` | Grupos del mundial | ⚠️ Existe pero NO se usa actualmente |
| `teams` | Equipos | ⚠️ Existe pero NO se usa actualmente |

### Fases Configuradas

**Tabla `phases`:**
```
id | name    | order
---|---------|------
1  | Fecha 1 | 1
2  | Fecha 2 | 2
3  | Fecha 3 | 3
4  | Fecha 4 | 4
```

**Estado:** ✅ Las 4 fases están creadas y funcionando correctamente.

### Estructura de Partidos

**Campos obligatorios para cada Match:**
- `home_team` (String) - Nombre del equipo local
- `away_team` (String) - Nombre del equipo visitante
- `kickoff_at` (DateTime con timezone) - Hora de inicio del partido
- `closes_at` (DateTime con timezone) - Hora de cierre de pronósticos
- `phase_id` (Integer FK) - Referencia a la fase (1-4)
- `home_goals` (Integer nullable) - Resultado local (NULL hasta que se carga)
- `away_goals` (Integer nullable) - Resultado visitante (NULL hasta que se carga)

**Restricción:**
- `closes_at` DEBE ser menor que `kickoff_at`
- UniqueConstraint en (`home_team`, `away_team`, `kickoff_at`)

---

## 👥 USUARIOS Y AUTENTICACIÓN

### Tipos de Usuarios

| Tipo | `is_admin` | `is_enabled` | Puede Pronosticar | Aparece en Rankings |
|------|------------|--------------|-------------------|---------------------|
| Usuario regular | `False` | `True` | ✅ Sí | ✅ Sí |
| Usuario deshabilitado | `False` | `False` | ❌ No (no puede login) | ❌ No |
| Administrador | `True` | `True` | ❌ No | ❌ No |

### Sistema de Emails Permitidos

**Estado:** ✅ **ACTIVO Y FUNCIONANDO**

**Flujo de registro:**
1. Usuario intenta registrarse con `email@example.com`
2. Sistema verifica si existe en tabla `allowed_emails`
3. Si NO existe → Mensaje: "El email no está habilitado para registrarse"
4. Si existe → Permite continuar con validaciones

**Administración:**
- Solo admins pueden agregar emails a la lista
- Ruta: `/admin/allowed-emails`
- Script: `add_allowed_emails.py` (para desarrollo)

### Contraseñas

**Estado actual:**
- ✅ Hash con `werkzeug.security.generate_password_hash`
- ✅ Verificación con `check_password_hash`
- ✅ Longitud mínima: 4 caracteres
- ⚠️ **NO hay requisitos de complejidad** (solo longitud)

**Métodos del modelo:**
```python
user.set_password(password)  # Establece hash
user.check_password(password)  # Verifica
```

---

## 🎯 SISTEMA DE PRONÓSTICOS

### Estados de un Pronóstico

| Estado | Condición | Usuario Puede Modificar |
|--------|-----------|------------------------|
| **Abierto** | `datetime.now(UTC) < match.closes_at` | ✅ Sí |
| **Cerrado** | `datetime.now(UTC) >= match.closes_at` | ❌ No |
| **Finalizado** | `match.home_goals != None` | ❌ No (resultado cargado) |

### Validaciones Activas

**Frontend (JavaScript):**
- ✅ Inputs deshabilitados si pronóstico cerrado
- ✅ Countdown visual hasta cierre
- ⚠️ Puede tener bugs - **NUNCA confiar solo en frontend**

**Backend (Python - CRÍTICO):**
```python
if not match.is_open():
    flash('Este pronóstico está cerrado', 'error')
    return redirect(url_for('main.predictions'))
```
- ✅ Validación en `main/routes.py` línea ~44
- ✅ **Esta es la validación que REALMENTE importa**

### Modificación de Pronósticos

**Comportamiento actual:**
```python
prediction = Prediction.query.filter_by(
    user_id=current_user.id,
    match_id=match_id
).first()

if prediction:
    # ACTUALIZA pronóstico existente
    prediction.home_goals = home_goals
    prediction.away_goals = away_goals
else:
    # CREA nuevo pronóstico
    prediction = Prediction(...)
    db.session.add(prediction)
```

**Estado:** ✅ Usuario puede modificar pronóstico múltiples veces mientras esté abierto

---

## 🏆 SISTEMA DE PUNTOS

### Estado de Implementación

**Componente 1: Ganador/Empate (10 pts)**
- ✅ Implementado
- ✅ Funcional
- ✅ Si falla, devuelve 0 (no sigue evaluando)

**Componente 2: Batacazo (1-5 pts bonus)**
- ✅ Implementado
- ✅ Funcional
- ✅ Basado en porcentaje de aciertos

**Componente 3: Score Exacto (máx 5 pts)**
- ✅ Implementado
- ✅ Funcional
- ✅ Penalización por diferencia de goles

### Cálculo de Puntos

**Método:** `Prediction.calculate_points()`

**Se ejecuta:**
- ✅ Cuando admin carga resultado de un partido
- ✅ Cuando admin edita resultado existente
- ✅ **NO se ejecuta automáticamente** - Admin debe guardarlo

**Almacenamiento:**
```python
prediction.points_awarded = prediction.calculate_points()
db.session.commit()
```
- Campo `points_awarded` en tabla `predictions`
- ✅ Nullable (None si resultado no cargado)

### Recálculo Masivo

**Cuando admin carga/edita resultado:**
```python
for prediction in match.predictions:
    prediction.points_awarded = prediction.calculate_points()
db.session.commit()
```

**Estado:** ✅ TODOS los pronósticos del partido se recalculan automáticamente

---

## 📊 RANKINGS

### Tipos de Rankings Disponibles

| Ruta | Tipo | Filtro |
|------|------|--------|
| `/rankings` | General | Suma TODOS los puntos de todas las fases |
| `/rankings/phase/<id>` | Por Fase | Solo puntos de esa fase específica |
| `/rankings/matches/<id>` | Por Partido | ⚠️ Existe pero implementación incompleta |

### Exclusión de Administradores

**CRÍTICO:** Administradores NO aparecen en rankings

**Implementación actual:**
```python
.filter(User.is_admin == False)
```

**Ubicaciones:**
- ✅ `main/routes.py` - Ruta `/rankings`
- ✅ `main/routes.py` - Ruta `/rankings/phase/<id>`
- ✅ Consulta de conteo en admin dashboard

**Estado:** ✅ Funcionando correctamente

---

## 🔐 PANEL DE ADMINISTRACIÓN

### Rutas Disponibles

| Ruta | Funcionalidad | Estado |
|------|---------------|--------|
| `/admin/dashboard` | Panel principal | ✅ Funcional |
| `/admin/matches` | Listar partidos | ✅ Funcional |
| `/admin/matches/new` | Crear partido | ✅ Funcional |
| `/admin/matches/<id>/edit` | Editar partido | ✅ Funcional |
| `/admin/matches/<id>/delete` | Eliminar partido | ✅ Funcional |
| `/admin/users` | Listar usuarios | ✅ Funcional |
| `/admin/users/<id>` | Ver usuario | ✅ Funcional |
| `/admin/users/<id>/edit` | Editar usuario | ✅ Funcional |
| `/admin/users/<id>/delete` | Eliminar usuario | ✅ Funcional |
| `/admin/allowed-emails` | Gestionar emails permitidos | ✅ Funcional |
| `/admin/comments` | Ver/eliminar comentarios | ✅ Funcional |

### Protección de Rutas

**Decoradores aplicados:**
```python
@admin_bp.route('/dashboard')
@login_required          # Primero: verifica login
@admin_required          # Segundo: verifica admin
def dashboard():
```

**Estado:** ✅ Todas las rutas admin están protegidas correctamente

### Carga de Resultados

**Proceso actual:**
1. Admin navega a `/admin/matches/<id>/edit`
2. Ingresa `home_goals` y `away_goals`
3. Submit del formulario
4. Backend:
   - Actualiza `match.home_goals` y `match.away_goals`
   - Itera sobre `match.predictions`
   - Calcula `prediction.points_awarded` para cada uno
   - Guarda cambios
5. Redirige a lista de partidos

**Estado:** ✅ Funcionando correctamente

---

## 🎨 FRONTEND Y TEMPLATES

### Estructura de Templates

```
templates/
├── base.html (Layout principal con Bootstrap 5)
├── auth/
│   ├── login.html
│   ├── register.html
│   └── change_password.html
├── main/
│   ├── index.html (Homepage con countdown)
│   ├── predictions.html (Hacer pronósticos)
│   ├── rankings.html (Ranking general)
│   ├── rankings_phase.html (Ranking por fase)
│   ├── all_predictions.html (Ver pronósticos de todos)
│   ├── tablon.html (Comentarios)
│   └── reglamento.html
└── admin/
    ├── dashboard.html
    ├── matches.html
    ├── create_match.html
    ├── edit_match.html
    ├── users.html
    ├── view_user.html
    ├── edit_user.html
    ├── allowed_emails.html
    └── comments.html
```

### CSS y Assets

**Archivo:** `static/css/site.css`

**Estado:**
- ✅ Bootstrap 5 integrado (CDN)
- ✅ Bootstrap Icons incluidos
- ✅ Google Fonts (Inter)
- ✅ CSS personalizado con variables de tema
- ✅ Responsive design

**Imágenes:**
```
static/images/
├── backgrounds/ (fondos)
├── teams/ (escudos)
├── players/ (jugadores)
└── stadiums/ (estadios)
```

**Estado:** ⚠️ Estructura creada pero imágenes no incluidas (por tamaño)

### Filtros de Template

**Activos y funcionando:**
- ✅ `{{ country|fifa_code }}` - Convierte a código FIFA
- ✅ `{{ country|country_iso2 }}` - Convierte a ISO2 para banderas
- ✅ `{{ current_user }}` - Disponible globalmente

---

## 🌐 DESPLIEGUE

### Entorno de Producción (Render)

**URL:** (configurada en Render)

**Variables de entorno requeridas:**
```bash
DATABASE_URL=postgresql://...  # PostgreSQL de Render
SECRET_KEY=clave-secreta-aleatoria
```

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn app:app
```

**Estado:** ✅ Desplegado y funcionando

### Entorno de Desarrollo Local

**Base de datos:** SQLite en `instance/prode.db`

**Activación de entorno virtual:**
```powershell
& e:\prode_mundial\venv\Scripts\Activate.ps1
```

**Ejecutar:**
```powershell
python app.py
```

**Puerto:** `5000` (Flask default)

**Estado:** ✅ Funcionando en desarrollo

---

## 🔄 MIGRACIONES Y CAMBIOS DE ESQUEMA

### Estado Actual

**Sistema de migraciones:** ❌ **NO implementado**

**Cómo se manejan cambios de DB:**
- ⚠️ Desarrollo: Se borra y recrea DB (`1_recrear_base_de_datos.py`)
- ⚠️ Producción: Cambios manuales en PostgreSQL o scripts ad-hoc

**Recomendación futura:**
- 📝 Considerar implementar Flask-Migrate (Alembic)
- 📝 Especialmente antes de lanzamiento público

---

## 🐛 BUGS CONOCIDOS Y LIMITACIONES

### Bugs Conocidos

1. **⚠️ Timezone en Frontend**
   - Fechas se muestran en UTC
   - TODO: Convertir a zona horaria local del usuario en JavaScript

2. **⚠️ No hay paginación**
   - Lista de partidos puede ser muy larga
   - Lista de usuarios puede crecer indefinidamente
   - TODO: Implementar paginación

3. **⚠️ Validación de emails débil**
   - Solo verifica que esté en lista
   - No valida formato de email robusto
   - TODO: Agregar validación de formato

### Limitaciones del Sistema

1. **Un solo mundial**
   - No hay soporte para múltiples torneos simultáneos
   - Hardcoded para Mundial 2026

2. **Fases fijas (1-4)**
   - No hay eliminación directa como fase separada
   - Sistema asume solo fase de grupos

3. **Sin notificaciones**
   - Usuarios no reciben avisos de:
     - Resultados cargados
     - Partidos próximos a cerrar
     - Cambios en rankings

4. **Sin recuperación de contraseña**
   - No hay "olvidé mi contraseña"
   - Admin debe resetear manualmente

---

## ✅ FUNCIONALIDADES CONFIRMADAS

### Autenticación
- ✅ Registro con email permitido
- ✅ Login/logout
- ✅ Cambio de contraseña
- ✅ Sistema de sesiones (Flask-Login)
- ✅ Protección de rutas con decoradores

### Pronósticos
- ✅ Crear pronóstico nuevo
- ✅ Modificar pronóstico existente (antes del cierre)
- ✅ Validación de cierre (backend)
- ✅ Visualización de pronósticos abiertos/cerrados

### Rankings
- ✅ Ranking general
- ✅ Ranking por fase
- ✅ Exclusión de admins
- ✅ Ordenamiento por puntos y nombre

### Administración
- ✅ Dashboard con estadísticas
- ✅ CRUD completo de partidos
- ✅ CRUD completo de usuarios
- ✅ Gestión de emails permitidos
- ✅ Moderación de comentarios
- ✅ Carga y edición de resultados
- ✅ Recálculo automático de puntos

### Visualización
- ✅ Banderas de países (via flag-icons)
- ✅ Countdown al primer partido
- ✅ Lista de próximos partidos
- ✅ Tablón de comentarios
- ✅ Ver pronósticos de todos los usuarios

---

## 🔮 ROADMAP FUTURO (No implementado)

### Corto Plazo
- [ ] Recuperación de contraseña por email
- [ ] Paginación en listas largas
- [ ] Mejorar validación de formularios
- [ ] Tests automatizados (pytest)

### Mediano Plazo
- [ ] Sistema de notificaciones
- [ ] Conversión de timezones en frontend
- [ ] Estadísticas avanzadas por usuario
- [ ] Exportar rankings a PDF/Excel

### Largo Plazo
- [ ] Soporte para múltiples torneos
- [ ] Sistema de ligas/grupos privados
- [ ] API REST para apps móviles
- [ ] Fase de eliminación directa

---

## 📝 NOTAS IMPORTANTES

### Al Modificar el Código

**ANTES de hacer cambios:**
1. ✅ Leer `PROJECT_RULES.md` - Reglas arquitectónicas
2. ✅ Leer este archivo - Estado actual del sistema
3. ✅ Verificar que el cambio no rompa funcionalidad documentada
4. ✅ Probar en desarrollo antes de producción

### Al Reportar Bugs

**Incluir:**
- Entorno (Desarrollo/Producción)
- Pasos para reproducir
- Comportamiento esperado vs actual
- Capturas de pantalla si aplica

### Al Agregar Features

**Documentar:**
- Actualizar `PROJECT_RULES.md` si afecta arquitectura
- Actualizar este archivo con nueva funcionalidad
- Agregar tests si es posible
- Actualizar README si es user-facing

---

## 📞 CONTACTO Y MANTENIMIENTO

**Responsable:** (Agregar nombre)  
**Última revisión:** 25 de Febrero, 2026  
**Próxima revisión:** Después de cada deploy importante

---

**🎯 Recuerda:** Este documento es un snapshot del sistema FUNCIONAL. Úsalo como referencia para asegurar que los cambios no rompan lo que ya funciona.
