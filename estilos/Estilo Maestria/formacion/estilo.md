# estilo-maestria.md — Estilo «MaestrIA» (v1)

**Estado:** aprobado en varias lecciones y módulos del curso.
**Vídeos que lo usaron:** LM 1, Lección 1–5 y Módulo 1–6. Son vídeos horizontales a cámara de 35 a 100 s para la formación MaestrIA / Código Maestría.
**Dónde está el código:** el motor está en `../motores/motor-formacion/` y las herramientas en `../herramientas/` (corte de silencios, Whisper, brillo, auditoría, render y base común de módulos).
**Estilos de los que viene:** `estilobasico.md` y `estilo motions.md`. Este estilo **funde los dos** [DECISIÓN] y añade las **pantallas de texto azules** [DECISIÓN].

Cómo se obtuvo cada dato:
- **[CÓDIGO]**: valor exacto que había en `build.py`, `scenes.py`, `textcards.py`, `scenes_b.py`, `motions.py` o `fxlib.py`.
- **[MEDIDO]**: sale de los MP4 entregados, medido con ffmpeg.
- **[DECISIÓN]**: lo pidió o lo aprobó el presentador.

---

## 0. El estilo en 12 reglas
1. **Horizontal 1920×1080 a 30 fps, vídeo entero, sin música** [DECISIÓN].
2. **La cara del presentador se ve siempre en el primer segundo.** Ninguna pantalla completa empieza antes de 1,0 s [DECISIÓN].
3. **Silencios cortados:** las pausas de más de 0,3 s se quitan, dejando 0,05 s a cada lado y un fundido de 0,01 s en cada unión.
4. **Brillo medio, +37 %, solo en la persona.** El fondo azul se queda igual [DECISIÓN].
5. **Zoom alterno 100 % / 116 %** con un empuje lento de +4 % dentro de cada plano. **Todas las uniones** del corte de silencios que quedan fuera de un gráfico cambian de zoom, para que no se vea el tirón [DECISIÓN].
6. **Tres tipos de pantalla:** (a) el presentador a cámara con **motions blancos laterales**; (b) **gráficos a pantalla completa sobre fondo claro** (tarjetas, temario, comparativas); (c) **pantallas de texto AZULES con letra blanca** para las frases clave [DECISIÓN].
7. Cada gráfico **ilustra literalmente lo que se dice**, y cada elemento entra **0,10 s antes de su palabra**. Las escenas entran **0,06 s (2 fotogramas) antes** de la palabra que las dispara.
8. **Subtítulos por trozos**, palabra a palabra, con **una palabra destacada** en mayúsculas grandes. Sobre las pantallas azules **no hay subtítulos**, porque el texto ya está en grande.
9. **Sonidos al ritmo del movimiento:** cada entrada lleva su whoosh, pop, click, ding o impacto [DECISIÓN].
10. **Delante de cada módulo o lección va la intro «solo logo» (3 s)**, pegada con `concat -c copy` sin recodificar [DECISIÓN].
11. **Volumen final −16 LUFS con ganancia fija + limitador.** Nunca `loudnorm`.
12. **Cierre:** pantalla azul con «vamos allá / vamos a ello» y el logo MaestrIA, que se ve en cuanto entra la pantalla.

---

## 1. Formato y entrega [MEDIDO]
- 1920×1080, 30 fps, H.264 (`libx264 -crf 16`), audio AAC a 256 kbps y 48 kHz.
- Sonoridad: entre −16,1 y −16,5 LUFS en los 6 módulos. Desfase audio/vídeo ≤ 0,02 s.
- Nombres: `<Nombre> - sin intro.mp4` y `<Nombre> - pasada N.mp4` (con intro), en `~/crear-videos/mis-videos/<Nombre>/`.

