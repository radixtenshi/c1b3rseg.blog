---
title: "Img Cleanup: limpieza selectiva de adjuntos no vinculados en Obsidian"
labels: [Herramientas, Obsidian]
---

Si usás Obsidian para tomar notas, probablemente ya te pasó esto: pegás capturas, adjuntás PDFs, vas editando las notas y reemplazando contenido... y con el tiempo la carpeta de adjuntos se llena de archivos que ninguna nota referencia más. Borrarlos a mano es tedioso y siempre da cosa: ¿y si alguna nota todavía los usa?

Desarrollamos **Img Cleanup**, un plugin open source de Obsidian que resuelve exactamente ese problema, de forma selectiva y segura.

<!-- imagen: captura del modal con la lista de archivos desvinculados -->

## Qué hace

Img Cleanup escucha los cambios en tus notas `.md` (con un debounce de 1.5 segundos para no interrumpirte mientras escribís) y detecta qué adjuntos quedaron **desvinculados** mientras editabas. Si encontró archivos que ya no se referencian, abre un modal que los lista con un checkbox por archivo y dos acciones: **Delete** (mandar a la papelera) o **Keep** (dejarlos donde están).

No borra nada a ciegas: vos decidís archivo por archivo, o de una para todos desde el modal.

## Características

- **Detección en vivo:** monitorea los cambios en los `.md` del vault y compara las referencias antes/después de cada edición.
- **Formatos soportados:** `![](ruta)`, `![[archivo]]`, `[[archivo]]` y links de Markdown. Las URLs externas se ignoran.
- **Solo las carpetas que vos elijás:** por defecto `.img/` (configurable en Settings). Todo lo que esté fuera de esas carpetas se ignora por completo.
- **Backlinks como red de seguridad:** si otra nota todavía referencia el archivo, **ni siquiera se ofrece** para borrar.
- **Modal por lotes:** una sola ventana con todos los archivos desvinculados, con checkbox por archivo.
- **"No volver a preguntar":** podés persistir la última acción como política permanente (borrar siempre / conservar siempre). Se resetea a "preguntar" desde Settings.
- **Respeta la papelera de Obsidian:** usa `fileManager.trashFile()`, así que aplica tu configuración de papelera (carpeta `.trash` o papelera del sistema). Nunca borra permanente contra tu voluntad.
- **Trace log:** cada acción queda registrada en un archivo JSONL (fecha, archivo, nota de origen, destino y acción), con rotación y tope de 1000 entradas. El historial se ve desde un modal, con opción de abrir el archivo o limpiarlo.

<!-- imagen: captura de la configuración del plugin en Settings -->

## Instalación

Es manual, son dos archivos:

1. Crear la carpeta `.obsidian/plugins/img-cleanup/` dentro de tu vault.
2. Copiar `manifest.json` y `main.js` (ya vienen compilados en el repo) adentro.
3. Reiniciar Obsidian → **Settings → Community plugins** → habilitar **Img Cleanup**.

## Configuración

En **Settings → Img Cleanup**:

| Setting | Descripción |
|---|---|
| Enable plugin | Activa/desactiva el monitoreo |
| Watched folders | Carpetas monitoreadas, separadas por coma (por defecto `.img/`) |
| Permanent action | Estado de la política "no preguntar más" + botón para resetear a "Preguntar" |
| Trace history | Abre el modal con el log de acciones |

El log vive en `.obsidian/plugins/img-cleanup/data/appendix-log.jsonl`.

## Código fuente

El plugin es open source (licencia MIT) y el código está disponible en GitHub:

**https://github.com/radixtenshi/obsidian-img**

Está escrito en TypeScript con esbuild para el bundle. El repo incluye también el documento de lineamientos de desarrollo y la estructura del código, por si querés contribuir o adaptarlo a tu vault.

## Qué no hace

Para que no haya sorpresas:

- No escanea archivos "huérfanos" globales del vault: solo detecta los que quedaron desvinculados mientras editabas.
- No maneja links entre notas: solo adjuntos e imágenes.
- No funciona con Canvas.

## Para probarlo

Si acumulaste esa carpeta de "imágenes que capaz alguna vez uso", instalalo, editá unas notas y mirá cómo el modal te muestra exactamente qué se quedó sin usar. El código, el README completo y las mejoras propuestas están en el repo de GitHub:

👉 **https://github.com/radixtenshi/obsidian-img**
