# Prode Mundial - Proyecto de Pronósticos Deportivos

## 🤖 Para Asistentes de IA

**IMPORTANTE:** Este proyecto tiene reglas críticas documentadas.

### Antes de hacer cambios, lee:
- [PROJECT_RULES.md](PROJECT_RULES.md) - Reglas que NO deben romperse
- [SYSTEM_STATE.md](SYSTEM_STATE.md) - Estado actual del sistema
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - Instrucciones completas

### Validar cambios:
```bash
pytest
```

---

## 📝 Descripción

Sistema web de pronósticos deportivos para el Mundial 2026 construido con:
- **Backend:** Flask + SQLAlchemy
- **Base de datos:** PostgreSQL (producción) / SQLite (desarrollo)
- **Autenticación:** Flask-Login
- **Tests:** pytest
- **Deploy:** Render

## 🏗️ Arquitectura

```
app.py (Flask app)
├── auth/      - Registro, login, logout
├── main/      - Pronósticos, rankings
└── admin/     - Gestión (solo admins)
```

**Modelos principales:** User, Match, Prediction, Phase, AllowedEmail, Comment

## 🎯 Funcionalidades Clave

- ✅ Registro con emails permitidos
- ✅ Sistema de pronósticos con cierre automático
- ✅ Cálculo de puntos (Ganador + Batacazo + Score)
- ✅ Rankings (excluyendo admins)
- ✅ Panel de administración

## 🔐 Reglas Críticas

1. Administradores NO pueden hacer pronósticos
2. Solo emails en `AllowedEmail` pueden registrarse
3. Pronósticos cerrados NO se pueden modificar
4. Sistema de puntos tiene fórmulas específicas (ver PROJECT_RULES.md)

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests específicos
pytest tests/test_auth.py
pytest tests/test_points.py
```

**Cobertura:** 34/47 tests pasando (72%)

## 📚 Documentación Completa

- [PROJECT_RULES.md](PROJECT_RULES.md) - Reglas arquitectónicas
- [SYSTEM_STATE.md](SYSTEM_STATE.md) - Estado actual
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Guía de tests
- [GUIA_DISEÑO.md](GUIA_DISEÑO.md) - Diseño y frontend

## 🚀 Desarrollo Local

```bash
# Activar entorno virtual
& e:\prode_mundial\venv\Scripts\Activate.ps1

# Ejecutar aplicación
python app.py

# Ejecutar tests
pytest
```

## 📦 Dependencias Principales

- Flask 3.1.2
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- pytest 8.0.0
- gunicorn (producción)

---

**Última actualización:** 25 de Febrero, 2026