## 2. Flujo de trabajo (en este orden)
1. **Preparar:** `bash ~/.config/crear-videos/py ../herramientas/preparar.py <vídeo> <carpeta>`. Corta los silencios (`cortar.py`), transcribe con Whisper y crea `proyecto/assets/aroll.mp4` (con brillo) y `voz.m4a`.
   - Whisper: `whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-small.bin -l es -ojf -dtw small -nfa`.
2. **Guion final** (`trabajo/guion_final.txt`): lo que **dice el audio**, con la ortografía del guion del presentador [DECISIÓN]. Las diferencias se apuntan para el informe final.
3. **Tiempos:** `../herramientas/palabras.py <trabajo>` crea `palabras.json`. Usa el tiempo DTW de Whisper − 0,14 s, y tras cada corte el *offset*.
4. **Subtítulos:** `trabajo/spec.txt` (ver §5).
5. **Escenas, pantallas azules y motions:** se copia la base de `../herramientas/base_modulo/` y se añade al final lo propio del vídeo.
6. **Comprobar:** `bash ~/.config/crear-videos/py build.py` → `auditar.py` (sin tirones) → `npx --yes hyperframes@0.8.114 lint` (0 errores) → `snapshot --at … --no-end --describe false --timeout 20000` y revisar los fotogramas.
7. **Entregar:** `bash ~/.config/crear-videos/py ../herramientas/entregar.py <carpeta> <nombre> [--intro INTRO.mp4]`. Hace el render (uno a la vez, con candado, para ordenadores de 8 GB), añade la intro sin recodificar y audita el MP4. El sonido sale tal cual del render: no se ajusta el volumen.

## 3. Color [CÓDIGO + DECISIÓN]
- Filtro (`../herramientas/color.fc.txt`): `curves=all='0/0 0.35/0.52 1/1'` aplicado solo donde **no** está el fondo azul. La máscara se hace con `chromakey=color=0x3468D8:similarity=0.08:blend=0.08`.
- Paleta de los gráficos: fondo `#F5F6F8`, tinta `#101010`, azul `#0050E0`, rojo `#E5484D` (tachados) y azul oscuro `#14256B` (texto de pastilla).
- Azul de las pantallas de texto: `radial-gradient(ellipse at 50% 38%, #2f74ff 0%, #1157df 45%, #003fab 100%)`.

## 4. Tipografía [CÓDIGO]
- **Hanken Grotesk 700** para subtítulos, títulos y palabras gigantes (también 500).
- **Spline Sans Mono 500** para etiquetas en MAYÚSCULAS con mucho espaciado (14 px de *letter-spacing* en las pantallas azules).
- **Newsreader itálica 500** para acentos en serif azul (poco uso).
- **Didot Bold** solo en la intro, junto al logo [DECISIÓN].

## 5. Subtítulos [CÓDIGO]
- Caja: `left 260 / right 260 / top 800 px`.
- Palabra normal: 64 px, interlineado 1,2, separación entre palabras 18 px.
- Palabra **destacada**: ocupa su propia línea, en MAYÚSCULAS, 112 px, `letter-spacing −3 px`.
- Colores: sobre la persona, blanco con sombra `0 4px 24px rgba(0,0,0,.55)`; sobre los gráficos claros, tinta `#101010` con la destacada en azul `#0050E0`, sin sombra; sobre las pantallas azules, ocultos.
- Animación:
  - palabra normal: entra con desenfoque de 10 px a 0, `y 14 → 0`, en 0,12 s;
  - destacada: entra con desenfoque de 14 px, `scale .7 → 1` y `back.out(2.5)`, en 0,16 s;
  - el trozo se apaga en 2 fotogramas justo antes del siguiente.
- `spec.txt`: trozos separados por `|` y la destacada entre `*asteriscos*`, que **solo puede ser una palabra**. Las palabras tienen que coincidir una a una con `palabras.json`.
- Sombra inferior sobre el A-roll: degradado negro al 38 % en los 380 px de abajo.

