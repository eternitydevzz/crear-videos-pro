# Estilo Albert — interpretación del estilo de edición (motions)

> **Nota del repo:** esta ficha se hizo con el reel descargado y sus archivos de trabajo (`video.mp4`, `Frames/`, `cortes.txt`, `info.txt`, `audio/`, `transcripcion.md` y `ventanas/`). En el repo solo están la ficha y los **mosaicos**: esos archivos se citan como fuente de los datos, pero no se incluyen. Para tenerlos, pasa el link del reel por `/crear-videos-pro:crear-estilo-videos`.

- **Cuenta analizada:** @albert.olgaard (Instagram)
- **Material:** 6 reels, de 30,5 a 38,75 s (207 s en total). Carpeta: `albert-reels/`
- **Fecha del análisis:** 3-10-2026
- **No incluido:** el 7.º link (`Dd4ABsKiqu9`). No se pudo descargar porque Instagram lo marca con restricción de edad.

---

## 0. Cómo leer este documento

Cada afirmación lleva una etiqueta, para que se vea qué es seguro y qué no:

| Etiqueta | Significa |
|---|---|
| **[MEDIDO]** | Es un número sacado de los frames con código (ffmpeg + numpy). |
| **[VISTO]** | Lo vi yo en las hojas de contacto, frame por frame, pero no lo medí con código. |
| **[HIPÓTESIS]** | Es una interpretación mía. No la he comprobado. |

---

## 1. El estilo en 10 líneas

1. Son reels verticales (720×1280) de **noticias o tutoriales de IA**. El orden es siempre el mismo: gancho, explicación, y cierre pidiendo que comenten una palabra.
2. Todo el video usa **dos capas que se alternan**. La capa **Pantalla** muestra una tarjeta flotante sobre fondo beige, con subtítulo grande debajo. La capa **Cara** muestra la tarjeta arriba y a Albert hablando abajo.
3. Las dos capas **se alternan sin repetirse**. Cada bloque dura **≈ 3,8 s de media** (entre 1 y 8 s). Hay un cambio de capa cada **4,3 s**.
4. **Los 6 videos empiezan en la capa Pantalla**, sin cara, y los 6 **terminan en la capa Cara** con la tarjeta de comentarios.
5. La cara aparece por primera vez entre los **2,5 y los 8 s** (mediana: 4,6 s).
6. Cada cosa que Albert dice **tiene su dibujo en pantalla en ese mismo momento**: un logo, un número que sube, un meme, una lista que se rellena o texto que se teclea.
7. La capa Pantalla usa un subtítulo **palabra por palabra**, de 1 a 3 palabras a la vez. Palabras clave en cursiva con serifa, y en verde (bueno) o rojo (malo).
8. La capa Cara usa un subtítulo **en frases cortas**, en mayúsculas, con letra tipo máquina de escribir, blanco sobre caja negra. Va justo en la costura entre tarjeta y cara.
9. Los logos de las marcas se tratan como **personajes**. Se pelean, se disparan, se aplastan y "mueren" (gag "X mató a Y"). Aparece en 4 de los 6 videos.
10. Los números nunca aparecen quietos: **cuentan, suben o bajan** hasta quedarse en una caja verde o roja.

---

## 2. Qué revisé y con qué límites

**Qué revisé [MEDIDO]:**
- Los **829 frames** de los 6 videos (139 + 126 + 151 + 122 + 136 + 155), a **4 frames por segundo**. Cada uno lo vi dentro de una hoja de contacto de 8 frames (106 hojas), con el número de frame y el segundo escritos encima.
- Medí con código: el color del fondo, dónde empieza la cara, el tamaño de las tarjetas, cuánto dura cada bloque y con qué frecuencia cambian los subtítulos.

**Límites que tengo que decirte:**
- A 4 frames por segundo **no se ven las animaciones de menos de 0,25 s**: la curva exacta de cada rebote, cuánto tarda una tarjeta en entrar o cómo es el corte justo de una transición. Esas partes las describo por su resultado, no por su curva. Hace falta analizar las transiciones a 30 fps (todavía no lo hice).
- En las hojas cada frame se veía al 41 % de su tamaño. **El texto pequeño de las pantallas (menús, tablas) lo leí solo cuando se podía.** Los subtítulos grandes y las cifras sí se leen bien.
- **No analicé el audio ni los efectos de sonido.** Están separados en `audio/` dentro de cada carpeta, pero no los escuché para este documento.
- Mi detección automática de capas confunde las explosiones a pantalla completa con "cara" (en V2 y V6). Lo corregí a mano en las cifras de este documento.
- El conteo de cambios de subtítulo de la capa Cara **no es fiable**: la zona que medí incluye la cara en movimiento. Para esa capa uso lo que vi, no el número.

---

## 3. Los 6 videos de un vistazo

