# 🧪 GUÍA DE TESTING - PRODE MUNDIAL

## 📝 Propósito

Los tests automatizados aseguran que:
1. ✅ Los cambios futuros no rompan funcionalidad existente
2. ✅ Las reglas críticas de `PROJECT_RULES.md` se cumplan
3. ✅ El estado documentado en `SYSTEM_STATE.md` se mantenga

---

## 🚀 Instalación

### 1. Instalar dependencias de testing

```powershell
# Activar entorno virtual
& e:\prode_mundial\venv\Scripts\Activate.ps1

# Instalar pytest y extensiones
pip install -r requirements.txt
```

---

## ▶️ Ejecutar Tests

### Todos los tests
```powershell
pytest
```

### Tests específicos
```powershell
# Solo autenticación
pytest tests/test_auth.py

# Solo sistema de puntos
pytest tests/test_points.py

# Solo pronósticos
pytest tests/test_predictions.py

# Solo admin
pytest tests/test_admin.py

# Solo modelos
pytest tests/test_models.py
```

### Con más información
```powershell
# Verbose (muestra cada test)
pytest -v

# Muy verbose (muestra prints)
pytest -vv

# Mostrar solo errores
pytest -q
```

### Tests específicos
```powershell
# Una clase específica
pytest tests/test_auth.py::TestRegistration

# Un test específico
pytest tests/test_auth.py::TestRegistration::test_register_success
```

---

## 📊 Cobertura de Tests

### Generar reporte de cobertura
```powershell
# Instalar coverage (si no está)
pip install pytest-cov

# Ejecutar con coverage
pytest --cov=. --cov-report=html

# Abrir reporte
start htmlcov/index.html
```

---

## 🎯 Tests Críticos por Área

### 1. Autenticación (`test_auth.py`)
- ✅ Registro con email permitido
- ✅ Rechazo de email no permitido
- ✅ Validación de contraseñas
- ✅ Login/logout
- ✅ Usuarios deshabilitados

**Por qué es crítico:**
- Protege el sistema de registros no autorizados
- Valida el orden correcto de validaciones (PROJECT_RULES.md Sección 3)

### 2. Sistema de Puntos (`test_points.py`)
- ✅ Pronóstico exacto (15+ puntos)
- ✅ Acertar ganador (10+ puntos)
- ✅ Fallar ganador (0 puntos)
- ✅ Batacazos (bonus)
- ✅ Empates

**Por qué es crítico:**
- El cálculo de puntos es la lógica central del sistema
- Cualquier cambio aquí afecta a todos los usuarios
- Fórmulas documentadas en PROJECT_RULES.md Sección 4

### 3. Pronósticos (`test_predictions.py`)
- ✅ Crear pronóstico en partido abierto
- ✅ Modificar pronóstico existente
- ✅ Rechazar pronóstico en partido cerrado
- ✅ Admins no pueden pronosticar
- ✅ Rankings excluyen admins

**Por qué es crítico:**
- Valida reglas de negocio (PROJECT_RULES.md Sección 5)
- Protege integridad de datos

### 4. Administración (`test_admin.py`)
- ✅ Solo admins acceden a /admin
- ✅ Crear/editar partidos
- ✅ Cargar resultados
- ✅ Gestionar usuarios

**Por qué es crítico:**
- Protege rutas sensibles
- Valida permisos (PROJECT_RULES.md Sección 7)

### 5. Modelos (`test_models.py`)
- ✅ Creación de entidades
- ✅ Hash de contraseñas
- ✅ Método `is_open()` de Match
- ✅ Constraints de DB

**Por qué es crítico:**
- Valida estructura de base de datos (PROJECT_RULES.md Sección 2)

---

## 🛠️ Escribir Nuevos Tests

### Estructura básica

```python
"""
tests/test_nueva_funcionalidad.py
"""
import pytest
from models import db, User, Match

class TestNuevaFuncionalidad:
    """Descripción de qué se testea"""
    
    def test_caso_exitoso(self, client, regular_user):
        """Test del caso feliz"""
        # Arrange - Preparar
        # ... configuración
        
        # Act - Ejecutar
        response = client.get('/ruta')
        
        # Assert - Verificar
        assert response.status_code == 200
    
    def test_caso_error(self, client):
        """Test del caso de error"""
        # ...
```

### Usar Fixtures

Fixtures disponibles en `conftest.py`:

```python
def test_mi_funcion(client, regular_user, open_match):
    # client: Cliente de test de Flask
    # regular_user: Usuario regular creado
    # open_match: Partido con pronósticos abiertos
    ...
```

