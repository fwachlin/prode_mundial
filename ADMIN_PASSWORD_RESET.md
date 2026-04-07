# 🔑 Sistema de Reseteo de Contraseñas por Admin

## ✅ Implementado

Funcionalidad para que los administradores puedan resetear contraseñas de usuarios que las olvidaron.

## 📋 Cómo Usar

### 1. Acceso Admin
1. Iniciar sesión como administrador
2. Ir a **Panel de Control → Gestionar Usuarios**

### 2. Resetear Contraseña
1. Localizar al usuario en la tabla
2. Hacer click en el botón **"🔑 Resetear"**
3. Confirmar la acción en el diálogo
4. El sistema establece la contraseña: `olvidadizo1234`

### 3. Comunicar al Usuario
El admin debe comunicar al usuario por otro medio (WhatsApp, email personal, etc.):
```
Tu contraseña ha sido reseteada a: olvidadizo1234

Por favor:
1. Inicia sesión con esta contraseña
2. Ve a Configuración → Cambiar Contraseña
3. Establece una nueva contraseña personal
```

## 🔒 Seguridad

### Protecciones Implementadas:
- ✅ **Solo admins** pueden resetear contraseñas
- ✅ **No se puede** resetear contraseña de otros admins
- ✅ Confirmación antes de ejecutar
- ✅ La contraseña se **hashea** antes de guardar
- ✅ Notificación visual del cambio

### Contraseña por Defecto:
```
olvidadizo1234
```
- Simple de recordar
- Fácil de comunicar
- El usuario **DEBE** cambiarla inmediatamente

## 💡 Flujo Completo

```
Usuario olvida contraseña
         ↓
Contacta al Administrador
         ↓
Admin resetea contraseña → "olvidadizo1234"
         ↓
Admin comunica contraseña al usuario
         ↓
Usuario ingresa con contraseña temporal
         ↓
Usuario cambia su contraseña (Configuración)
         ↓
✅ Usuario puede usar su nueva contraseña
```

## 📝 Archivos Modificados

- `templates/admin/users.html` - Botón de reseteo
- `admin/routes.py` - Ruta POST `/admin/users/<id>/reset-password`

## 🚀 Deploy

Los cambios están en el commit `472bd96`:
```bash
feat: Admin puede resetear contraseñas de usuarios
```

Render detectará automáticamente el push y desplegará los cambios.

---

**Fecha de implementación:** 6 de Abril, 2026  
**Versión:** 1.0