| # | Código | Seg. | Tema | 1.ª cara | Cambios de capa | % con cara | Gancho | Palabra del CTA |
|---|---|---|---|---|---|---|---|---|
| V1 | Dd9O9UpCRNs | 34,75 | Higgsfield dentro de ChatGPT (`/tinder`, `/linkedin`, `/pov`, `/360`, `/ugc`) | 4,25 s | 7 | 47 % | Demo directa: teclea `/tinder` en el primer segundo | `/video` |
| V2 | Dd_w892CW-m | 31,5 | "dots" de OpenAI frente a "Muse" de Meta | 4,75 s | 7 | ≈40 % | Un avión con el logo de ChatGPT bombardea a "Muse" | `DOTS` |
| V3 | Dd5_N6EiY4h | 37,75 | GPT-6.1 Sol y dots frente a Opus 5.5 | 2,5 s | 11 | 56 % | El logo de ChatGPT hace un mate de baloncesto sobre el de Claude | `DOTS` |
| V4 | Dd1dN_EgWvk | 30,5 | Runable reemplaza 10 herramientas | 7,25 s | 9 | 45 % | 10 logos de apps caen y aparece un emoji 😬 "ripped off" | `STACK` |
| V5 | DduBEWLCIy4 | 34,0 | Higgsfield: 1.000 millones de run rate y 100 % de cashback en la API | 8,0 s | 7 | 42 % | Meme de Drake ("Nah") y meme del mago ("crazy") | `API` |
| V6 | DdocHKLq7i0 | 38,75 | Archivo CLAUDE.md para no gastar el límite de uso con Opus 5.5 | 4,5 s | 7 | ≈59 % | Caras de Dario Amodei y Sam Altman, un lanzacohetes y una explosión | `SAVE` |

**[MEDIDO]:** 48 cambios de capa en 207 s = uno cada 4,3 s. Los bloques de Pantalla duran **3,9 s** de media (mediana 4,0 s) y los de Cara **3,7 s** (mediana 3,25 s). Son 27 bloques de cada tipo.
Los efectos a pantalla completa de V2, V3 y V6 los conté dentro del bloque Pantalla (son parte del gancho).

**Palabra-gancho "mató / murió":** aparece en 4 de los 6 videos, en la transcripción (V2 "killed Muse", V3 "dunked on", V4 "dead" ×4, V6 "killed Astra"). V1 y V5 no la usan.

---

## 4. El patrón central: dos capas que se alternan

### 4.1 Mapa de capas de cada video

`P` = capa Pantalla · `C` = capa Cara · `*` = efecto a pantalla completa. **Cada carácter es 0,25 s** (un frame).

```
V1  PPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCPPPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCCCCCPPPPPPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCCCPPPPPPPPPPPPPPPPPCCCCCCCCCCC
V2  PPPPPP****PPPPPPPPPCCCCCCCCCCCCCCCPPPPPPPPPPPPCCCCPPPPPPPPPPPPPCCCCCCCCCCCCCPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCC
V3  PPPPPPPPP*CCCCCCCCCCCCCCCCCCCCCCPPPPPPPPPCCCCCCCCCCCCCPPPPPPPPPPCCCCCCCPPPPPPPPPCCCCCCCCCCCCPPPPPPPPPPPCCCCCCCCCCCCPPPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCC
V4  PPPPPPPPPPPPPPPPPPPPPPPPPPPPPCCCCCCPPPPPPPCCCCCCCCCCPPPPPCCCCCCCCCCCPPPPPPPPPCCCCCCCCCCCCCCCCCPPPPPPPPPPPPPPPPPCCCCCCCCCCC
V5  PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPCCCCCCCCCCCCPPPPPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCPPPPPPPPPPPCCCCCCCCCCCCCCCPPPPPPPPPPPPPPPPCCCCCCCCCCCCC
V6  PPPP***PPPPPPPPPPPCCCCCCCCCCCPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCCPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCPPPPPPPPPPPPPPPPCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
```

Todas las líneas empiezan en `P` y terminan en `C`. En cada una se ve cómo las dos capas se turnan.

### 4.2 Capa A — "Pantalla" (la tarjeta manda)

**[MEDIDO] en 2 frames de V1 (a 720×1280):**

| Elemento | Medida |
|---|---|
| Fondo | Beige liso **≈ #F0EFEA** (240,239,234 en 5 de 6 videos; 241,240,235 en V4) |
| Tarjeta | Blanca, con esquinas redondeadas y sombra suave. Empieza a **y ≈ 115–133 px** (≈ 10 % desde arriba) |
| Alto de la tarjeta | Variable: hasta **≈ 580–695 px** si es imagen vertical |
| Ancho de la tarjeta | **≈ 71–76 %** del ancho si es imagen vertical (513–544 px); más ancha si es una ventana de escritorio |
| Subtítulo | Centrado en **y ≈ 773 px (≈ 60 % de la altura)**. Ese valor no cambia aunque cambie el tamaño de la tarjeta |
| Zona de abajo | Vacía del todo desde **y ≈ 820 hasta 1280**: queda libre el último **35 %** del cuadro |

