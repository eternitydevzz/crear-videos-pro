# Estilo «Enrique-mex»

> **Nota del repo:** esta ficha se hizo con el reel descargado y sus archivos de trabajo (`video.mp4`, `Frames/`, `cortes.txt`, `info.txt`, `audio/`, `transcripcion.md` y `ventanas/`). En el repo solo están la ficha y los **mosaicos**: esos archivos se citan como fuente de los datos, pero no se incluyen. Para tenerlos, pasa el link del reel por `/crear-videos-pro:crear-estilo-videos`.

Sale de 4 reels (talking head sobre Claude, en español de México):

| Carpeta | Link | Tema | Duración |
|---|---|---|---|
| video1 | instagram.com/p/DeRSjtdineF | Auditar tu app de Claude (arnés de seguridad) | 68,8 s |
| video2 | instagram.com/p/DeOgu1ECD_l | Haiku 5.5: 90 % más barato | 48,6 s |
| video3 | instagram.com/p/DeJYliUCna5 | Agente que vigila lo que hace Claude | 59,2 s |
| video4 | instagram.com/p/DeEauAsimty | Skills para mejorar el diseño de tu web | 52,6 s |

Una regla solo entra en la ficha si se repite en los 4 vídeos. Lo que cambia de uno a otro va como **variante**.
**[MEDIDO]** = sale de un fotograma, de `medir.py` o de `audio.sh`. **[SUPOSICIÓN]** = es mi interpretación.

Lo que el usuario quiere replicar (manda sobre todo lo demás): **un sonido distinto para cada palabra clave, fotos de Claude o de lo que se está hablando, y memes para dar dinamismo. Un estilo fácil y viral.** No hay música (lo dijo el usuario).

---

## Resumen: 10 reglas

1. **Un plano fijo de la cara** (A-roll) casi todo el vídeo, grabado con el móvil en vertical: 1440×2560 a 30 fps. [MEDIDO]
2. **Título fijo arriba durante todo el vídeo**: 2 líneas blancas en negrita, sin caja, centradas, entre y = 469 y 712 px (18–28 % del alto). [MEDIDO]
3. **Subtítulo pequeño abajo**: 1 a 4 palabras, blanco, sin caja, centrado, a y ≈ 2031–2141 px (79–84 %). Cambia cada 0,4–0,9 s siguiendo la voz. [MEDIDO]
4. **Cada palabra clave lleva un elemento visual encima del subtítulo**, a la altura del pecho. Es una de estas 4 cosas: recuadro blanco con texto, logo de app, sticker pixel art o captura/meme. [MEDIDO]
5. **Ritmo de elementos**: en el vídeo más denso (video2) entra uno cada **1,7 s** de media (29 en 48,6 s). En video4 entran 13 en los primeros 41 s, uno cada ~3 s, y en los últimos 11 s ninguno. [MEDIDO, contado en mosaicos]
6. **Todo entra creciendo**, de pequeño a su tamaño, en **3–4 fotogramas (0,2–0,27 s)**. No hay fundidos de entrada. [MEDIDO en mosaicos: 1,33→1,53 s en video1, 5,40→5,60 s en video2]
7. **Todo sale de golpe**, sin animación: o desaparece de un fotograma al siguiente o se va con un jump cut. [MEDIDO]
8. **Los memes y capturas tapan la cara**: rectángulo con esquinas redondeadas centrado a la altura de los ojos, de 1,2 a 3 s. [MEDIDO]
9. **Recuadro de palabra clave**: caja blanca redondeada con texto negro en negrita y a veces un emoji (🔥 💯 ✅ ❌ 👀). Se pueden **apilar en lista** (2–3 recuadros, uno debajo de otro, entrando de uno en uno). [MEDIDO]
10. **Audio igualado a −14 LUFS**, pico de −0,1 a −0,7 dBFS, casi mono, con las pausas de la voz recortadas: los silencios miden ≤ 0,23 s. [MEDIDO] Hay sonido en cada elemento que entra: lo dice el usuario. Los segundos exactos, el tipo de sonido y su volumen **no los he medido** [SUPOSICIÓN, ver § 8].

---

## 1. Datos técnicos [MEDIDO]

| | video1 | video2 | video3 | video4 |
|---|---|---|---|---|
| Resolución | 1440×2560 | 1440×2560 | 1440×2560 | 1440×2560 |
| fps | 30 | 30 | 30 | 30 |
| Duración | 68,8 s | 48,6 s | 59,2 s | 52,6 s |

Duración típica: **48–69 s**.

## 2. Estructura y ritmo

