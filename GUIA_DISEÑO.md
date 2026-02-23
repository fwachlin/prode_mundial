# 🎨 Guía de Trabajo con Ramas de Diseño

## 📊 Estado Actual

### Ramas Creadas:
- ✅ `main` - Versión funcional base (sin diseño)
- ✅ `design/bootstrap-theme` - Diseño con Bootstrap 5 ⭐ (estás aquí)

### Cambios Implementados en `design/bootstrap-theme`:

#### 1. **Bootstrap 5 Integrado**
   - CDN de Bootstrap CSS y JS
   - Bootstrap Icons incluidos
   - Google Fonts (Inter) para tipografía moderna

#### 2. **Navbar Mejorado**
   - Diseño oscuro con gradiente verde
   - Responsive (hamburger menu en móvil)
   - Iconos en cada opción
   - Dropdown para usuario logueado

#### 3. **Templates Actualizados**
   - ✅ `base.html` - Estructura completa con Bootstrap
   - ✅ `auth/login.html` - Formulario moderno con iconos
   - ✅ `auth/register.html` - Formulario mejorado
   - ✅ `main/index.html` - Hero section, cards, countdown mejorado

#### 4. **CSS Personalizado** (`site.css`)
   - Variables de color temáticas
   - Gradientes personalizados
   - Estilos para cards, botones, tablas
   - **Sección preparada para tus imágenes** (línea ~200)
   - Animaciones y hover effects

#### 5. **Estructura de Imágenes**
   - `/static/images/backgrounds/` - Para fondos
   - `/static/images/teams/` - Para escudos
   - `/static/images/players/` - Para jugadores
   - `/static/images/stadiums/` - Para estadios
   - Incluye `README.md` con instrucciones

---

## 🚀 Cómo Trabajar con las Ramas

### **Ver tu rama actual:**
```powershell
git branch
# El asterisco (*) indica tu rama actual
```

### **Cambiar entre ramas:**

#### Volver a `main` (versión sin diseño):
```powershell
git checkout main
```

#### Volver a `design/bootstrap-theme`:
```powershell
git checkout design/bootstrap-theme
```

### **Ver los cambios del diseño:**
```powershell
# Ver qué archivos cambiaron
git diff main design/bootstrap-theme --name-only

# Ver diferencias detalladas
git diff main design/bootstrap-theme
```

---

## 📸 Agregar Imágenes

### Paso 1: Conseguir imágenes
Descarga fotos de:
- **Unsplash**: https://unsplash.com/s/photos/football-stadium
- **Pexels**: https://www.pexels.com/search/soccer/
- Wikipedia (escudos oficiales)

### Paso 2: Colocar en carpetas
```
static/images/
  backgrounds/
    stadium.jpg       ← Tu foto de estadio favorita
    world_cup.jpg     ← Imagen del mundial
  teams/
    argentina.png     ← Escudo de Argentina
    brasil.png        ← Escudo de Brasil
  players/
    messi.jpg         ← Fotos de jugadores
```

### Paso 3: Activar imagen de fondo en hero
Edita `static/css/site.css`, línea ~200:
```css
.hero-with-bg {
  background-image: linear-gradient(rgba(26, 71, 42, 0.85), rgba(45, 106, 79, 0.85)), 
                    url('/static/images/backgrounds/stadium.jpg');
  /* 👆 Cambia "stadium.jpg" por el nombre de tu imagen */
}
```

### Paso 4: Guardar cambios
```powershell
git add static/images/
git commit -m "feat: agregar imágenes de estadios y equipos"
git push origin design/bootstrap-theme
```

---

## 🎨 Crear Otra Rama de Diseño (Alternativa)

Si quieres probar otro estilo sin perder este:

```powershell
# Asegúrate de estar en main
git checkout main

# Crea nueva rama
git checkout -b design/minimal-modern

# Haz tus cambios...
# Guarda:
git add .
git commit -m "feat: diseño minimalista"
git push -u origin design/minimal-modern
```

---

## 🔄 Comparar Diseños

### Ver sitio con Bootstrap:
```powershell
git checkout design/bootstrap-theme
python app.py
# Abre http://localhost:5000
```

### Ver sitio sin diseño (original):
```powershell
git checkout main
python app.py
# Abre http://localhost:5000
```

### Comparar visualmente:
1. Toma screenshots de cada versión
2. Decide cuál te gusta más
3. Puedes mezclar ideas de ambas

---

## ✅ Aplicar el Diseño a Producción

Cuando estés satisfecho con `design/bootstrap-theme`:

```powershell
# 1. Ve a main
git checkout main

# 2. Mergea los cambios
git merge design/bootstrap-theme

# 3. Resuelve conflictos si hay (generalmente no habrá)

# 4. Sube a producción
git push origin main
```

---

## 🛠️ Comandos Útiles

```powershell
# Ver todas las ramas (locales y remotas)
git branch -a

# Ver diferencias entre ramas
git diff main design/bootstrap-theme

# Eliminar rama (si ya no la necesitas)
git branch -d design/bootstrap-theme
git push origin --delete design/bootstrap-theme

# Ver historial de commits
git log --oneline --graph --all

# Crear rama desde rama actual
git checkout -b design/nueva-idea
```

---

## 📋 Próximos Pasos Recomendados

### 1. **Probar el diseño Bootstrap** (ahora)
   - Ejecuta `python app.py`
   - Navega por todas las páginas
   - Toma notas de lo que te gusta/no te gusta

### 2. **Agregar tus imágenes**
   - Descarga 2-3 fotos de estadios
   - Consigue escudos de selecciones
   - Colócalas en las carpetas correctas

### 3. **Personalizar colores** (opcional)
   - Edita `site.css`, variables en línea 1-15
   - Cambia gradientes, colores primarios

### 4. **Mejorar templates restantes**
   - `rankings.html`
   - `predictions.html`
   - `tablon.html`
   - `admin/dashboard.html`

### 5. **Decidir y mergear**
   - Cuando estés feliz, mergear a `main`
   - O crear más ramas para probar otras ideas

---

## 💡 Tips

- **No tengas miedo de experimentar**: las ramas te protegen
- **Commits frecuentes**: guarda cada cambio pequeño
- **Screenshots**: documenta visualmente cada versión
- **Pide feedback**: muestra a amigos/colegas

---

## 🆘 Ayuda Rápida

Si algo sale mal:

```powershell
# Descartar cambios no guardados
git checkout .

# Volver a commit anterior
git reset --hard HEAD~1

# Ver qué cambió
git status
```

¡Estás listo para hacer tu sitio hermoso! ⚽🎨