**[HIPÓTESIS]** El 35 % vacío de abajo sirve para dejar sitio a la interfaz de Instagram (descripción, botones). No lo he comprobado.

### 4.3 Capa B — "Cara" (Albert + tarjeta arriba)

**[MEDIDO] en 4 videos distintos (V1, V4, V5, V6):**

| Elemento | Medida |
|---|---|
| Costura entre la parte de arriba y la cara | **y = 571 px**, exacto en los 4. La cara ocupa de 572 a 1280: **≈ 55 % del alto** |
| Tarjeta de arriba | Más ancha que en la capa A: **≈ 91 %** del ancho (x de 32 a 690 en V4) y ≈ 400 px de alto |
| Subtítulo | **Caja negra centrada en la costura** (y ≈ 546–597, unos 50 px de alto) |

**Cómo está grabado Albert [VISTO]:**
- **V1, V2, V3, V4:** selfie con la mano, micrófono de peluche en la otra mano, cuarto claro con cortinas.
- **V5 y V6:** sentado en una silla de escritorio, micrófono de pie delante, pizarra blanca detrás. El color de V6 es algo más oscuro y frío.
- Dentro de un mismo bloque de cara no vi saltos de plano, solo el movimiento normal de hablar.

### 4.4 Cuándo usa cada capa

**[VISTO + HIPÓTESIS]:** es lo que parece, no una regla que él haya dicho.

- **Capa Pantalla:** cuando la tarjeta **enseña** algo (un resultado generado, el momento de teclear, un logo, una lista).
- **Capa Cara:** cuando hay **reacción o juicio** ("WHY IS THIS SMART", "HOW THE FUCK IS THAT EVEN POSSIBLE"), cuando **explica un paso** o cuando **pide el comentario**.
- La tarjeta de arriba **no desaparece** en la capa Cara: la información sigue en pantalla mientras él habla.
- **Excepción única [VISTO]:** en V2, de 7,75 a 8,5 s, la cara ocupa **toda la pantalla** (sin tarjeta) para decir "BUT HERE'S WHAT YOU NEED TO KNOW". Es el único momento así en los 6 videos.

### 4.5 Ritmo [MEDIDO]

- **Primera cara:** 2,5 · 4,25 · 4,5 · 4,75 · 7,25 · 8,0 s. Media 5,2 s, mediana 4,6 s.
- **Bloque más corto:** 1,0 s (V2, 11,5 a 12,5 s: el emoji 🤔 "WHY IS THIS SMART"). **Más largos:** 8 s, en tres sitios: V2 en Pantalla (19 a 27 s), V5 en Pantalla (0 a 8 s) y V6 en Cara (19,25 a 27,25 s).
- **Cierre:** en los 6 videos el último bloque es una capa Cara con la tarjeta de comentarios. El video termina **justo cuando el corazón se pone rojo**. No hay despedida.

---

## 5. Los subtítulos: dos sistemas

### 5.1 Subtítulo "palabra por palabra" (capa Pantalla)

- **Tamaño del grupo [VISTO]:** 1 a 3 palabras a la vez. Se añaden palabras ("it'll" → "it'll generate"), y luego cambia el grupo ("a" → "a Tinder" → "profile").
- **Frecuencia [MEDIDO]:** en la zona del subtítulo, que está sobre fondo liso y por eso la medida es limpia, **el texto cambia en el 71 % de los pasos de 0,25 s**. Es decir, un cambio de palabra cada **≈ 0,35 s**.
- **Cómo aparecen [VISTO, interpretación consistente]:** cada grupo parece estar colocado **centrado con su ancho final**, y las palabras van apareciendo en su sitio. Por eso, la primera palabra de un grupo sale a la izquierda del centro ("the" a ≈ 32 % del ancho) y no se mueve al llegar la siguiente.
- **Énfasis por tamaño [VISTO]:** las palabras clave salen **más grandes** (≈ +25 %): "smarter", "Meta", "computer", "UGC".
- **Color [MEDIDO en frames sueltos]:**

| Uso | Color medido | Ejemplos |
|---|---|---|
| Texto normal | **≈ #222121** (34,33,33), sans en negrita | casi todo |
| Afirmación positiva / clave | **≈ #299046** (verde) | "profile picture", "ready to go", "one-fifth", "cheaper", "billion-dollar", "100%", "sub-agent" |
| Algo negativo | **≈ #E9483A** (rojo) | "usage limit" (V6) |
| Nombre de producto, comando o cifra | **Cursiva con serifa, negrita** | `/tinder`, ChatGPT, Higgsfield, Opus, dots, Fable, 200, 5 |

- **Detalle de marca [VISTO]:** "Opus 5.5" se escribe con "Opus" en cursiva con serifa y "5.5" en sans normal.
- **Tipografías [HIPÓTESIS]:** la sans negrita parece Helvetica o Inter, y la cursiva con serifa parece una Times en negrita cursiva. No lo he comprobado con el archivo original.

### 5.2 Subtítulo "frase corta" (capa Cara)