**Fixtures disponibles:**
- `app` - Aplicación Flask
- `client` - Cliente de test
- `allowed_email` - Email permitido
- `regular_user` - Usuario regular
- `admin_user` - Usuario admin
- `open_match` - Partido abierto
- `closed_match` - Partido cerrado
- `finished_match` - Partido con resultado
- `prediction` - Pronóstico de ejemplo

---

## 🔍 Debugging Tests

### Test falló, ¿qué hacer?

#### 1. Ver detalles del error
```powershell
pytest -vv tests/test_auth.py::TestRegistration::test_register_success
```

#### 2. Ver prints en el test
```python
def test_debug(self, client):
    response = client.get('/ruta')
    print(response.data)  # Esto se mostrará con -s
    assert ...
```

```powershell
pytest -s tests/test_auth.py
```

#### 3. Usar debugger
```python
def test_debug(self, client):
    import pdb; pdb.set_trace()  # Breakpoint
    response = client.get('/ruta')
```

#### 4. Ver SQL queries
```python
def test_debug(self, app):
    with app.app_context():
        from flask import current_app
        current_app.config['SQLALCHEMY_ECHO'] = True
        # ... test
```

---

## ⚠️ Tests que DEBEN Pasar Siempre

Estos tests validan reglas críticas. Si fallan, **NO mergear cambios**:

### Autenticación
- `test_register_email_not_allowed` - Emails no permitidos rechazados
- `test_login_disabled_user` - Usuarios deshabilitados no pueden login

### Puntos
- `test_wrong_winner_zero_points` - Fallar ganador = 0 puntos
- `test_exact_prediction_max_points` - Exacto = máximo puntos

### Pronósticos
- `test_cannot_predict_closed_match` - No pronosticar en cerrados
- `test_admin_cannot_predict` - Admins no pronostican

### Admin
- `test_regular_user_cannot_access_admin` - Solo admins en /admin

---

## 📈 Workflow Recomendado

### Antes de hacer cambios
```powershell
# 1. Ejecutar todos los tests
pytest

# 2. Verificar que pasen
# ✅ Todos en verde → Continuar
# ❌ Alguno falla → Investigar antes de cambiar código
```

### Después de hacer cambios
```powershell
# 1. Ejecutar tests afectados
pytest tests/test_<modulo_modificado>.py

# 2. Si pasan, ejecutar todos
pytest

# 3. Si todo pasa, commit
git add .
git commit -m "Descripción del cambio"
```

### Al agregar funcionalidad nueva
```powershell
# 1. Escribir test primero (TDD)
# crear tests/test_nueva_feature.py

# 2. Ejecutar (debe fallar)
pytest tests/test_nueva_feature.py

# 3. Implementar funcionalidad

# 4. Ejecutar hasta que pase
pytest tests/test_nueva_feature.py

# 5. Ejecutar todos para no romper nada
pytest
```

---

## 🚨 Problemas Comunes

### "ModuleNotFoundError: No module named 'models'"

**Solución:**
```powershell
# Ejecutar desde la raíz del proyecto
cd e:\prode_mundial
pytest
```

### "FAILED tests/test_*.py - sqlalchemy.exc.OperationalError"

**Causa:** Problemas con base de datos en memoria

**Solución:**
- Verificar que `conftest.py` está creando las fases
- Verificar imports en el test

### "fixture not found"

**Causa:** Fixture no está en `conftest.py`

**Solución:**
- Agregar fixture a `tests/conftest.py`
- Verificar nombre de fixture

### Tests pasan localmente pero fallan en otro entorno

**Causa:** Dependencias de versión

**Solución:**
```powershell
pip freeze > requirements.txt
```

---

## 📝 Checklist Antes de Commit

- [ ] Todos los tests pasan (`pytest`)
- [ ] Tests nuevos agregados para funcionalidad nueva
- [ ] Tests críticos siguen pasando
- [ ] No hay tests deshabilitados con `@pytest.skip`
- [ ] Coverage no bajó significativamente

---

## 🎯 Objetivo Final

**Meta:** Tener confianza de que cambios futuros no rompen lo que ya funciona.

**Beneficio:** 
- ✅ Desarrollar más rápido
- ✅ Menos bugs en producción
- ✅ Documentación ejecutable del sistema
- ✅ Protección contra cambios accidentales

---

## 📞 Soporte

Si un test falla y no sabes por qué:
1. Lee el mensaje de error completo
2. Ejecuta con `-vv` para más detalles
3. Revisa `PROJECT_RULES.md` para entender la regla que se rompió
4. Revisa `SYSTEM_STATE.md` para ver el estado esperado

---

**Última actualización:** 25 de Febrero, 2026