**Cortes de plano.** La herramienta marcó casi todos los cortes como «dudosos» (51, 29, 20 y 14). En los mosaicos se ve que la mayoría son **jump cuts dentro del mismo plano de cara**: él se queda en el mismo sitio y solo cambia un poco la postura o el acercamiento, por ejemplo en video1 a 3,20→3,26 s y a 11,40→11,53 s. Además se quitan las pausas: ningún silencio pasa de 0,23 s. [MEDIDO en mosaicos y en `audio/medidas.txt`] No los he mirado uno a uno a 30 fps con `ventana.sh`, así que **el número exacto de jump cuts no está verificado**.

**B-roll (solo en video4)** [MEDIDO]: 6 cortes duros entre 13,97 y 20,40 s. Son grabaciones de la pantalla del portátil hechas con el móvil (GitHub y la página de la skill) y se alternan con la cara:

| Inicio | Fin | Duración | Tipo |
|---|---|---|---|
| 13,97 | 15,33 | 1,36 s | Pantalla (perfil de GitHub, con acercamiento lento) |
| 15,33 | 16,17 | 0,84 s | Cara |
| 16,17 | 17,60 | 1,43 s | Pantalla (web de la skill) |
| 17,60 | 18,70 | 1,10 s | Cara |
| 18,70 | 20,40 | 1,70 s | Pantalla (README / instalar) |

Variante: video1, video2 y video3 no tienen B-roll de pantalla. Usan capturas flotantes encima de la cara (§ 6).

**Arco del vídeo** [MEDIDO en transcripciones y mosaicos]:
- 0–3 s: gancho con el problema o la promesa («Te van a hackear…», «Claude ahora te sale 90 % más barato»). El primer elemento entra antes de 1,5 s (a 0,33 s en video1, 0,53 s en video4 y 1,06 s en video2).
- Desarrollo: un elemento visual por cada palabra clave.
- Últimos ~5 s: CTA hablado: «comenta …», «te lo paso», «sígueme y compártelo». En video2 sale el sticker «TE LO PASO» a 45,4 s y el botón «+ SEGUIR» a 46,66 s.

## 3. Transiciones [MEDIDO]

- **Corte duro** entre planos, siempre.
- Lo que `extraer.sh` marca como «disolvencia (2–4 fotogramas)» coincide en los mosaicos con la entrada de un meme o una captura que tapa la cara (por ejemplo, video1 a 0,33 s), **no con un fundido entre planos**. No he visto ningún fundido real.

## 4. Zoom y encuadre

- A-roll: plano medio corto. La cabeza ocupa la mitad superior, cortada por arriba a la altura de la coronilla, y se ve el pecho. [MEDIDO en mosaicos]
- Hay cambios de acercamiento entre jump cuts: la cara salta a un tamaño un poco mayor o menor. **No he medido la escala con `medir.py encuadre`.** [SUPOSICIÓN: es un zoom digital del editor o el móvil movido entre tomas; no lo puedo distinguir]
- B-roll de video4: acercamiento lento dentro del plano (de 14,00 a 14,86 s la pantalla crece de forma visible). [MEDIDO en mosaico]

## 5. Subtítulos

**Título fijo (gancho escrito)** [MEDIDO con `medir.py`]
- 2 líneas centradas: línea 1 a y 469–557 px (video2) / 524–609 px (video4), con 86–89 px de alto y hasta 1019 px de ancho; línea 2 a y 574–712 px, con 70–86 px de alto.
- Blanco #FCFCFC, negrita, sin caja ni contorno visible. Una sombra suave **no la he podido comprobar**.
- Está desde el fotograma 0 hasta el final, también encima del B-roll.
- Texto: 5–7 palabras con la promesa, y a veces una palabra en mayúsculas («**AUDITA** bien tu proyecto de Claude»).

**Subtítulo de voz** [MEDIDO]
- y 2031–2088 px (video2) / 2072–2141 px (video4) = **79–84 %** del alto. Alto de línea 58–70 px, unas 3 veces menor que el título.
- Blanco #F8F6F7–#FDF9FC, sin caja, centrado (centro x 716–718).
- **1 a 4 palabras por bloque**, normalmente 2–3, en minúscula salvo nombres propios. Ejemplos: «tienes cloud y», «página web», «y quieres mejorar».
- Cambia de golpe, sin animación, cada **0,4–0,9 s**.
- No resalta ninguna palabra dentro del subtítulo: el resalte lo hace el recuadro o sticker de encima.

