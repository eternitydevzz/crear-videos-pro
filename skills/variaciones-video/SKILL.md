---
name: variaciones-video
description: A partir de un video del usuario crea 5 variaciones listas para subir a Instagram (Trial Reels) o a X/Twitter, cada una con un texto de gancho distinto encima en los primeros segundos (e inicio, encuadre, velocidad y color distintos, sin metadatos), más 5 descripciones distintas, una por variación, con hashtags si van a Instagram. Úsala siempre que el usuario pase un video y pida "variaciones", "versiones", "copias", "5 videos", "ganchos", "trial reels" o "descripciones para Instagram/Twitter/X".
---

# Variaciones de video para Instagram o X

Rápido y simple. Una sola pregunta como mucho, y el usuario recibe el resultado.

## Paso 0: plataforma

Si el usuario no dijo a qué plataforma van, preguntarlo en una línea: **Instagram, X o las dos**. Si ya lo dijo (o lo dijo antes en la conversación), no preguntar. Mientras responde se puede ir ejecutando el paso 1.

| | Instagram (Trial Reels) | X |
|---|---|---|
| Largo de la descripción | 1–4 frases; sin límite práctico (2.200) | Máx. 280 caracteres (sin Premium) |
| Hashtags | Exactamente 5 (el máximo de Instagram), **los mismos en las 5 variaciones** | 0–2 |
| Duración máxima | 90 s como Reel | 2:20 sin Premium |
| CTA "comenta X" | Funciona (respuesta automática con ManyChat) | Avisar: en X los DMs se mandan a mano |

Si son las dos: los mismos 5 videos, y dos juegos de descripciones (`## v1 — Instagram` / `## v1 — X`).

## Pasos

1. Analizar:
   ```bash
   bash ~/.config/crear-videos/py "${CLAUDE_PLUGIN_ROOT}/skills/variaciones-video/scripts/variar.py" analizar "<ruta_del_video>"
   ```
   Crea `<nombre>_variaciones/` junto al video con `transcripcion.txt`, `palabras.json` y `fotogramas.jpg`.
2. Leer `transcripcion.txt` y mirar `fotogramas.jpg` para entender el video.
3. Escribir `ganchos.txt` en esa carpeta: exactamente 5 líneas, un gancho por línea (línea 1 = v1…).
   - Cada uno con un ángulo distinto: curiosidad, resultado concreto, error común, contraste/antes-después, pregunta directa.
   - Corto: 4–9 palabras. Sin emojis (la fuente no los dibuja). Mayúsculas iniciales normales, no todo en mayúsculas.
   - Debe cuadrar con lo que se dice o ve al inicio del video, no prometer algo que el video no da.
   - Público latino en EE. UU.: escribir "AI", no "IA".
4. Generar los videos:
   ```bash
   bash ~/.config/crear-videos/py "${CLAUDE_PLUGIN_ROOT}/skills/variaciones-video/scripts/variar.py" generar "<ruta_del_video>"
   ```
   Crea `<nombre>_v1.mp4` … `_v5.mp4`. El gancho sale arriba, en caja blanca, los primeros 3,5 s.
   Cada variación tiene su propio encuadre (zoom 3–10 % anclado a un lado distinto) y su propio inicio: v1 desde el principio y v2–v5 saltando ~1–3 s, siempre al inicio de una palabra y prefiriendo inicios de frase o pausas (usa `palabras.json`, transcrito con Whisper en local). El script imprime dónde empieza cada una: comprobar en `transcripcion.txt` que ninguna arranque de forma rara.
5. Revisar un fotograma de cada variación en el segundo 1 (que el gancho no tape la cara ni texto importante). Si lo tapa, cambiar `y=h*0.13` en `variar.py` para ese video y regenerar (el cambio se pierde al actualizar el plugin: es solo para ese video).
6. Escribir `descripciones.md` en la carpeta: 5 descripciones, una por variación (`## v1` … `## v5`), alineadas con el gancho de esa variación, con las reglas de la plataforma (tabla del paso 0).
   - Español, tono natural, sin sonar a IA (nada de "descubre", "increíble", emojis en cada línea).
   - Si el video pide comentar una palabra, mantener ese CTA.
   - **Hashtags para Instagram**: 5, al final, separados por una línea en blanco, idénticos en las 5 (si cambian, no se sabe si ganó el gancho o los hashtags). Mezcla: 1 amplio en inglés que usa el público (p. ej. `#AI`), 1 amplio en español (p. ej. `#inteligenciaartificial`), 1 del tema exacto con menos competencia y 2 de la marca/herramienta que sale en el video. Nunca genéricos tipo `#viral`, `#fyp`, `#reels`.
7. Comprobación final (el paso `generar` ya la hace con los videos; repetirla ahora para incluir `descripciones.md`):
   ```bash
   bash ~/.config/crear-videos/py "${CLAUDE_PLUGIN_ROOT}/skills/variaciones-video/scripts/variar.py" comprobar "<ruta_del_video>"
   ```
   Revisa cada variación en busca de marcas C2PA o etiquetas de AI, y los textos en busca de caracteres invisibles. Si encuentra algo, lo limpia (los videos se reempaquetan sin recodificar) y vuelve a comprobar. Si sale con error, algo quedó: decírselo al usuario, no ocultarlo.
8. Responder con:
   - La ruta de la carpeta y el resultado de la comprobación en una línea.
   - Por variación: el archivo, el gancho y la descripción completa (con hashtags) en un bloque de código, lista para copiar.
   - Avisar si el video pasa de la duración máxima de la plataforma.
   - Si es Instagram, recordar en 3 líneas cómo subirlas:
     - Las 5 como **Trial Reels**, una por día o cada dos días.
     - **Desactivar el compartir automático con seguidores** y decidir a mano con la ganadora.
     - Elegir la ganadora por retención en los primeros 3 s, tiempo medio de visualización y comentarios con la palabra del CTA, no solo por vistas (Instagram puede frenar alguna por parecida a las otras).

## Si el usuario trae resultados de los Trial Reels

Identificar qué ángulo de gancho ganó y usarlo como primer gancho (v1) en los próximos videos, manteniendo los otros 4 ángulos para seguir probando.
