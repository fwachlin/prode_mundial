# 📊 Configuración de Google Analytics 4 - Guía Paso a Paso

## ✅ Código Ya Implementado

El código de Google Analytics ya está integrado en tu aplicación. Solo necesitas:
1. Crear tu cuenta de Google Analytics
2. Obtener tu ID de medición
3. Configurarlo en Render

---

## 🚀 PASO 1: Crear Cuenta de Google Analytics

### 1.1 Ir a Google Analytics
- Abre: https://analytics.google.com
- Haz clic en **"Comenzar a medir"** (o **"Start measuring"**)
- Inicia sesión con tu cuenta de Google

### 1.2 Crear Cuenta
- **Nombre de la cuenta:** `Prode Mundial` (o el nombre que prefieras)
- Marca las casillas de compartir datos (opcional, recomendado)
- Clic en **"Siguiente"**

### 1.3 Crear Propiedad
- **Nombre de la propiedad:** `Prode Mundial 2026`
- **Zona horaria:** Selecciona tu país (ej: `(GMT-03:00) Argentina`)
- **Moneda:** Tu moneda local (ej: `Peso argentino - ARS`)
- Clic en **"Siguiente"**

### 1.4 Detalles del Negocio
- **Sector:** Selecciona lo más cercano (ej: `Juegos y entretenimiento`)
- **Tamaño de la empresa:** Selecciona `Pequeña (1-10 empleados)`
- **Uso de Analytics:** Marca `Medir el compromiso del usuario`
- Clic en **"Crear"**

### 1.5 Aceptar Términos
- Acepta los términos de servicio
- Clic en **"Acepto"**

---

## 🔑 PASO 2: Obtener tu ID de Medición

### 2.1 Configurar Flujo de Datos
Después de crear la propiedad, verás **"Recopilación de datos"**:

- Selecciona **"Web"**
- **URL del sitio web:** `https://tu-app.onrender.com` (reemplaza con tu URL de Render)
- **Nombre del flujo:** `Prode Mundial Web`
- Clic en **"Crear flujo"**

### 2.2 Copiar ID de Medición
Verás una pantalla con:

```
ID de medición
G-XXXXXXXXXX
```

**🔥 IMPORTANTE:** Copia este ID (empieza con `G-`). Lo necesitarás en el siguiente paso.

Ejemplo: `G-1A2B3C4D5E`

---

## ⚙️ PASO 3: Configurar en Render

### 3.1 Ir a tu Dashboard de Render
- Abre: https://dashboard.render.com
- Selecciona tu servicio `prode-mundial` (o como lo hayas llamado)

### 3.2 Agregar Variable de Entorno
- Ve a la pestaña **"Environment"** (en el menú lateral)
- Haz clic en **"Add Environment Variable"**
- Agrega:
  - **Key:** `GA_MEASUREMENT_ID`
  - **Value:** `G-XXXXXXXXXX` (tu ID copiado del paso anterior)
- Clic en **"Save Changes"**

### 3.3 Esperar el Redespliegue
Render automáticamente redesplegará tu aplicación (toma 2-3 minutos).

---

## 🧪 PASO 4: Verificar que Funciona

### 4.1 Visitar tu Sitio
- Abre tu app en Render: `https://tu-app.onrender.com`
- Navega por algunas páginas (home, login, ranking, etc.)

### 4.2 Ver los Datos en Google Analytics
- Vuelve a https://analytics.google.com
- En el menú lateral, ve a **"Informes" → "Tiempo real"**
- Deberías ver:
  - `1 usuario activo ahora` (o más si hay otros visitando)
  - Las páginas que visitaste
  - Tu ubicación en el mapa

**⏰ Nota:** Los datos en tiempo real aparecen en segundos. Los informes completos tardan ~24 horas.

---

## 📈 PASO 5: Ver Estadísticas (después de 24-48h)

Una vez que tengas datos, podrás ver:

### Dashboard Principal
- **Usuarios:** Cuántas personas visitaron (últimos 7 días, 30 días, etc.)
- **Nuevos usuarios vs. Recurrentes**
- **Sesiones:** Número total de visitas
- **Páginas vistas:** Total de páginas cargadas

### Informes Útiles

#### 📍 Informes → Adquisición → Tráfico
- **De dónde vienen:** Directo, Google, redes sociales, etc.

#### 🌍 Informes → Demográficos → Ubicaciones
- **Países y ciudades** de tus visitantes