**Recuadro de palabra clave** [MEDIDO]
- Caja blanca con esquinas redondeadas y texto negro en negrita, 1 línea (a veces 2). y 1710–1827 px (≈ 67–71 %), justo encima del subtítulo. En video2 mide 716 px de ancho.
- El texto es la idea resumida, no la frase literal: la voz dice «te sale 90 %» y el recuadro pone «90 % más barato»; la voz dice «velocidad no es igual a calidad» y el recuadro pone «Velocidad ≠ calidad 💯».
- Dura 1,5–3 s, más que el subtítulo, y sigue en pantalla mientras cambia el subtítulo de debajo.
- **Lista apilada**: «Resumir» → «Clasificar» → «Compactar» (video2, 25,33 / 26,06 / 26,93 s) y «Un skill ❌» → «Una herramienta ❌» → «Un arnés ✅» (video1, 10,66 / 11,53 / 12,26 s). Cada recuadro nuevo entra debajo del anterior.
- Variante: en video3 (38,73→39,13 s) el recuadro sale vacío y se escribe **letra a letra** («Ar» → «Arré» → «Arréglalo.») en unos 0,4 s.

## 6. Textos en pantalla y gráficos

Hay 4 tipos de elemento. Todos entran creciendo en 0,2–0,27 s y salen de golpe. [MEDIDO]

| Tipo | Cómo es | Dónde | Cuánto dura | Ejemplos (segundo) |
|---|---|---|---|---|
| **Recuadro de texto** | caja blanca, texto negro en negrita y emoji | y ≈ 67–71 % | 1,5–3 s | «90 % más barato» v2 1,06; «Acaba de salir 🔥» v2 10,40; «Un equipo completo 🔥» v1 33,20 |
| **Logo de app** | icono cuadrado blanco redondeado con el logo y el nombre debajo (Claude, ChatGPT) | pecho, centrado | 0,6–1 s | Claude v1 1,33; v2 4,26; v3 1,20; v4 0,53. ChatGPT v2 20,26 |
| **Sticker pixel art** | mascota naranja pixelada + cartel con la palabra en mayúsculas pixeladas + icono (papelera, casilla ✅, monitor, regalo…) | pecho, centrado, ~300 px de ancho | 1–1,6 s | «BASURA» v4 6,40; «DILE A CLAUDE» v4 21,26; «REGLAS DE APPLE» v4 22,80; «TE LO PASO» v2 45,40; botón «+ SEGUIR» v2 46,66; robot con candado v1 2,20; mascota con gafas de sol y rayo v2 15,13 |
| **Captura o meme** | rectángulo con esquinas redondeadas; tapa los ojos o la cara | centro, a la altura de los ojos | 1,2–3 s | Capturas: tarjeta «Claude Opus 5.5» v2 5,46; «Sonnet 5.5» 6,60; «Claude Haiku 5.5» 8,20; tabla de benchmarks 20,80; «Egg drop test» 29,80. Memes: hombre con pasamontañas ante ordenadores v1 0,33; hombre de sitcom con cara de asombro v2 11,53; hombre en sofá a oscuras v2 17,26; hombre en oficina v2 34,60; niña mirando de reojo v1 21,20; hombre de esmoquin aplaudiendo en una gala v1 54,53 |

**Qué tipo va con cada palabra** [SUPOSICIÓN sacada del patrón de los 4 vídeos]:
- Una **marca o producto** nombrado (Claude, ChatGPT, Opus) lleva su logo o su captura real.
- Un **dato o idea fuerte** («90 % más barato», «Lo más importante») lleva un recuadro de texto.
- Una **acción o un consejo** («dile a Claude», «analiza», «referencias», «te lo paso») lleva un sticker pixel art.
- Una **emoción o reacción** (sorpresa, ironía, «sales bien», «hackear») lleva un meme.

Los stickers pixel art son un recurso propio y repetido: el mismo personaje en los 4 vídeos. [MEDIDO] De dónde salen (si los hizo él, si son de un pack o de una app) **no lo sé**.

## 7. Color [MEDIDO en fotogramas]

- Fondo: pared beige/gris cálido con puerta y luz amarilla de techo. Piel cálida. Camiseta verde oliva (video1 y video2) o blanca (video3 y video4).
- Texto: blanco #FCFCFC (título y subtítulos). Recuadros blancos con texto negro.
- Acentos: el naranja/terracota de Claude (logo y mascota pixel art), azul y verde en los carteles pixelados, rojo ❌ y verde ✅.
- No se ve una corrección de color marcada: parece la imagen del móvil con luz cálida de interior. [SUPOSICIÓN]

## 8. Sonido [MEDIDO, limitado]

No he escuchado el audio. El usuario confirma que **no hay música** y que **cada palabra clave lleva su sonido, que va variando, y unos destacan más que otros**.

