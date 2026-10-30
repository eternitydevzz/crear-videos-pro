---
name: editar-con-estilo
description: Edita un vídeo de una persona hablando a cámara siguiendo una ficha de estilo (estilo.md). Corta los silencios, transcribe con tiempos por palabra, monta gráficos animados con HyperFrames, subtítulos palabra a palabra, música y efectos, y entrega el vídeo por pasadas. Úsala siempre que el usuario diga "edita mi vídeo", "edítalo con este estilo", "aplica el estilo", "edítalo como Maestria", pase un vídeo junto a un estilo.md, o después de usar crear-estilo-videos.
---

# Editar con estilo

Edita el vídeo del usuario aplicando un `estilo.md`. Responde siempre en español. No inventes nada: cada tiempo, color o medida sale del estilo, del vídeo o de una medición. Trabaja en el chat principal, sin agentes.

**Cómo se lanzan los scripts (igual en Mac y en Windows):** cada comando empieza de cero; repite siempre:

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/editar-con-estilo/scripts"
bash ~/.config/crear-videos/py "$S/cortar_silencios.py" --video VIDEO --salida CARPETA/trabajo
```

Nunca llames a `python` o `python3` a secas: no tienen las librerías.

**Dónde está cada cosa:**
- Estilos del equipo: `${CLAUDE_PLUGIN_ROOT}/estilos/Estilo Maestria/` (fichas, motores y herramientas) y `${CLAUDE_PLUGIN_ROOT}/estilos/creadores/`.
- Estilos que ha creado el usuario: `~/crear-videos/mis-estilos/`.
- Stock (música, sonidos, motions, logos, fuentes): `${CLAUDE_PLUGIN_ROOT}/stock/` (índice en `${CLAUDE_PLUGIN_ROOT}/STOCK.md`).
- Vídeos del usuario y todo lo que se crea: `~/crear-videos/mis-videos/`. Nunca escribas dentro de la carpeta del plugin: se sustituye entera al actualizar.

**Reglas con el usuario** (son las que más fallos evitan):
- Si algo no está claro, pregunta. No supongas.
- Haz solo lo que pide. No añadas ni cambies nada (textos, fuentes, tamaños, efectos) sin preguntar antes.
- Si lo que pide va contra el estilo o la zona segura, avísale una vez y haz lo que decida.
- Antes de cambiar el diseño de una escena, enséñale un fotograma y espera su visto bueno.
- Tú no oyes el audio: lo que diga el usuario sobre el sonido manda sobre tus mediciones.

**HyperFrames:** usa siempre el lanzador del plugin (`node <plugin de HyperFrames>/skills/hyperframes/scripts/plugin-cli.mjs <comando>`) y nunca `skills update`, porque rompe la instalación. Construye todas las escenas en este chat, aunque HyperFrames proponga repartirlas en agentes.

**Composición propia, nunca plantillas.** Construye una composición de HyperFrames hecha a medida para este vídeo. No uses los flujos ni los temas que trae HyperFrames (`embedded-captions`, `talking-head-recut`, `make-theme`, los temas o "DNA", `render-theme`…): imponen su propio diseño (fuente, colores, subtítulos abajo del todo, 1280×720) y el resultado no se parece al estilo. Tampoco cambies de técnica (subtítulos quemados con ffmpeg, otra librería, otra app) sin preguntar antes.
- La composición tiene exactamente la resolución y los fps de `cortado.mp4` (míralos con `ffprobe`). Nunca 1280×720 por defecto.
- Los subtítulos son una capa propia en HTML que lee `palabras.json` y aplica tal cual lo que dice el `estilo.md`: fuente, color, tamaño, posición, palabras por bloque y caja de énfasis.
- Cada gráfico del plan es un elemento propio de la composición, hecho con el material del usuario.
- **Si el estilo es del Estilo Maestria**, parte de su motor (`estilos/Estilo Maestria/motores/`) y de sus herramientas (`estilos/Estilo Maestria/herramientas/`): ahí está cómo se hizo de verdad. Cópialo a la carpeta del vídeo antes de tocarlo.

## Flujo (en este orden)

1. **Comprueba los requisitos:** `bash ~/.config/crear-videos/py "$S/comprobar_edicion.py"`. Si falta algo, remite a `INSTALAR.md`.

2. **Pregunta antes de empezar, todo en un solo mensaje:**
   - el vídeo a editar y el `estilo.md` (enséñale los estilos que hay: los del equipo y los suyos);
   - el guion, si lo tiene (si lo hay, el texto de los subtítulos será el suyo, palabra por palabra; si no, sale de la transcripción);
   - la música (archivo, o una del stock) y si se recorta o va entera;
   - la palabra del CTA, las marcas cuyo logo debe salir y la moneda si se habla de dinero;
   - si el `estilo.md` no fija la tipografía, propón una y pregunta.

3. **Carpeta del vídeo:** `~/crear-videos/mis-videos/<nombre del vídeo>/`. Ahí va todo: trabajo, proyecto de HyperFrames y pasadas.

4. **Inventario de recursos:** busca los sonidos, músicas, animaciones y logos del stock (`${CLAUDE_PLUGIN_ROOT}/stock/`, con `STOCK.md`) y de la carpeta del vídeo, con su duración. No des nada por inexistente sin buscarlo. Si faltan logos, pide al usuario que los descargue y te diga dónde los dejó. Mira cada logo antes de usarlo.

5. **Corta los silencios:** `bash ~/.config/crear-videos/py "$S/cortar_silencios.py" --video VIDEO --salida CARPETA/trabajo`. Quita las pausas de más de 0,3 s dejando 0,05 s a cada lado. Deja `cortado.mp4` (el vídeo con el que se trabaja a partir de aquí), `voz.wav` y `cortes.json`. Dile cuánto duraba y cuánto dura.

6. **Tiempos por palabra:** `bash ~/.config/crear-videos/py "$S/tiempos.py" --trabajo CARPETA/trabajo [--guion GUION.txt]`. Detecta solo si el vídeo está en español o en inglés y deja `palabras.json`. Si hay guion, muestra dónde el audio no coincide con él y **pregunta qué se dice de verdad**. No lo rellenes tú.

7. **Plan de escenas:** una tabla con inicio, duración, tipo (persona a cámara o gráfico), lo que se dice y lo que se ve. Sigue el `estilo.md`. Cada corte va anclado a una palabra. **Enséñale el plan y espera su aprobación.**

   **Material:** junto al plan, haz la lista de lo que necesita cada escena de gráfico: qué captura, logo, imagen o clip (por ejemplo «captura del Administrador de anuncios de Meta», «logo de WhatsApp», «clip de una persona mirando el móvil»). Pídeselo al usuario y dile que lo deje en `<carpeta del vídeo>/material/`. Si te pasa direcciones de páginas web públicas, puedes capturarlas tú; nunca páginas donde haga falta su sesión. Si el estilo se apoya en capturas o B-roll y no hay material, **avísale antes de seguir**: el vídeo solo llevará subtítulos, textos y formas animadas y no se parecerá del todo a la referencia. Que decida él.

8. **Primeros 10 segundos:** constrúyelos con HyperFrames (lee antes su skill `/hyperframes:hyperframes`), con subtítulos, música y efectos. Renderízalos y pide feedback. **No edites el vídeo completo hasta que el usuario acepte estos 10 segundos.**

9. **Vídeo completo:** el resto, con el mismo criterio. Cada gráfico ilustra lo que se dice en ese momento, y cada elemento aparece con su palabra.

10. **Música bajo la voz:** instala `@hyperframes/core` en el proyecto, con la misma versión que el plugin, y aplica el *carve* de HyperFrames para que la música baje sola cuando se habla.

11. **Verifica antes de entregar:**
    - `check` de HyperFrames sin errores.
    - Fotos 0,1 s después de cada palabra clave: la animación tiene que verse ya.
    - Subtítulos **debajo de la barbilla**: saca un fotograma de cada plano a cámara con una rejilla horizontal cada 50 px, mira en qué línea queda la barbilla (con el zoom aplicado) y empieza los subtítulos unos 45 px por debajo.
    - Todo dentro de la zona segura.

12. **Render final:** renderiza la composición con la voz de `cortado.mp4`, la música y los efectos. **El vídeo se entrega tal cual sale de HyperFrames: no hay paso de mezcla** ni se normaliza el volumen. Nómbralo `"<título> - pasada N.mp4"`.

13. **Entrega la pasada** y cuéntale, por este orden:
    - qué salió mal;
    - qué no se comprobó;
    - qué mejorarías;
    - tu puntuación.

14. **Rondas de cambios:** aplica solo lo que pida, verifica y entrega la pasada siguiente. Cuando el usuario apruebe el vídeo, ofrécele actualizar el `estilo.md` con lo que se decidió (solo si es suyo, en `mis-estilos/`).
    - **Antes de tocar nada, decide si es un cambio pequeño** (unir piezas, poner una intro u outro, cambiar un tramo, ajustar el volumen). Si lo es, hazlo con la operación mínima y **sin codificaciones innecesarias**:
      - Unir vídeos con el mismo formato: comprueba con `ffprobe` que coinciden códec, resolución, fps, formato de píxel y audio, y únelos con `ffmpeg -f concat -safe 0 -i lista.txt -c copy salida.mp4` (tarda segundos).
      - Cambiar solo el sonido: `-c:v copy` y recodifica solo el audio.
      - Cambiar un tramo: renderiza solo ese tramo y móntalo sobre la pasada anterior; nunca vuelvas a renderizar el vídeo entero.
      - Recodifica todo solo si los formatos no coinciden, y avisa antes de por qué.
    - Después de unir, comprueba: duración (suma de las partes), sincronía audio/vídeo con `ffprobe`, que 2–3 s alrededor de la unión se decodifican sin errores y un fotograma justo después del corte.

## Lo que no hay que hacer (pasó en vídeos reales)

- Fiarte de los tiempos de Whisper en frases largas o repartir a ojo palabras que salen pegadas: las animaciones llegan tarde. Usa `tiempos.py`.
- Poner los subtítulos en el centro sobre la cara.
- Usar en las escenas nombres de clase que ya existen en la página principal (`.word`, `.av`…): chocan y ocultan elementos.
- Buscar una palabra repetida sin distinguir mayúsculas («yo» y «YO»).
- Normalizar el volumen con `loudnorm` o llevarlo a −16 LUFS: comprime y deshace los volúmenes del render.
- Usar los flujos o temas ya hechos de HyperFrames (`embedded-captions`, `talking-head-recut`): el vídeo salió en 1280×720, con su fuente y sus colores, y sin parecerse en nada al estilo. Cinco pasadas perdidas.
- Renderizar el vídeo entero antes de que el usuario apruebe el plan y los primeros 10 segundos.
- Seguir sin material cuando el estilo vive de capturas y B-roll, sin avisar antes al usuario.
- Recodificar vídeos enteros para un cambio pequeño: para poner una intro de 3 s delante de 4 lecciones se lanzó un concat con `libx264` sobre ~350 s de vídeo; con `-c copy` tardó segundos y quedó igual.
