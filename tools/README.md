# Herramienta de publicación para Blogger

Publica notas del blog **c1b3rseg.blogspot.com** usando la Blogger API v3 de Google.
Las notas se redactan en Markdown dentro de `posts/` y los adjuntos (imágenes, PDFs)
viven en `assets/` dentro de este repo.

## Configuración inicial (una sola vez)

1. **Google Cloud Console** → <https://console.cloud.google.com/> → Crear proyecto
   (ej: `c1b3rseg-blog`).
2. **Habilitar la API**: <https://console.cloud.google.com/apis/library/blogger.googleapis.com>
   → *Enable*.
3. **Pantalla de consentimiento OAuth**:
   <https://console.cloud.google.com/apis/credentials/consent>
   - Usuario: *Externo*
   - Completar nombre, email de soporte
   - *Save and Continue*
   - En *Test users* → *Add users* → agregar tu Gmail (el con el que administrais el blog)
4. **Credenciales**:
   <https://console.cloud.google.com/apis/credentials>
   → *Create Credentials* → *OAuth client ID* → tipo **Desktop app** → *Create*
   → *Download JSON*.
5. Guardar el JSON descargado en `tools/client_secret.json`.
6. Instalar dependencias y autorizar:

```bash
pip install -r tools/requirements.txt
python tools/publish.py auth
```

`auth` abre el navegador, aceptás los permisos y el script queda autorizado
para siempre (renueva los tokens solo).

> El archivo `tools/client_secret.json` y el token generado
> (`tools/.blogger_token.json`) están en `.gitignore`: **nunca se suben al repo**.

## Uso

```bash
# crear un borrador (lo más seguro: revisar antes de publicar)
python tools/publish.py post posts/mi-nota.md

# publicar directo
python tools/publish.py post posts/mi-nota.md --publicar

# listar posts con sus IDs
python tools/publish.py list

# pasar un borrador a publicado
python tools/publish.py publish <post-id>

# editar y republicar un post existente
python tools/publish.py update <post-id> posts/mi-nota.md --publicar

# borrar (pide confirmación)
python tools/publish.py delete <post-id>
```

## Formato de las notas (`posts/*.md`)

```markdown
---
title: Título de la nota
labels: [Recursos, Linux]
---

Contenido en Markdown...

![captura](assets/mi-captura.png)
```

- `title` es obligatorio; `labels` es opcional (coma o lista).
- Las rutas relativas `assets/...` se reescriben automáticamente a
  `https://raw.githubusercontent.com/radixtenshi/c1b3rseg.blog/main/assets/...`
- **Importante**: subir y pushear los assets al repo *antes* de publicar,
  si no las imágenes no van a cargar.

Ver `posts/_plantilla.md` como ejemplo.

## Flujo de trabajo sugerido

1. Redactar la nota en `posts/` (o pedírsela a OpenCode).
2. Subir los assets: `git add assets/... && git commit && git push`.
3. Publicar borrador: `python tools/publish.py post posts/nota.md`.
4. Revisar en el blog y publicar: `python tools/publish.py publish <id>`.