## 6. Pantallas de texto azules [CÓDIGO] (`textcards.card`)
- Estructura: etiqueta mono (46 px, 80 % de blanco) encima y **palabra gigante blanca** debajo, centradas. Sombra `0 10px 50px rgba(0,20,80,.35)`.
- **Tamaño automático:** `min(220, 1650 / (0,64 × letras))` px, en una sola línea de ~1650 px como máximo.
- Variantes:
  - `letters=True`: letra a letra, con desenfoque y `stagger .035`;
  - `ul=True`: línea blanca que se dibuja debajo;
  - `strike=t`: **tachado rojo** + temblor + texto al 45 %, para negar algo.
- Entrada de la palabra gigante: `scale 1.7 → 1` con desenfoque de 16 px y `back.out(1.8)`, en 0,28 s. Durante toda la pantalla, empuje lento a `scale 1.04`.
- La palabra grande **debe salir pronto**. Si sale en el último segundo, no da tiempo a leerla.
- Duración habitual: entre 1,1 y 4 s. En LM 1, «¿Lo mejor?» y «¿Y qué ocurre?» duran **1,5 s** [DECISIÓN].
- Cierre: añade el logo blanco (170 px), que entra girando (`rotationY −180 → 0`) a los 0,3 s. Sonidos: whoosh-morph al entrar y chime a los +0,4 s.

## 7. Gráficos sobre fondo claro [CÓDIGO] (`scenes.py` + `scenes_b.py`)
- Fondo `#F5F6F8`, cuadrícula de 72 px (líneas al 4,5 %) y 2 brillos azules difuminados en las esquinas.
- Tarjetas blancas con radio de 36 px y sombra `0 30px 80px rgba(16,24,40,.14)`. Tarjeta «caliente»: degradado azul con texto blanco.
- Pastilla de título (`.tag`): mono de 44 px, borde azul de 4 px, en dos tonos (`<b>` en azul).
- Todo el contenido va **por encima de y = 770**, porque debajo van los subtítulos.
- Entrada de escena (`SCENE_IN`): `scale 1.12 → 1`, desenfoque de 18 px a 0, en 0,22 s.
- Piezas reutilizables:
  - `cards(tag, items)`: fila de tarjetas con icono que entran con su palabra y se marcan ✓.
  - `post(done, new, title, sub, head)`: **temario «En este módulo»**, una tarjeta con filas que se marcan ✓. **Su altura depende del número de filas** (190 + 84 por fila). Si el temario es largo, se parte en dos con la cara del presentador en medio y la segunda parte repite como hechas las filas clave.
  - `rule(num, icon, title, chips, kind)`: «0N» gigante + tarjeta con icono, para series de REGLA / PRINCIPIO / TAREA.
  - Comparativas a medida: antes ↔ hoy, pobres ↔ claras, de ↔ a.
- **No encadenar más de ~5 s de pantallas completas seguidas.** Hay que volver a la cara del presentador.

## 8. Motions blancos laterales [CÓDIGO] (`fxlib.py` + `motions.py`)
- Posición: izquierda en `cx 300` y derecha en `cx 1620`, a `y ≈ 360–400`, siempre por encima de los subtítulos. Se alterna el lado.
- Envoltorio común (`box`): halo, anillo de luz que se expande y entrada `scale .35 → 1` con `back.out(1.7)`. La salida dura 0,3 s.
- Piezas:
  - `big`: número o texto gigante con temblor y destellos.
  - `logo`: M de MaestrIA girando en 3D.
  - `brand`: logo de una marca en una baldosa blanca, por ejemplo Claude con `stock completo/logos/Claude_AI_symbol.svg`.
  - `chip`: chip «AI» que se dibuja.
  - `checklist`: 3 filas que se marcan ✓ con su palabra. Textos cortos, de 12 caracteres como máximo.
  - `people`: avatares + etiqueta.
  - `coin`: moneda $ 3D. Con `num=False` no sale ninguna cifra inventada.
  - Otras: `gears`, `shield`, `speed`, `clock`, `donut`, `counter`, `rain`, `flag`, `install`.
