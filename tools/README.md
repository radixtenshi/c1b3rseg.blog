# Herramienta de publicación para Blogger

Publica notas del blog **c1b3rseg.blogspot.com** usando la Blogger API v3 de Google.
Las notas se redactan en Markdown dentro de `publicaciones/`, cada una en su propia
carpeta (`publicaciones/AAAA-MM-DD-titulo/`), y los adjuntos (imágenes, PDFs) viven
en `assets/` dentro de este repo.

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
python tools/publish.py post publicaciones/2026-10-12-obsidian-img/obsidian-img.md

# publicar directo
python tools/publish.py post publicaciones/2026-10-12-obsidian-img/obsidian-img.md --publicar

# listar posts con sus IDs
python tools/publish.py list

# pasar un borrador a publicado
python tools/publish.py publish <post-id>

# editar y republicar un post existente
python tools/publish.py update <post-id> publicaciones/.../nota.md --publicar

# borrar (pide confirmación)
python tools/publish.py delete <post-id>
```

## Estructura de las publicaciones (`publicaciones/*.md`)

Cada nota vive en su propia carpeta, nombrada `AAAA-MM-DD-titulo`:

```
publicaciones/
├── _plantilla.md
└── 2026-10-12-obsidian-img/
    └── obsidian-img.md
```

Formato del archivo `.md`:

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

Ver `publicaciones/_plantilla.md` como ejemplo.

## Flujo de trabajo sugerido

1. Redactar la nota en `publicaciones/AAAA-MM-DD-titulo/` (o pedírsela a OpenCode).
2. Subir los assets: `git add assets/... && git commit && git push`.
3. Publicar borrador: `python tools/publish.py post publicaciones/.../nota.md`.
4. Revisar en el blog y publicar: `python tools/publish.py publish <id>`.