| | video1 | video2 | video3 | video4 |
|---|---|---|---|---|
| Sonoridad integrada | −14,1 LUFS | −14,0 LUFS | −14,1 LUFS | −14,2 LUFS |
| Rango (LRA) | 3,0 LU | 2,9 LU | 3,4 LU | 2,4 LU |
| Pico | −0,1 dBFS | −0,3 dBFS | −0,1 dBFS | −0,7 dBFS |
| Lateral vs central | −34,6 dB | −33,1 dB | −33,7 dB | −32,1 dB |
| Silencio más largo (< −45 dB) | 0,16 s | 0,18 s | 0,23 s | 0,18 s |

- Casi mono (el lateral está ~33 dB por debajo). Volumen muy constante (LRA ≤ 3,4 LU). Pausas recortadas.
- **Espectrograma de video2, 0–10 s** [SUPOSICIÓN]: se ven rayas verticales finas que suben por encima de 4–13 kHz cerca de 1,0–1,1 s, 4,3 s y 5,4–5,5 s. Coinciden (±0,2 s) con la entrada del recuadro «90 % más barato» (1,06), el logo de Claude (4,26) y la tarjeta de Opus (5,46). Puede que sean los efectos de sonido, pero también pueden ser consonantes de la voz («s», «t»): **no lo puedo separar sin escucharlo**.
- **Qué sonido es cada uno, cuánto dura y a qué volumen va respecto a la voz: no está medido.** El usuario decidió no separar el audio con la otra skill.

## 9. Receta para replicar

1. **Graba** en vertical (1440×2560 o 1080×1920, 30 fps), en plano medio corto, con luz cálida y fondo de casa. Habla directo a cámara 50–70 s.
2. **Recorta las pausas** con jump cuts. Ningún silencio debe pasar de ~0,2 s.
3. **Pon el título fijo** arriba (18–28 % del alto): 2 líneas blancas en negrita, sin caja, de principio a fin. Es la promesa en 5–7 palabras.
4. **Pon los subtítulos de voz** abajo (79–84 %): blancos, pequeños (~1/3 de la altura del título), 2–3 palabras por bloque, en corte seco.
5. **Marca las palabras clave** del guion: una cada 1,5–3 s, más seguidas al principio. Para cada una elige el tipo según la tabla del § 6 (marca → logo/captura, dato → recuadro, acción → sticker, emoción → meme).
6. **Haz entrar cada elemento creciendo** en 6–8 fotogramas a 30 fps (0,2–0,27 s), justo cuando se dice la palabra. Sácalo de golpe a los 1–3 s o con el siguiente jump cut.
7. **Ponle un sonido corto a cada entrada**, distinto según el tipo, y más fuerte en las palabras más importantes (lo pide el usuario). Qué sonidos usar: **pendiente de decidir con el usuario** (§ 10).
8. **Usa listas apiladas** cuando haya 2–3 opciones o pasos: un recuadro por opción, entrando de uno en uno.
9. Si enseñas una herramienta, mete **B-roll de pantalla** (1–1,7 s por plano, alternando con la cara y con un acercamiento lento).
10. **Cierra** con un CTA hablado de comentario («comenta X y te lo paso»), con el sticker «TE LO PASO» y el botón «+ SEGUIR».
11. **Audio final**: voz a −14 LUFS, pico ≤ −0,1 dBFS, mono. No uses loudnorm dinámico; ver la memoria [[audio-no-loudnorm-dinamico]].

## 10. Lo que no se pudo determinar

- **Fuente** del título, los subtítulos y los recuadros: es una sans-serif en negrita y redondeada, parecida a la de los subtítulos automáticos de las apps de edición móvil. **No sé su nombre.**
- **App de edición y nombre de las animaciones**: se ve un «crecer al entrar» de 0,2 s; no sé cómo se llama en ninguna app.
- **Origen de los stickers pixel art y de los memes**: no lo sé.
- **Sonidos**: cuáles son, sus segundos exactos, su volumen relativo y cómo decide cuál «destaca». No se escuchó ni se separó el audio.
- **Número exacto de jump cuts** y escala del zoom entre tomas: no se miraron los «dudosos» uno a uno a 30 fps ni se midió el encuadre.
- **Mosaicos que no revisé uno a uno**: en video1 y video3 leí un fotograma de muestra cada ~10 s (video1: 0–4 s, 10–13 s, 19–21 s, 32–34 s y 53–55 s; video3: 0–4 s, 21–23 s y 38–40 s). video2 lo revisé completo; video4 también, salvo los tramos de 2,1 a 6,4 s y de 8,5 a 12,8 s. Las reglas salen sobre todo de video2 y video4, y comprobé en video1 y video3 que se cumplen.