- Nada decorativo sin sentido: cada motion va ligado a una palabra.

## 9. Sonido [CÓDIGO]
Efectos en `assets/sfx`:

| Efecto | Volumen | Uso |
|---|---|---|
| `whoosh.m4a` | 0,24 | Entrada de pantalla |
| `swish.mp3` | 0,24 | Entrada de gráfico claro |
| `whoosh-slide.mp3` | 0,20–0,23 | Deslizamiento |
| `whoosh-morph.mp3` | 0,20–0,24 | Logo o cierre |
| `pop.mp3` | 0,28 | Aparición |
| `click.mp3` | 0,22 | Fila o tarjeta |
| `ding.m4a` | 0,15 | Palabra clave |
| `impacto.m4a` | 0,08 | Número gigante o tachado |
| `type-short.mp3` | 0,24 | Chip |
| `sparkle-twinkle.mp3` | 0,05 | Letra a letra |
| `chime.mp3` | 0,12–0,14 | Logo |

- Cada efecto va a la primera pista libre (pistas 20 en adelante), para que no se pisen.
- Volumen final: ganancia = −16 − I(LUFS) y luego `alimiter=limit=0.79:attack=5:release=50:level=false`, AAC a 256k y 48 kHz.

## 10. Intro «solo logo» (3 s) [DECISIÓN]
- Proyecto: `Intro Codigo Maestria/proyecto-logo/`, render en `renders/solo-logo.mp4`.
- Animación: fondo azul y M blanca 3D que da una vuelta (`rotationY −360 → 0` en 0,85 s, `power3.out`). Impacto a 0,8 s, chime a 1,1 s y sparkle a 1,2 s.
- Para pegarla: se le sube el volumen (`volume=8dB` + el mismo alimiter, AAC 48 kHz) y se une con `ffmpeg -f concat -safe 0 -i lista.txt -c copy`. **Nunca se recodifica el vídeo** [DECISIÓN].
- La versión con «AESTRIA» en Didot Bold junto a la M está en `Intro Codigo Maestria/proyecto/`.

## 11. Errores que ya pasaron (no repetir)
- **Tirones** entre motions: venían de uniones del corte sin tapar. Ahora el inicio de cada escena se adelanta, o su final se alarga, hasta la unión que tenga a ≤ 0,4 s (`snaps`), y las escenas seguidas se recortan para que no se solapen.
- **`wt(palabra, n)` busca la palabra EXACTA, con su puntuación:** «Claude.» ≠ «Claude», «Esto» ≠ «esto». Hay que contar bien la n o usar `wa(palabra, desde_segundo)`.
- Las palabras grandes de las pantallas azules salían tarde y solo se leían 0,5 s.
- Un temario de altura fija quedaba medio vacío con 2 filas.
- Hubo textos que se salían de la pantalla. Ahora el tamaño es automático, pero hay que revisarlo en el snapshot.
- Se recodificó un concat de 350 s para añadir una intro de 3 s. Con `-c copy` tarda segundos.
- Se lanzaron 4 renders en paralelo en un Mac de 8 GB. Hay que hacerlos **uno a uno**.
- **Guardar los proyectos:** al borrar las carpetas de los vídeos se perdió el motor una vez. Antes de borrar, hay que conservar `proyecto/*.py`, `assets/fonts`, `assets/sfx` y `assets/logos` de un vídeo de referencia.

## 12. Motor
El motor se reconstruyó y está en `../motores/motor-formacion/` (`build.py`, `scenes.py`, `fxlib.py`, `textcards_base.py`…). Las piezas comunes siguen en `../herramientas/base_modulo/`.


---
**Reglas generales aprendidas en vídeos reales:** ver [§15 de la ficha de YouTube](../youtube/estilo.md#15-reglas-aprendidas-en-vídeos-reales-valen-para-todo-el-estilo-maestria).