- **Forma [VISTO]:** letra tipo máquina de escribir, **MAYÚSCULAS**, blanca sobre una caja negra de esquinas redondeadas (interior **≈ #161712**, medido). Mide ≈ 50 px de alto y va **centrada en la costura** (y ≈ 571).
- **Contenido [VISTO]:** 2 a 5 palabras por frase. Cambia cada **≈ 0,5 a 1,5 s**. Ejemplos de V1: "IF YOU WRITE /LINKEDIN" (1,5 s), "IT'LL CREATE A", "PROFESSIONAL IMAGE", "FOR YOUR LINKEDIN PROFILE".
- **Palabrotas [VISTO], sin criterio fijo:** V2 pone "SH*T" y V5 "F***" censurados, pero V3 pone "HOW THE FUCK" **sin censurar**.
- **En el único plano de cara completa (V2):** la caja baja y se queda sobre el micrófono (≈ 77 % de la altura).

---

## 6. La tarjeta

### 6.1 Cómo es

- Siempre es un **rectángulo blanco con esquinas redondeadas y una sombra suave** [VISTO].
- Hay variantes: crema (la tarjeta de Anthropic en V3), negra (V2, tarjeta "dots"), con **degradado naranja-rosa y textura de puntos** (V4, secuencia de "Runable") y con **marco de ventana de Mac** con tres puntos de colores (V5, V6, V3).
- Su **ancho cambia según el contenido** [MEDIDO en 3 frames + VISTO]. Una imagen vertical queda más estrecha (≈ 71–76 %). Una ventana de escritorio se estira (≈ 90 % o más).
- El contenido cambia **dentro de la misma tarjeta** (se disuelve y entra el siguiente) o **entra una tarjeta nueva** que empuja o tapa a la anterior (V3: "Introducing dots" y debajo la de "GPT-6.1 Sol").

### 6.2 Qué entra en la tarjeta (los 6 videos juntos) [VISTO]

| Tipo | Ejemplos |
|---|---|
| Maqueta de pantalla (móvil o escritorio) | ChatGPT escribiendo `/tinder`, agente "Shiney", editor con CLAUDE.md, videollamada, Gmail, búsqueda de Google |
| Resultado generado | Foto de perfil, vídeo POV del perro, zapatilla en 360°, anuncio UGC |
| Logos tratados como personajes | ChatGPT, Claude, Meta Muse, las mascotas de dots |
| Meme | Pepe Silvia, Chris Pratt, DiCaprio señalando, DiCaprio brindando, Drake, el mago, Fry, Michael Scott, Lobo de Wall Street, Roll Safe |
| Emoji grande | 🤔 con signos de interrogación flotando, 😬 con dientes |
| Gráfico o medidor | Barras de benchmark, barra de cashback, odómetro, calendario |
| Documento o web simulada | Página de precios, tuit de OpenAI, cheque "Higgsfield Inc." |
| Cierre | Tarjeta de comentarios (en los 6) |

**Memes por video [VISTO]:** V1 y V4 ninguno · V2 uno · V3 dos · V6 tres · V5 cuatro. Emoji grande: V2, V4, V5 (y un dedo medio en V6).

---

## 7. Catálogo de motions

Cada motion lleva **dónde aparece** (video y segundo aproximado) y **cómo replicarlo en simple**. Las recetas son mis hipótesis de implementación, no medidas.

### M1 — Escritura en vivo sincronizada con la voz
- **Dónde:** V1 (comando `/tinder`, 0–2 s; `/pov`, `/360`, `/ugc`), V6 (el archivo CLAUDE.md, 15,75 a 27 s), V3 (documento "Set up dots with the new models", 33,25 a 36 s), cuadro de comentarios en los 6.
- **Qué se ve [VISTO]:** letra a letra, con cursor parpadeante. En V6 el texto se escribe al mismo ritmo que las palabras del subtítulo. En V1 salta incluso el teclado de iPhone con la tecla pulsada.
- **Receta:** texto que se revela carácter a carácter + cursor + ritmo atado a la voz.

### M2 — Zoom y recorte sobre la maqueta
- **Dónde:** V1 0–2 s (la tarjeta se acerca al teclado y al campo de texto), V5 4–5,75 s (el tuit se desplaza hacia arriba).
- **Qué se ve [VISTO]:** la tarjeta enseña solo la parte que importa. La maqueta se **desplaza o se acerca** para seguir la acción, en vez de enseñar la pantalla completa.
- **Receta:** una maqueta grande dentro de una tarjeta con recorte, y una cámara virtual que se mueve por encima.

### M3 — Dedo y cursor
- **Dónde:** círculo gris translúcido en las maquetas de móvil (V1, V2 comentarios); flecha negra en las de escritorio (V2, V4, V5, V6).
- **Receta:** un círculo gris o una flecha que se mueve a donde se hace clic, un instante antes de que cambie la pantalla.

### M4 — Lluvia de logos
- **Dónde:** V4 0–1,75 s (10 logos de apps caen uno a uno), V2 4,75 a 5,5 s (iconos que aparecen en abanico), V4 21,5 a 23,5 s (los logos orbitan y se van).
- **Qué se ve [VISTO]:** cada logo entra **ligeramente inclinado** y se asienta en una cuadrícula con su nombre debajo. Sale un logo por cada palabra o número que dice ("10 tools").
- **Receta:** entrada escalonada de cada ícono con pequeña rotación, atada al conteo hablado.

### M5 — Gag "X mató a Y" (logos que se matan)
- **Dónde:**
  - V2 0–2,25 s: un avión negro con logo ChatGPT suelta una bomba sobre el peluche "Muse from Meta".
  - V3 0–2,25 s: el logo de ChatGPT, con brazos y puños, hace un mate sobre el de Claude, que se aplasta.
  - V4 6–7 s (Calendly, con pistola de pintura), 8,75–10,25 s (Otter, aplastado), 13–14 s (Zapier, cortado con katana), 17–19 s (ChatGPT y Claude, con un cañón de confeti).
  - V6 0–1 s: Dario Amodei con un lanzacohetes contra Sam Altman.
- **Qué se ve [VISTO]:** el logo de la marca es el actor. Cada "muerte" es distinta y más exagerada que la anterior. Termina con la palabra "dead" en el subtítulo.
- **Receta:** cada marca = un personaje con su cartel debajo, y un arma o animación nueva por cada una.

### M6 — Efecto que llena la pantalla = transición
- **Dónde:** V2 1,5–2,5 s (explosión y luego telón de teatro rojo que se abre para mostrar "dots"), V3 2,25 s (el balón de baloncesto tapa todo), V6 1–1,75 s (explosión naranja y blanca).
- **Qué se ve [VISTO]:** un objeto del gag **crece hasta ocupar los 720×1280** y, al desaparecer, deja el fondo beige limpio con el nuevo contenido. Es lo único en los 6 videos que sale del marco de la tarjeta.
- **Receta:** el último frame del gag es un primer plano gigante del objeto, que se disuelve en la siguiente escena.

### M7 — Contadores y barras que se rellenan
- **Dónde:** el más usado del estilo.
  - V4 15–16 s: 19 → 1.304 → 2.731 → **3.000+** (caja verde al final).
  - V4 2,75–4 s: total de precios hasta **$216,98/month** (caja roja).
  - V5: odómetro hasta **$1.000.000.000** (2,75–3,5 s), tuit con $15.589.374 → **$20.000.000** (5–5,5 s, caja roja), medidor **$0 → $14.385 → $70.010 → $99.934 → $100.000** (20,25–21,5 s, caja verde), bolsa de cashback **$20.000.000 → $1.974.000 → $0** (23–24 s, en rojo).
  - V3 6–7,5 s: barra **20,1 → 40,0 → 56,6 → 69,3 → 71,4** (recuadro verde); barras de benchmark de 16 a 17 s.
  - V2: reloj de móvil **12:47 → 2:58 → 3:44 → 5:37 → 6:12**, con notificaciones que se apilan.
- **Qué se ve [VISTO]:** el número **no entra quieto**. Cuenta o baja, y al llegar se queda en una caja verde (logro) o roja (peligro). Si algo se acaba o se prohíbe, el número baja a cero y se pone rojo.

### M8 — Resaltador amarillo y recuadros
- **Dónde:** V3 8–10 s (tabla de precios), V3 13,5–16 s (tarjetas con "a fifth" resaltado), V4 4,25–5,75 s ("Your Total"), V5 5,5 s (caja roja alrededor de **$20.000.000**), V6 (recuadro rojo alrededor de los tres medidores).
- **Qué se ve [VISTO]:** recuadros **rojo** (lo caro o malo) y **verde** (lo barato o bueno), y una franja amarilla (**≈ #FAEFA1**, medida) que pasa por la fila o frase importante, de izquierda a derecha.

### M9 — Meme y emoji de reacción
- **Dónde:** V5 (4 memes: 0–1,25 s, 5,75–7,75 s y 8,75–9,5 s, el más denso), V6 (3), V3 (2), V2 (1 + emoji), emoji 🤔 con signos de interrogación que flotan (V2, V5).
- **Qué se ve [VISTO]:** el meme entra en **la misma tarjeta** que el resto y casi siempre en un bloque de capa Cara, justo cuando Albert reacciona. Marca el chiste o la sorpresa.
- **Receta:** meme en la tarjeta de arriba cuando la frase es una reacción.

### M10 — Lista que se rellena al ritmo de la voz
- **Dónde:** V5 16–20 s (modelos: "Seedance 2.5", "Kling 3.0", "MiniMax H3", "Wan 3.0", "Genjutsu", con un check verde por cada uno), V3 33,25–35,5 s (checklist de tres pasos), V3 25,75–27,5 s (lista de tareas con checks), V6 31,25–34 s (sub-agentes con su modelo).
- **Qué se ve [VISTO]:** cada fila **aparece justo cuando se dice** y se marca con un check verde unas décimas después.

### M11 — Brillo diagonal sobre tarjeta quieta
- **Dónde:** V3 15–16 s, V4 5,5–5,75 s, V5 17–18 s, V6 6,25–7 s.
- **Qué se ve [VISTO]:** cuando una tarjeta se queda **fija** más de un par de segundos, le pasa una **franja blanca diagonal** por encima. Evita que parezca una imagen congelada.

### M12 — Ráfaga de resultados dentro de la tarjeta
- **Dónde:** V4 24,25–27,5 s (Runable): webs, presentación, gráficos y posts de Instagram pasan sobre una tarjeta con degradado naranja-rosa, uno cada ≈ 0,25–0,5 s.
- **Receta:** una ráfaga rápida de resultados, tantos como la frase pida ("does the work of all of..."), todos en la misma tarjeta.

### M13 — Diagrama de nodos con líneas
- **Dónde:** V6 28,75–31 s (CLAUDE.md arriba con tres sub-agentes debajo, cada uno con su etiqueta de modelo), V5 11–14,5 s ("You" → "API" → "Higgsfield", con billetes que viajan por la línea y luego el cheque), V3 26,75–28,5 s (dot → ChatGPT Work y Codex).
- **Receta:** líneas finas que se dibujan, cajas pequeñas con etiqueta de color y un objeto (billete, texto) que viaja por la línea.

### M14 — Cierre: tarjeta de comentarios
- **Dónde:** los 6 videos, siempre al final.
- **Secuencia [VISTO]:** Albert dice "comenta X" → se pulsa el campo → se **teclea la palabra clave** (`/video`, `DOTS`, `STACK`, `API`, `SAVE`) → se pulsa "Post" → aparece el comentario → se pulsa el **corazón y se pone rojo** → fin.
- **Variantes:**
  - V1, V2, V3: la tarjeta muestra el comentario fijado de Albert ("Comment 'VIDEO' and I'll send you the link").
  - V4, V5, V6: aparece "No comments yet".
  - V5: una burbuja de "escribiendo…" aparece debajo (simula la respuesta).
  - V6: una cápsula "CLAUDE.md · the full prompt" con flecha se "envía" (la flecha se pone azul).

---

## 8. La estructura de cada video

Plantilla extraída de los 6 [MEDIDO + VISTO]:

| Tramo | Qué pasa | Capa |
|---|---|---|
| **0 – ≈ 4,5 s** (V3: 2,5 s, V4 y V5: 7–8 s) | **Gancho.** Un gag "X mató a Y", un meme, o una demo directa. **Sin cara.** | Pantalla (con efecto a pantalla completa en V2, V3, V6) |
| **Hasta ≈ 8 s** | Primera cara: reacción o "esto es lo que importa". | Cara |
| **Resto** | Alternancia: Pantalla muestra, Cara explica o reacciona. Cada ≈ 3,8 s. | Alterna |
| **Últimos 3 – 7,5 s** | Una frase que dice qué recibes ("I made a quick guide…") + CTA con la tarjeta de comentarios. | Cara |
| **Final** | Corazón rojo y corte. | — |

Hay **dos cosas que repite siempre**:
1. **Un resumen en el gancho de lo que viene.** En V3, V5 y V6 el primer subtítulo ya contiene el titular ("ChatGPT just dunked on Opus 5.5", "Higgsfield just hit a billion-dollar run rate", "Claude just killed Astra"). Ocurre sin cara.
2. **Un recurso gratis al final.** En los 6 videos termina con "comenta X y te lo envío".

---

## 9. Receta mínima para imitar el estilo

1. Fondo beige **#F0EFEA** y dos capas, **Pantalla** y **Cara**, que se turnan.
2. El video **empieza en Pantalla sin cara** y **termina en Cara** con la tarjeta de comentarios.
3. Un cambio de capa **cada ≈ 4,3 s** (los bloques duran entre 1 y 8 s, 3,8 s de media).
4. Costura entre tarjeta y cara en **y = 571 px**. Subtítulo de Pantalla centrado en **y ≈ 773 px**. Dejar libre el último **35 %** de la capa Pantalla.
5. Dos sistemas de subtítulo: **palabra por palabra** (sans negrita, 1–3 palabras, cada ≈ 0,35 s) en Pantalla y **frase corta en mayúsculas monoespaciadas sobre caja negra** en Cara.
6. Color de énfasis: **verde** para lo bueno, **rojo** para lo malo, **cursiva con serifa** para nombres, comandos y cifras.
7. **Cada cosa que se dice aparece dibujada** en ese momento. Los números **siempre cuentan** hasta una caja verde o roja.
8. Los **logos son personajes**. Un gag "X mató a Y" en el gancho cuando el tema sea una rivalidad.
9. Un **efecto a pantalla completa** (explosión, balón, telón) como puente entre el gancho y el contenido.
10. Terminar siempre con **"comenta X"**, con la palabra tecleada y el corazón rojo.

---

## 10. Lo que no sé, no medí o es hipótesis

1. **Las curvas de las animaciones.** A 4 fps no veo cuánto tardan los rebotes, las entradas o los cortes, ni si hay "overshoot". Falta medir a 30 fps las transiciones: explosión, balón, telón, el cambio entre capas y la entrada de las tarjetas.
2. **El audio.** No analicé los efectos de sonido ni la música. Están separados en `audio/` pero no los escuché para este análisis.
3. **Las tipografías.** Solo sé cómo se ven (sans negrita, serifa cursiva, monoespaciada). No tengo el nombre real de las fuentes.
4. **Las maquetas.** No sé si las pantallas (agente "Shiney", la tabla de precios, el editor) son capturas reales o están hechas a mano con código. Las que se ven con fechas "September 2026" y la interfaz de "dots" parecen hechas a mano, pero **no lo he comprobado**.
5. **El 7.º video.** Con restricción de edad: falta para que el análisis sea de los 7. Cabe que muestre algo que los otros 6 no.
6. **Solo 6 videos de una misma semana.** El patrón es consistente en todos, pero no sé si Albert lo ha usado siempre o lo estrenó hace poco.
7. **La regla "cuándo cara y cuándo pantalla"** (sección 4.4) es mi interpretación de lo que vi. Albert puede decidirlo por otro motivo.

---

## Apéndice A — Cronología por video

(Segundos aproximados, a 0,25 s de precisión. `P` = Pantalla, `C` = Cara.)

### V1 · Dd9O9UpCRNs · Higgsfield en ChatGPT (34,75 s)
| Seg. | Capa | Qué pasa |
|---|---|---|
| 0–4,25 | P | La tarjeta se acerca al campo de texto, teclea `/tinder`, "Thinking", aparece la foto de perfil de Tinder |
| 4,25–8,0 | C | `/linkedin` y la foto profesional |
| 8,0–12,5 | P | `@h` → Higgsfield, `/pov`, perro, vídeo POV generado |
| 12,5–17,75 | C | `/360` con una zapatilla, que gira en 7 posiciones |
| 17,75–23,0 | P | `/ugc` con un frasco y la mujer que lo presenta |
| 23,0–27,75 | C | "This won't work by default": menú de ChatGPT (Library, Projects, Plugins) |
| 27,75–32,0 | P | Busca "Hig" en Plugins, pulsa "+", entra en Higgsfield, "ready to go" |
| 32,0–34,75 | C | Comentarios: teclea `/video`, corazón |

### V2 · Dd_w892CW-m · dots frente a Muse (31,5 s)
| Seg. | Capa | Qué pasa |
|---|---|---|
| 0–2,25 | P + efecto | Avión con logo ChatGPT bombardea a "Muse from Meta", explosión a pantalla completa |
| 2,5–4,75 | P | Telón rojo que se abre, aparece "dots" (mascota amarilla con gafas y pajarita) |
| 4,75–8,5 | C | Iconos de apps en abanico, meme Pepe Silvia; 7,75–8,5 s: cara a pantalla completa |
| 8,5–11,5 | P | Agente "Shiney": maqueta de chat y su "computer" |
| 11,5–12,5 | C | Emoji 🤔 con "?" flotantes |
| 12,5–15,75 | P | Navegador del agente: búsqueda "best CRM for small agencies", Gmail |
| 15,75–19,0 | C | iPhone con hora corriendo (12:47 → 6:12) y notificaciones; 17,25 s: tarjeta negra "dots" con 4 mascotas |
| 19,0–27,0 | P | Podio de OpenAI con trofeo y confeti, "Muse from Meta" más bajo; mascotas con cerebros rosados (el de dots crece, el de Muse se encoge) |
| 27,0–31,5 | C | "Your dot", comentario `DOTS`, corazón |

### V3 · Dd5_N6EiY4h · GPT-6.1 Sol y dots frente a Opus 5.5 (37,75 s)
| Seg. | Capa | Qué pasa |
|---|---|---|
| 0–2,5 | P + efecto | ChatGPT hace un mate sobre Claude; el balón llena la pantalla |
| 2,5–8,0 | C | Foto del evento, web "GPT-6.1 Sol", barra OSWorld 2.0 de 20,1 a 71,4 |
| 8,0–10,25 | P | Tabla de precios con recuadros rojo ($10/$50) y verde ($2/$10) y fila amarilla |
| 10,25–13,5 | C | Memes (Chris Pratt, DiCaprio señalando), el logo de Claude entra |
| 13,5–16,0 | P | Dos tarjetas ("GPT-6.1 Sol", "Claude Opus 5.5") con "a fifth" resaltado |
| 16,0–17,75 | C | Barras del índice de inteligencia (Opus 5.5 sube de 19,4 a 57,6) |
| 17,75–20,0 | P | Tuit de OpenAI con vídeo "dots" |
| 20,0–23,0 | C | Mascota azul con boina; "dots = Grok Bot" |
| 23,0–25,75 | P | Tres mascotas con su "computer" cada una |
| 25,75–28,75 | C | Lista de tareas con checks y diagrama dot → ChatGPT Work / Codex |
| 28,75–33,25 | P | "Introducing dots" y debajo "GPT-6.1 Sol $2–$10"; "cheaper" en verde |
| 33,25–37,75 | C | Checklist "Set up dots…", comentario `DOTS`, corazón |

### V4 · Dd1dN_EgWvk · Runable (30,5 s)
| Seg. | Capa | Qué pasa |
|---|---|---|
| 0–7,25 | P | 10 logos caen, emoji 😬, calculadora ($216,98/month), pistola de pintura mata a Calendly |
| 7,25–8,75 | C | Chat del agente "?" con Google Calendar |
| 8,75–10,5 | P | "?" aplasta a Otter.ai |
| 10,5–13,0 | C | Videollamada, el agente se une; nota "Wednesday Standup" se escribe sola |
| 13,0–14,25 | P | Katana corta a Zapier |
| 14,25–17,0 | C | "Connect Apps": contador 19 → 3.000+ |
| 17,0–19,25 | P | Cañón de confeti sobre ChatGPT y Claude |
| 19,25–23,5 | C | Selector de modelos; los logos orbitan alrededor del "?" y se van |
| 23,5–27,75 | P | Logo "Runable" y ráfaga de resultados sobre degradado naranja-rosa; hub con apps conectadas |
| 27,75–30,5 | C | Comentarios, `STACK`, corazón |

### V5 · DduBEWLCIy4 · Higgsfield y el cashback (34,0 s)
| Seg. | Capa | Qué pasa |
|---|---|---|
| 0–8,0 | P | Meme Drake "Nah", meme del mago "crazy", gráfico que crece con logo Higgsfield, odómetro $1.000.000.000, tuit, DiCaprio brindando con 🎉 |
| 8,0–11,0 | C | 🤔, meme de Fry, calendario de septiembre que se rellena en verde del 26 al 30 ("5 days") |
| 11,0–16,0 | P | "You → API → Higgsfield" con billetes; cheque con 0 % → 100 % |
| 16,0–20,25 | C | Lista de modelos con checks |
| 20,25–23,0 | P | Medidor $0 → $100.000 "per business" |
| 23,0–26,75 | C | Bolsa de cashback $20.000.000 → $0 (rojo) |
| 26,75–30,75 | P | Personas que llegan al buzón "CASHBACK"; temporizador del 26 al 30; "5 days"; barra "MAX" |
| 30,75–34,0 | C | Comentarios, `API`, corazón |

### V6 · DdocHKLq7i0 · CLAUDE.md y Opus 5.5 (38,75 s)
| Seg. | Capa | Qué pasa |
|---|---|---|
| 0–1,0 | P | Dario Amodei y Sam Altman con un lanzacohetes |
| 1,0–1,75 | efecto | Explosión a pantalla completa |
| 1,75–4,5 | P | Logo de Claude y "Claude Opus 5.5" que se escribe letra a letra |
| 4,5–7,25 | C | Tres medidores (Claude, ChatGPT, Gemini) que se ponen rojos, "Limit reached" |
| 7,25–11,25 | P | Meme Michael Scott y dedo medio, "usage limit" en rojo |
| 11,25–15,75 | C | Barra roja que baja a verde, meme Roll Safe, el editor con CLAUDE.md |
| 15,75–19,25 | P | Teclea "Never do the work yourself. Always dispatch a sub-agent." |
| 19,25–27,25 | C | Teclea "Don't always use Fable. Use Opus 5.5 for easier tasks." y el bloque "Model routing" |
| 27,25–31,25 | P | Icono CLAUDE.md, meme Lobo de Wall Street ("And boom"), árbol de sub-agentes con modelos |
| 31,25–38,75 | C | Lista de sub-agentes con modelo, comentarios `SAVE`, cápsula del prompt que se envía |

---

## Apéndice B — Correcciones de la transcripción comprobadas en pantalla

La transcripción automática (Whisper `small`) se equivocó en nombres propios. Aquí van los que **comprobé con texto que aparece en pantalla**. **No he modificado** los archivos `transcripcion.txt` ni `.srt`.

| Transcripción | Pantalla dice | Video |
|---|---|---|
| "Hicksville" | **Higgsfield** | V1 |
| "chat.jbc" | La interfaz es **ChatGPT** (no pude leer la dirección) | V1 |
| "DUTs", "dots" | **dots** | V2, V3 |
| "Chatchity" | **ChatGPT** | V3 |
| "Solo 6.1" | **GPT-6.1 Sol** | V3 |
| "Grogbutt" | **Grok Bot** | V3 |
| "Astra" | **GPT-6 Astra** (era correcto) | V3, V6 |
| "Sabia" | **Zapier** | V4 |
| "Runnable" | **Runable** | V4 |
| "ends 2.5" | **Seedance 2.5** | V5 |
| "clink 3.0" | **Kling 3.0** | V5 |

Los nombres "Muse", "Opus 5.5", "Fable" y "Claude" estaban bien.
