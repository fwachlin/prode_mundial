# 🧪 Tests del Prode Mundial

Este directorio contiene tests automatizados para validar la funcionalidad crítica del sistema.

## 📋 Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py              # Configuración de fixtures
├── test_auth.py             # Tests de autenticación
├── test_predictions.py      # Tests de pronósticos
├── test_admin.py            # Tests de admin
├── test_points.py           # Tests del sistema de puntos
└── test_models.py           # Tests de modelos
```

## 🚀 Ejecutar Tests

### Todos los tests
```powershell
pytest
```

### Tests específicos
```powershell
pytest tests/test_auth.py
pytest tests/test_points.py
```

### Con información detallada
```powershell
pytest -v
```

### Con coverage
```powershell
pytest --cov=. --cov-report=html
```

## ✅ Cobertura Actual

- ✅ Autenticación (registro, login, emails permitidos)
- ✅ Sistema de puntos (cálculo completo)
- ✅ Pronósticos (apertura/cierre, validaciones)
- ✅ Roles de admin
- ✅ Modelos de base de datos

## 📝 Agregar Nuevos Tests

1. Crear archivo `test_<funcionalidad>.py`
2. Importar fixtures de `conftest.py`
3. Escribir tests siguiendo el patrón AAA (Arrange-Act-Assert)
4. Ejecutar tests para validar

## 🎯 Objetivo

Los tests aseguran que cambios futuros no rompan funcionalidad crítica establecida en `PROJECT_RULES.md` y `SYSTEM_STATE.md`.
