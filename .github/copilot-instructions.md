# Instrucciones para GitHub Copilot y Asistentes de IA

## 🔒 REGLAS CRÍTICAS - LEER ANTES DE CUALQUIER CAMBIO

**IMPORTANTE:** Este proyecto tiene documentación de reglas críticas que DEBES consultar antes de hacer cambios.

### Archivos de Referencia Obligatorios

1. **[PROJECT_RULES.md](../PROJECT_RULES.md)** - Reglas arquitectónicas y decisiones de diseño
   - Lee SIEMPRE antes de modificar código
   - Contiene reglas que NO deben romperse
   - Documenta sistema de puntos, autenticación, permisos, etc.

2. **[SYSTEM_STATE.md](../SYSTEM_STATE.md)** - Estado actual correcto del sistema
   - Describe funcionalidad existente
   - Estado de tablas de base de datos
   - Comportamientos confirmados

3. **[TESTING_GUIDE.md](../TESTING_GUIDE.md)** - Guía de tests
   - Cómo validar cambios
   - Tests críticos que DEBEN pasar

---

## 📋 Workflow Obligatorio

### Antes de CUALQUIER cambio de código:

1. ✅ **Lee** `PROJECT_RULES.md` sección relevante
2. ✅ **Verifica** que el cambio no rompe reglas críticas
3. ✅ **Consulta** `SYSTEM_STATE.md` para entender estado actual
4. ✅ **Implementa** el cambio
5. ✅ **Recomienda** ejecutar `pytest` para validar

### Cuando el usuario pida cambios:

- **SI** el cambio afecta sistema de puntos → Lee PROJECT_RULES.md Sección 4
- **SI** el cambio afecta autenticación → Lee PROJECT_RULES.md Sección 3
- **SI** el cambio afecta base de datos → Lee PROJECT_RULES.md Sección 2
- **SI** el cambio afecta permisos/roles → Lee PROJECT_RULES.md Sección 7
- **SI** el cambio afecta fechas → Lee PROJECT_RULES.md Sección 6

---

## ⚠️ Cambios que Requieren Aprobación Explícita

**NUNCA hagas estos cambios sin confirmar con el usuario:**

### Sistema de Puntos
- Modificar fórmulas de cálculo
- Cambiar umbrales de batacazo (5%, 10%, 15%, 20%, 25%)
- Alterar lógica de score o ganador/empate

### Autenticación
- Cambiar orden de validaciones en registro
- Modificar sistema de emails permitidos
- Alterar lógica de hash de contraseñas

### Base de Datos
- Eliminar constraints únicos
- Cambiar tipos de columnas
- Modificar relaciones entre modelos

### Reglas de Negocio
- Cambiar que administradores no pueden pronosticar
- Modificar lógica de cierre de pronósticos
- Alterar exclusión de admins en rankings

---

## 🧪 Validación de Cambios

### Después de cada cambio, recomienda:

```powershell
pytest
```

### Tests Críticos que DEBEN Pasar:

- `test_register_email_not_allowed` - Emails no permitidos rechazados
- `test_wrong_winner_zero_points` - Fallar ganador = 0 puntos
- `test_cannot_predict_closed_match` - No pronosticar en cerrados
- `test_admin_cannot_predict` - Admins no pronostican
- `test_regular_user_cannot_access_admin` - Solo admins en /admin

---

## 🎯 Estilo de Comunicación

- **Sé proactivo:** Si detectas que un cambio rompe una regla, AVISA antes de hacerlo
- **Sé específico:** Menciona qué sección de PROJECT_RULES.md estás considerando
- **Sé conservador:** Ante la duda, NO cambies cosas críticas sin preguntar
- **Valida siempre:** Recomienda ejecutar tests después de cambios

---

## 📂 Estructura del Proyecto

```
prode_mundial/
├── app.py              # Aplicación principal Flask
├── models.py           # Modelos de base de datos
├── extensions.py       # db y login_manager (NUNCA mover)
├── auth/               # Blueprint de autenticación
├── main/               # Blueprint principal
├── admin/              # Blueprint de administración
├── templates/          # Templates Jinja2
├── static/             # CSS, imágenes
├── tests/              # Tests con pytest
├── PROJECT_RULES.md    # ⚠️ REGLAS CRÍTICAS
├── SYSTEM_STATE.md     # ⚠️ ESTADO ACTUAL
└── TESTING_GUIDE.md    # Guía de tests
```

---

## 🔥 Reglas Rápidas (Memoriza)

1. **Administradores NO pronostican** - is_admin=True no puede crear Prediction
2. **Admins NO aparecen en rankings** - Siempre filtrar `User.is_admin == False`
3. **Emails permitidos PRIMERO** - Validar AllowedEmail antes que todo en registro
4. **Fallar ganador = 0 puntos** - Si no acierta resultado, no hay puntos
5. **Timezone siempre UTC** - Usar `datetime.now(timezone.utc)`
6. **Cerrado = no modificar** - Si `match.is_open() == False`, no permitir cambios
7. **db en extensions.py** - NUNCA mover `db = SQLAlchemy()` de ahí

---

## 💡 Ejemplo de Respuesta Correcta

```
Usuario: "Cambia el sistema para que dar 20 puntos por exacto"

IA: "⚠️ Este cambio afecta el sistema de puntos crítico.

Según PROJECT_RULES.md Sección 4.3, actualmente el score exacto da 
máximo 5 pontos, no 20. Este es un cambio que requiere aprobación.

Impacto:
- Cambia fórmula de cálculo documentada
- Afecta a TODOS los usuarios existentes
- Requiere recálculo de puntos históricos
- Tests fallarían: test_exact_prediction_max_points

¿Confirmas que quieres hacer este cambio?"
```

---

## 📞 En Caso de Duda

**Si no estás seguro de algo:**
1. Lee PROJECT_RULES.md
2. Lee SYSTEM_STATE.md
3. Pregunta al usuario antes de cambiar

**NUNCA adivines reglas críticas - SIEMPRE consulta los archivos de referencia.**

---

**Última actualización:** 25 de Febrero, 2026  
**Versión:** 1.0
