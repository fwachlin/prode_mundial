# 🛡️ TESTS SEGUROS - DOCUMENTACIÓN

## ✅ GARANTÍAS DE SEGURIDAD

Los tests están configurados para **NUNCA afectar la base de datos real** (`instance/prode.db`).

### Mecanismos de Protección

1. **Base de datos en memoria**: `'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'`
   - Los tests crean una DB temporal en RAM
   - Se destruye automáticamente al finalizar
   - IMPOSIBLE que afecte archivos del disco

2. **App independiente**: `test_app = Flask(__name__)`
   - NO importa `app.py` directamente
   - Crea una aplicación Flask completamente nueva
   - Sin conexión con la app de desarrollo

3. **Asserts de seguridad**:
   ```python
   assert test_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
   assert test_app.config['TESTING'] is True
   ```
   - Si la configuración es incorrecta, los tests fallan ANTES de ejecutarse

4. **Script de verificación**: `verify_tests_safe.py`
   - Verifica la configuración antes de ejecutar tests
   - Detecta imports peligrosos
   - Confirma que la DB real existe

## 🚀 Cómo Ejecutar Tests

### Opción 1: Con verificación automática
```powershell
python verify_tests_safe.py && pytest tests/
```

### Opción 2: Directamente (ya es seguro)
```powershell
pytest tests/
```

### Opción 3: Con verificación de que DB no cambia
```powershell
python verify_tests_safe.py
pytest tests/
```

## 📊 Cobertura de Tests

Actualmente: **47 tests pasando** ✅

| Módulo | Tests | Estado |
|--------|-------|--------|
| Autenticación | 11 | ✅ |
| Administración | 11 | ✅ |
| Pronósticos | 8 | ✅ |
| Puntos | 7 | ✅ |
| Modelos | 10 | ✅ |

## 🔍 Verificación Post-Test

Después de ejecutar tests, puedes verificar que la DB real NO fue modificada:

```powershell
# Ver timestamp de última modificación
Get-Item instance\prode.db | Select-Object Name, LastWriteTime

# Ver contenido (104 partidos deben existir)
python ver_db.py
```

## ⚠️ ¿Qué Hacer si la DB Fue Borrada?

Si por algún motivo la base de datos real fue borrada (NO debería pasar):

1. **Restaurar desde backup**:
   ```powershell
   python auto_backup.py restore
   ```

2. **O regenerar datos ficticios**:
   ```powershell
   python generar_datos_completos.py
   ```

## 📝 Tests Críticos (DEBEN Pasar Siempre)

Estos tests validan reglas de negocio críticas:

- ✅ `test_register_email_not_allowed` - Emails no permitidos rechazados
- ✅ `test_wrong_winner_zero_points` - Fallar ganador = 0 puntos
- ✅ `test_cannot_predict_closed_match` - No pronosticar en cerrados
- ✅ `test_admin_cannot_predict` - Admins no pronostican
- ✅ `test_rankings_exclude_admins` - Admins no en rankings

Si alguno falla, **NO mergear cambios**.

## 🔧 Troubleshooting

### "Tests fallan con BuildError"
**Solución**: Los blueprints no están registrados correctamente
- Verifica que `conftest.py` importa blueprints desde `.routes`

### "Tests borran datos reales"
**Solución**: 
1. Ejecuta `python verify_tests_safe.py`
2. Verifica que dice `sqlite:///:memory:`
3. Si no, revisa `tests/conftest.py` línea ~22

### "47 tests passed pero DB real cambió"
**Esto NO debería pasar**. Si pasa:
1. Verifica que `conftest.py` tiene `assert` de seguridad
2. Busca imports de `app` en archivos de test
3. Reporta el bug

## 📅 Última Actualización

**Fecha**: 25 de Febrero, 2026  
**Fix aplicado**: Tests ahora usan SQLite en memoria  
**Verificado**: ✅ 47 tests, DB real NO modificada

---

**Recuerda**: Siempre puedes ejecutar `python verify_tests_safe.py` para confirmar que todo está configurado correctamente.