#### 📄 Informes → Interacción → Páginas y pantallas
- **Páginas más visitadas:** `/`, `/login`, `/ranking`, etc.
- **Tiempo en cada página**

#### 📱 Informes → Tecnología → Detalles tecnológicos
- **Dispositivos:** Desktop, móvil, tablet
- **Navegadores:** Chrome, Firefox, Safari, etc.
- **Sistemas operativos:** Windows, Android, iOS, etc.

---

## 🔍 Verificar que Está Instalado (Técnico)

Si quieres confirmar que el código está en tu sitio:

1. Abre tu app en el navegador
2. Presiona `F12` (abrir DevTools)
3. Ve a la pestaña **"Console"**
4. Escribe: `gtag`
5. Si ves `ƒ gtag(){dataLayer.push(arguments);}` → **✅ Está instalado**
6. Si ves `undefined` → **❌ No está instalado** (verifica variable de entorno)

---

## 🧹 Desactivar Google Analytics (Local)

En tu computadora local, Google Analytics **NO** se activará automáticamente porque no tienes la variable de entorno `GA_MEASUREMENT_ID` configurada.

Si quieres probarlo localmente:

```powershell
# En PowerShell (Windows)
$env:GA_MEASUREMENT_ID = "G-XXXXXXXXXX"
python app.py
```

```bash
# En Linux/Mac
export GA_MEASUREMENT_ID="G-XXXXXXXXXX"
python app.py
```

**Recomendación:** No lo hagas. Deja que solo Render lo use para que tus visitas de prueba no contaminen las estadísticas.

---

## 📊 Métricas que Verás

### Métricas Básicas
- **Usuarios:** Personas únicas que visitaron
- **Sesiones:** Número total de visitas (un usuario puede tener varias sesiones)
- **Páginas vistas:** Total de páginas cargadas
- **Tasa de rebote:** % de usuarios que solo ven 1 página y se van
- **Duración promedio de sesión:** Tiempo promedio en el sitio

### Métricas Avanzadas (después de ~1 semana)
- **Usuarios activos:** Últimas 24h, 7 días, 28 días
- **Retención:** Cuántos usuarios vuelven
- **Conversiones:** Si configuraste objetivos (ej: registros, predicciones)

---

## 🎯 Próximos Pasos (Opcional)

### Configurar Eventos Personalizados
Puedes rastrear acciones específicas:

```html
<!-- Ejemplo: Botón de predicción -->
<button onclick="gtag('event', 'prediccion_enviada', {
    'partido_id': '{{ match.id }}',
    'usuario': '{{ current_user.username }}'
});">
    Enviar Predicción
</button>
```

### Vincular con Google Search Console
- Para ver cómo te encuentran en Google
- Palabras clave que traen tráfico

### Configurar Objetivos/Conversiones
- Registros completados
- Predicciones enviadas
- Tiempo en sitio > 2 minutos

---

## ❓ Preguntas Frecuentes

### ¿Cuánto cuesta?
**Gratis.** Google Analytics 4 es completamente gratuito.

### ¿Puedo ver visitas de ayer?
Sí, después de 24-48 horas los datos históricos estarán completos.

### ¿Afecta la velocidad del sitio?
No. El script es asíncrono (`async`) y no bloquea la carga.

### ¿Necesito avisar a los usuarios?
Depende de tu ubicación. En Europa (GDPR) necesitas un banner de cookies. En Argentina no es obligatorio, pero es buena práctica.

### ¿Puedo desactivarlo temporalmente?
Sí, simplemente elimina la variable `GA_MEASUREMENT_ID` de Render.

### ¿Qué pasa si no configuro la variable?
Nada. El código solo se activa si `GA_MEASUREMENT_ID` existe. Tu app funciona normal sin analytics.

---

## 📞 Soporte

- **Ayuda de Google Analytics:** https://support.google.com/analytics
- **Academia de Google Analytics:** https://analytics.google.com/analytics/academy/

---

## ✅ Checklist Final

- [ ] Cuenta de Google Analytics creada
- [ ] Propiedad "Prode Mundial 2026" creada
- [ ] Flujo de datos Web configurado
- [ ] ID de medición `G-XXXXXXXXXX` copiado
- [ ] Variable `GA_MEASUREMENT_ID` agregada en Render
- [ ] App redesplegada en Render
- [ ] Visitaste tu app para generar datos
- [ ] Viste datos en "Tiempo real" de Google Analytics
- [ ] 🎉 ¡Todo funcionando!

---

**Última actualización:** 2 de Marzo, 2026  
**Versión:** 1.0
