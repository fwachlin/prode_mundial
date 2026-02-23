# 🖼️ Guía de Imágenes - Prode Mundial 2026

Esta carpeta contiene todas las imágenes del sitio. Bootstrap está implementado y listo para mostrar tus fotos.

## 📁 Estructura de Carpetas

### `/backgrounds/`
**Imágenes de fondo para secciones hero**
- `stadium.jpg` - Foto de estadio para el hero principal (recomendado: 1920x800px)
- Sugerencias: Estadio Monumental, La Bombonera, estadios del mundial
- Formatos: JPG, PNG, WebP

### `/teams/`
**Escudos y logos de selecciones**
- `argentina.png`, `brasil.png`, etc.
- Tamaño recomendado: 200x200px (fondo transparente)
- Usar en cards de partidos y rankings

### `/players/`
**Fotos de jugadores destacados**
- Para cards especiales, highlights, estadísticas
- Tamaño recomendado: 400x600px (vertical)
- Ejemplos: messi.jpg, dibu_martinez.jpg

### `/stadiums/`
**Fotos de estadios específicos**
- Para mostrar en información de partidos
- Tamaño recomendado: 800x400px (horizontal)
- Nombrar según estadio: monumental.jpg, bombonera.jpg

## 🎨 Dónde se usan las imágenes

### 1. Hero Section (Página Principal)
```css
/* En site.css, línea ~200 */
.hero-with-bg {
  background-image: url('/static/images/backgrounds/stadium.jpg');
}
```
**Acción:** Coloca tu mejor foto de estadio en `/backgrounds/stadium.jpg`

### 2. Logos de Equipos en Partidos
```html
<!-- En templates cuando quieras mostrar logos -->
<img src="{{ url_for('static', filename='images/teams/argentina.png') }}" 
     class="team-logo" alt="Argentina">
```
**Acción:** Agrega escudos de selecciones en `/teams/`

### 3. Avatares de Usuarios
Actualmente usan iniciales, pero puedes agregar fotos:
```html
<img src="{{ url_for('static', filename='images/users/' + user.id + '.jpg') }}" 
     class="user-avatar">
```

### 4. Background del Navbar
Puedes agregar textura sutil al navbar editando en `site.css`:
```css
.navbar-dark {
  background-image: url('/static/images/backgrounds/texture.png');
}
```

## 💡 Tips para Imágenes

1. **Optimiza el tamaño**: Usa herramientas como TinyPNG antes de subir
2. **Nombres descriptivos**: `messi_celebrando.jpg` mejor que `img001.jpg`
3. **Formatos recomendados**:
   - Fotos: JPG (mejor compresión)
   - Logos con transparencia: PNG
   - Imágenes modernas: WebP (mejor calidad/tamaño)

4. **Responsive**: Las clases de Bootstrap ya están configuradas para que las imágenes se adapten

## 🚀 Ejemplo Rápido

Para empezar rápido, descarga estas imágenes (libres de derechos):

1. **Unsplash** (gratis): https://unsplash.com/s/photos/football-stadium
2. **Pexels** (gratis): https://www.pexels.com/search/soccer/
3. **Escudos oficiales**: Buscar en Wikipedia (citar fuente)

### Ejemplo de código para un partido con logos:

```html
<div class="match-card">
  <div class="d-flex justify-content-around align-items-center">
    <div class="text-center">
      <img src="{{ url_for('static', filename='images/teams/argentina.png') }}" 
           class="team-logo mb-2">
      <p class="fw-bold">Argentina</p>
    </div>
    <div class="display-4 text-muted">VS</div>
    <div class="text-center">
      <img src="{{ url_for('static', filename='images/teams/brasil.png') }}" 
           class="team-logo mb-2">
      <p class="fw-bold">Brasil</p>
    </div>
  </div>
</div>
```

## 📝 Próximos Pasos

1. Descarga/consigue tus imágenes favoritas
2. Colócalas en las carpetas correspondientes
3. Actualiza las rutas en los templates según necesites
4. Haz commit de los cambios: `git add . && git commit -m "feat: agregar imágenes"`

¡Listo para darle vida visual a tu Prode! ⚽🎨
