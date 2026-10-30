---
name: adaptar-para-subir
description: Deja imágenes y videos listos para subir a Instagram, Facebook o TikTok sin que Meta les ponga la etiqueta de AI. Reescribe los píxeles (JPEG 1080 de ancho), borra todos los metadatos incluido el manifiesto C2PA de ChatGPT/gpt-image, Sora, Gemini o Midjourney, y escribe como único dato la ubicación (por defecto Newark, New Jersey). Úsala siempre que el usuario pase una carpeta o archivos y diga "adáptalos para subir", "límpiales los metadatos", "quita lo de AI", "que no se note que es AI", "para Meta", "ponles que se hicieron en New Jersey" o parecido.
---

# Adaptar para subir

Sin preguntas. El usuario pasa una carpeta (o archivos) y recibe la carpeta lista para subir.

## Pasos

1. Ejecutar (ubicación por defecto: Newark, New Jersey; si el usuario nombró otra, pasar `--ciudad`, `--estado`, `--pais`, `--codigo`, `--lat`, `--lon`):
   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/skills/adaptar-para-subir/scripts/adaptar.sh" "<carpeta o archivos>"
   ```
   Por cada archivo imprime qué había antes (número de rastros de AI) y si quedó limpio. Los originales se mueven a `<carpeta>_originales`, fuera de la carpeta de subida, para que no se suba uno por error.
2. Si el script termina con "QUEDAN RASTROS" en algún archivo, mirarlo con `exiftool -a -G1` y `grep -aioE 'c2pa|openai|jumb'`, arreglarlo y volver a ejecutar. No darlo por bueno.
3. Responder en pocas líneas:
   - Qué había: la mayoría de las imágenes de Codex/ChatGPT traen manifiesto C2PA (agente "ChatGPT / gpt-image", origen "trainedAlgorithmicMedia", acción de marca de agua). Es lo que Meta lee para etiquetar.
   - Qué se hizo: recodificación a JPEG 1080 (destruye el bloque C2PA, no solo lo oculta), metadatos a cero, sin firma de ExifTool, ubicación escrita en GPS + IPTC + XMP. Videos: reempaquetados sin recodificar y sin metadatos, con la ubicación en `loci`, Keys de Apple (coordenadas y nombre) y `©xyz`, más ciudad/estado/país como atributos del Mac para que Finder los muestre.
   - Dónde están los originales.
   - **El límite, siempre y sin maquillar**: el manifiesto declara una marca de agua invisible en los píxeles. El reescalado y la recompresión la degradan mucho, pero no hay detector para confirmar que desapareció. Meta hoy etiqueta por metadatos y eso ya no está; si un día detectan por píxeles, esto no lo cubre. "Imposible" no existe.

## Detalles que ya están decididos

- Formato de salida: JPEG calidad 92, ancho 1080, alto proporcional (4:5 → 1080x1350, 1:1 → 1080x1080, 9:16 → 1080x1920). Es lo que Instagram genera de todas formas.
- Ubicación por defecto: Newark, NJ (40.7357, -74.1724). En video va en tres sitios: `loci` (lo escribe ffmpeg), y `com.apple.quicktime.location.ISO6709` (Keys) y `©xyz` (los añade exiftool). Medido con `mdls`: macOS solo lee el de Keys; `loci` y `©xyz` los ignora. Además se escribe el nombre `Ciudad, Estado` en Keys (`com.apple.quicktime.location.name`) y ciudad, estado y país como atributos del Mac (`com.apple.metadata:kMDItemCity`, `kMDItemStateOrProvince`, `kMDItemCountry`): es lo único que hace que Info de Finder muestre City / State or Province / Region en un video (el importador de Spotlight no los saca de ningún campo del mp4; probado). Esos atributos no van dentro del archivo y no viajan al subirlo; dentro del archivo van las coordenadas y el nombre. Para comprobarlo, `mdls archivo.mp4 | grep -i latit` (solo funciona en carpetas que Spotlight indexa, no en /tmp). Para comprobar `©xyz` por bytes hay que buscar el byte 0xA9 (`LC_ALL=C grep -aob $'\xa9xyz'`), no el `©` en UTF-8.
- No se inventan cámara, modelo ni fecha. Solo ubicación.
- Requiere `exiftool`, `ffmpeg` y el Python del equipo (`~/.config/crear-videos/py`, lo deja el instalador). Funciona en Mac y en Windows (Git Bash). Los atributos de Finder (ciudad, estado y país del vídeo) solo se escriben en el Mac.
