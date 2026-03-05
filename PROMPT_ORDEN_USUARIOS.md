# Prompt: Cambiar orden de usuarios en página de pronósticos

## Objetivo
Modificar la página "all_predictions" (📊 Pronósticos) para que los usuarios aparezcan en el orden en que se registraron en el prode, en lugar del orden alfabético actual.

## Contexto
Actualmente, en la página que muestra todos los pronósticos de todos los usuarios, los participantes aparecen ordenados alfabéticamente por nombre. Se desea cambiar esto para que aparezcan en el orden cronológico de registro (primero los que se anotaron primero).

## Cambio requerido

### Archivo a modificar
**Ruta:** `main/routes.py`  
**Función:** `all_predictions()` (aproximadamente línea 298)

### Cambio específico
**Línea actual (aproximadamente línea 301):**
```python
users = User.query.filter_by(is_admin=False).order_by(User.name).all()
```

**Cambiar a:**
```python
users = User.query.filter_by(is_admin=False).order_by(User.id).all()
```

## Justificación
- El campo `id` en la tabla `users` es un autoincremental que se asigna en el momento del registro
- Los usuarios con ID más bajo se registraron primero
- Ordenar por `User.id` preserva el orden cronológico de inscripción
- **No requiere modificaciones en la base de datos** (no se agregan columnas ni se cambian atributos)

## Resultado esperado
Cuando visites la página `/all-predictions`, los usuarios (columnas) aparecerán en el orden en que se registraron en el prode, mostrando primero a los que se anotaron antes.

## Validación
Después del cambio:
1. Ir a la página "📊 Pronósticos" 
2. Verificar que las columnas de usuarios ya no estén en orden alfabético
3. Confirmar que los usuarios con menor ID (registrados primero) aparecen a la izquierda

---

**Nota:** Este cambio solo afecta la visualización en la página de todos los pronósticos. No modifica rankings ni otras páginas.
