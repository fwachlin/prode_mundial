# Cambio en el Sistema de Registro - Nombres Asignados por Admin

**Fecha:** 28 de Febrero, 2026  
**Tipo:** Cambio de funcionalidad

---

## 📋 Resumen del Cambio

El sistema de registro ha sido modificado para que **el administrador defina tanto el email como el nombre** que tendrá cada participante al registrarse.

### Antes:
- El usuario elegía su propio nombre al registrarse
- El admin solo habilitaba el email

### Ahora:
- El admin define email + nombre del participante
- El usuario solo proporciona email y contraseña al registrarse
- El nombre se asigna automáticamente del registro de AllowedEmail

---

## 🎯 Objetivos del Cambio

1. **Evitar nombres excesivamente largos o estrafalarios**
2. **Control centralizado de nombres de participantes**
3. **Menos interacciones post-registro para cambiar nombres**
4. **Experiencia de registro más simple para usuarios**

---

## 🔧 Cambios Técnicos Implementados

### 1. Modelo AllowedEmail - [models.py](models.py)
```python
class AllowedEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)  # ← NUEVO CAMPO
```

### 2. Template Admin - [templates/admin/allowed_emails.html](templates/admin/allowed_emails.html)
- Agregado campo de entrada para el nombre
- Tabla muestra ahora: Nombre | Email | Acciones

### 3. Ruta Admin - [admin/routes.py](admin/routes.py)
```python
@admin_bp.route('/allowed-emails', methods=['POST'])
def allowed_emails():
    name = request.form.get('name')  # ← Nuevo campo
    email = request.form.get('email')
    db.session.add(AllowedEmail(email=email, name=name))
```

### 4. Template Registro - [templates/auth/register.html](templates/auth/register.html)
- **ELIMINADO** campo de nombre
- Usuario solo ingresa: email y contraseña

### 5. Ruta Registro - [auth/routes.py](auth/routes.py)
```python
@auth_bp.route('/register', methods=['POST'])
def register():
    allowed = AllowedEmail.query.filter_by(email=email).first()
    name = allowed.name  # ← Tomar nombre del AllowedEmail
    user = User(name=name, email=email, ...)
```

### 6. Tests Actualizados
- [tests/conftest.py](tests/conftest.py) - Fixture `allowed_email` actualizado
- [tests/test_auth.py](tests/test_auth.py) - Tests de registro sin campo nombre
- [tests/test_models.py](tests/test_models.py) - Test AllowedEmail con nombre

---

## 🗄️ Migración de Base de Datos

### Script: [add_name_to_allowed_emails.py](add_name_to_allowed_emails.py)

**Ejecutar UNA SOLA VEZ:**
```powershell
python add_name_to_allowed_emails.py
```

**Lo que hace:**
1. Agrega columna `name` a la tabla `allowed_emails`
2. Actualiza registros existentes con nombre basado en email (parte antes de @)
3. Establece columna como NOT NULL

**Compatibilidad:**
- ✅ SQLite (desarrollo)
- ✅ PostgreSQL (producción Render)

---

## ✅ Validación

**Tests ejecutados:**
```
pytest tests/ -v
```

**Resultado:**
- ✅ 47/47 tests pasaron
- ✅ Sin errores de sintaxis
- ✅ Reglas críticas respetadas

---

## 🚀 Despliegue en Producción

### Pasos para aplicar en Render:

1. **Hacer push del código actualizado:**
   ```bash
   git add .
   git commit -m "Admin asigna nombres de participantes en registro"
   git push
   ```

2. **Ejecutar migración en Render:**
   - Conectarse a la shell de Render
   - Ejecutar: `python add_name_to_allowed_emails.py`
   - Verificar: Registros existentes tienen nombres asignados

3. **Actualizar emails permitidos existentes:**
   - Entrar como admin a `/admin/allowed-emails`
   - Verificar que todos tienen nombres apropiados
   - Editar si es necesario (requeriría nueva funcionalidad)

---

## 📝 Notas para Administradores

### Al habilitar nuevos emails:
1. Ve a `/admin/allowed-emails`
2. Completa los campos:
   - **Nombre:** El nombre que tendrá el participante (ej: "Juan Pérez")
   - **Email:** El email autorizado (ej: "juan.perez@observatorio.com")
3. Haz clic en "Agregar"
4. El usuario se registrará automáticamente con ese nombre

### Recomendaciones para nombres:
- Usar nombre completo (Nombre Apellido)
- Evitar apodos o sobrenombres
- Mantener consistencia (mayúsculas/minúsculas)
- Límite: 100 caracteres

---

## 🔒 Reglas Críticas Respetadas

✅ **Emails permitidos PRIMERO** - Orden de validación intacto  
✅ **Admins no pronostican** - Sin cambios en esa lógica  
✅ **Tests críticos pasan** - `test_register_email_not_allowed` ✓  
✅ **Sistema de puntos** - Sin cambios  
✅ **Timezone UTC** - Sin cambios  

---

## 🐛 Troubleshooting

### Error: "NOT NULL constraint failed: allowed_emails.name"
**Causa:** No se ejecutó la migración  
**Solución:** Ejecutar `python add_name_to_allowed_emails.py`

### Los usuarios existentes tienen nombres raros
**Causa:** Migración usó parte del email como nombre por defecto  
**Solución:** 
1. Crear endpoint para editar AllowedEmail (futuro)
2. O actualizar manualmente en base de datos

---

**Última actualización:** 28 de Febrero, 2026  
**Autor:** Sistema automático de cambios
