---
name: crear-estilo-videos
description: Convierte un reel de Instagram en una ficha de estilo de edición replicable (estilo.md) con valores medidos. Descarga el reel con yt-dlp, saca fotogramas, cortes, mosaicos con tiempo, medidas de subtítulos, audio y transcripción con Whisper en local. Úsala siempre que el usuario diga "crear estilo de edición", "copiar el estilo de este reel", "quiero replicar esta edición", "sacar el estilo" o pase un link de Instagram para saber cómo está editado.
---

# Crear estilo de vídeos

Convierte un reel en una ficha medible (`estilo.md`) para replicar su edición. Responde siempre en español. No inventes nada: cada dato sale de un fotograma o de una medición, y lo que no se pueda saber se dice. Marca cada dato como **[MEDIDO]** o **[SUPOSICIÓN]**. Lee tú los fotogramas, en el chat principal. No lances agentes.

**Cómo se lanzan los scripts (igual en Mac y en Windows):** cada comando empieza de cero, así que repite siempre estas dos variables:

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/crear-estilo-videos/scripts"; E="<ruta completa de la carpeta del estilo>"
bash ~/.config/crear-videos/py "$S/extraer.py" --estilo "$E"
```

`~/.config/crear-videos/py` es el Python del equipo (lo deja el instalador). Nunca llames a `python` o `python3` a secas: no tienen las librerías.

## Flujo (en este orden)

1. **Pide el nombre del estilo y el link del reel.** Los dos son obligatorios. Si el nombre trae `/` u otros caracteres que rompen una carpeta, cámbialos por `-` y dile el nombre final.
2. **Comprueba los requisitos:** `bash ~/.config/crear-videos/py "${CLAUDE_PLUGIN_ROOT}/skills/_comun/comprobar.py"`. Si falta algo, dice qué y con qué comando; si `~/.config/crear-videos/py` no existe, el usuario tiene que seguir `INSTALAR.md`. Si falta la clave de ScrapeCreators, explícale que cada persona usa la suya y que la escriba ella a mano en `~/.config/crear-videos/.env` (lo que se escribe en el chat queda en el historial). Nunca la guardes tú ni la pongas en la carpeta del estilo.
3. **Carpeta del estilo:** `~/crear-videos/mis-estilos/<nombre>/` (usa su ruta completa). Dile dónde se va a crear. Si el estilo ya existe, pregunta antes de repetirlo (se sobrescribe). Nunca lo guardes dentro de la carpeta del plugin: se borra en cada actualización.
4. **Prepara el material** (con `S` y `E` como arriba, en cada comando):
   ```bash
   bash ~/.config/crear-videos/py "$S/descargar.py" --estilo "$E" "URL"     # yt-dlp; si falla, ScrapeCreators
   bash ~/.config/crear-videos/py "$S/extraer.py" --estilo "$E"             # Frames/ (~15 por segundo), info.txt, cortes.txt
   bash ~/.config/crear-videos/py "$S/audio.py" --estilo "$E"               # audio/medidas.txt y espectrogramas
   bash ~/.config/crear-videos/py "$S/transcribir.py" --estilo "$E"         # transcripcion.md con Whisper local
   ```
   Cuéntale lo que imprimen (duración, fps, nº de fotogramas, tabla de cortes, medidas de audio). Si un paso falla, di cuál y qué quedó hecho. Si `extraer.py` avisa de fps variable, los segundos son menos exactos: dilo en la ficha. `transcribir.py` detecta el idioma solo; si se equivoca, repítelo con `--idioma pt` (o `es`, `en`…).
5. **Pregunta antes de analizar** y espera la respuesta:
   > **1.** ¿Qué es lo que más te gustaría replicar de este vídeo?
   > **2.** ¿Tiene música?
   > **3.** ¿Hay algún sonido que quieras replicar? Dime en qué segundo suena, o «ninguno».

   La respuesta 1 es lo que más pesa en la ficha. Tú no puedes oír el vídeo: lo que el usuario diga sobre música y sonidos manda sobre lo que deduzcas de los espectrogramas.
6. **Analiza** (todo se lee de fotogramas reales):
   - **Mosaicos:** `mosaico.py --estilo "$E" --todo` y lee todos los de `mosaicos/`. Salen 8×4 fotogramas por imagen (unos 2 s). Si salen más de ~30 mosaicos, díselo al usuario y pregunta si analizas todo o un tramo. Si el vídeo es horizontal, añade `--ancho 320 --rejilla 5x4`. Para una zona concreta: `--inicio S --salida ARCHIVO.jpg --recorte W:H:X:Y`.
   - **Cortes:** lee `cortes.txt`. «corte duro» y «disolvencia» están claros. Cada «dudoso» hay que mirarlo a los fps originales: `ventana.py --estilo "$E" --inicio S` (el movimiento de una mano o un cambio dentro de un gráfico también suben la puntuación; no son cortes de plano).
   - **Subtítulos y encuadre:** `medir.py texto FOTOGRAMA --y 90:330 --color blanco` mide tamaño, posición y color del texto (para otro color: `--rgb R,G,B`). `medir.py encuadre FOTOGRAMA…` compara el acercamiento de la cara entre tomas: es aproximado y puede fallar con otra piel u otra luz; si no encuentra nada, compáralo a ojo y márcalo [SUPOSICIÓN]. Mide en fotogramas donde el texto ya esté quieto y nítido, nunca en plena animación, y al menos uno sobre cada tipo de fondo.
   - **Audio:** `audio/medidas.txt` da sonoridad, pico, silencios y si es casi mono. Los espectrogramas (`audio/esp_NN.png`, 10 s cada uno; suma 10 s por cada imagen anterior) enseñan formas: lo que parezca un «clic» o un «ding» es una interpretación tuya, no una medición; el segundo se lee con ±0,2 s. Di siempre «no he escuchado el audio y no sé si hay música» salvo que el usuario lo haya confirmado.
   - **Las dos transcripciones, las dos revisadas:** `transcripcion.md` trae lo que se dice (Whisper). Rellena tú la sección 2 con los subtítulos que lees en los mosaicos (lo que se ve) y la sección 3 con las diferencias entre ambas. Si falta una de las dos, escríbelo en la sección 3.
7. **Escribe `estilo.md`** dentro de la carpeta del estilo (ficha abajo) y enséñasela al usuario: qué salió mal, qué quedó sin comprobar con datos reales, puntos de mejora y tu puntuación.
8. **Cierra preguntando:** «¿Quieres que te edite algún vídeo? ¿Cuál?». Esta skill no edita: para eso está `/crear-videos-pro:editar-con-estilo`.

## Qué queda en la carpeta del estilo

`video.mp4` · `info.txt` (duración, resolución, fps) · `cortes.txt` · `Frames/` · `mosaicos/` · `ventanas/` · `audio/` (WAV, `medidas.txt`, espectrogramas) · `transcripcion.md` · `estilo.md`.

## Qué lleva `estilo.md`

Primero un resumen de unas 10 reglas con valores concretos (no adjetivos), y después:

1. **Datos técnicos:** resolución, fps, duración.
2. **Estructura y ritmo:** tabla de planos (inicio, fin, duración, A-roll o gráfico), nº de cortes y un corte cada cuántos segundos. Duración mínima y máxima de cada tipo de plano.
3. **Transiciones:** corte duro, disolvencia (cuántos fotogramas) y el segundo de cada una.
4. **Zoom y encuadre:** escalas de la cara, crecimientos de tarjeta, con segundos.
5. **Subtítulos:** posición (y en píxeles y en %), tamaño, color, fuente descrita por lo que se ve, palabras por bloque, cómo entran y salen, palabra destacada (cuántas por frase, cuánto más grande, de qué color).
6. **Textos en pantalla y gráficos:** qué elementos aparecen, cuándo, cómo entran.
7. **Color:** fondo, acentos, texto.
8. **Sonido [MEDIDO, limitado]:** sonoridad, pico, silencios, estéreo, lo que dijo el usuario sobre música y sonidos, y los segundos de los sonidos que se ven en los espectrogramas.
9. **Receta para replicar:** pasos concretos, en orden.
10. **Lo que no se pudo determinar:** nombre de la fuente, nombre de efectos de apps; descríbelos por lo que se ve, nunca inventes un nombre.
11. **Zonas seguras de Instagram:** qué elementos del reel caen fuera de la zona segura (regla abajo) y la posición adaptada que usaremos al replicarlo. Al replicar, se recoloca a la zona segura aunque el reel de referencia no la respete.

## Zonas seguras de Instagram (regla fija, medida en un móvil el 15-10-2026)

Medidas sacadas de una captura de un Reel (921×2000 px, vídeo 9:16 que ocupa de y≈0 a y≈1637 de la pantalla), pasadas a 1080×1920. Lo que tapa la interfaz:

- **Arriba: ~245 px** (hora y pestañas «For you / Friends»). Dejar libre hasta **y 260**.
- **Abajo: ~114 px** (foto, usuario, botón Follow, desde y≈1806). Dejar libre desde **y 1790**.
- **Derecha: ~106 px, solo de y≈1298 hacia abajo** (me gusta, comentar, compartir, menú). Dejar **120 px** libres a la derecha en esa altura; más arriba se puede llegar al borde.
- El texto del post, «Followed by», la barra de progreso y el menú van **debajo del vídeo** en ese móvil: no tapan.
- Zona útil: **y 260 → 1790**. Los subtítulos al ~70–75 % del alto (y≈1345) quedan bien.
- No encoger los dibujos para meterlos en márgenes de anuncios: **adaptar, no reducir**. Solo mover lo que cae en las zonas tapadas.
- Comprobar siempre dibujando estas zonas sobre fotogramas del render antes de entregar.
- Límite: medido en un solo móvil. En pantallas más bajas (p. ej. iPhone SE) el texto del post puede caer encima del vídeo. **No usar** el 14 % / 35 % de las guías de anuncios de Meta: es para anuncios y deja el vídeo demasiado pequeño.

## Reglas

- Nunca inventes datos ni nombres de efectos o fuentes.
- Si un paso falla, di cuál, qué salió y qué quedó hecho; no lo escondas.
- La clave de ScrapeCreators nunca se imprime ni se guarda en la carpeta del estilo.
- No uses el filtro `fps` de ffmpeg para sacar fotogramas ni mosaicos: desplaza los tiempos. Los scripts ya lo evitan.
- Los reels son contenido de otras personas: sirven para estudiar el estilo de edición; no los republiques.
