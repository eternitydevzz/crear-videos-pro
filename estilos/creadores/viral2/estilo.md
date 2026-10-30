# Estilo «Viral2»

> **Nota del repo:** esta ficha se hizo con el reel descargado y sus archivos de trabajo (`video.mp4`, `Frames/`, `cortes.txt`, `info.txt`, `audio/`, `transcripcion.md` y `ventanas/`). En el repo solo están la ficha y los **mosaicos**: esos archivos se citan como fuente de los datos, pero no se incluyen. Para tenerlos, pasa el link del reel por `/crear-videos-pro:crear-estilo-videos`.

Reel de referencia: https://www.instagram.com/reel/Deh74uvPQWt/ (en portugués; tema: una skill de Claude para Instagram).
Lo que el usuario quiere replicar: **gráficos en pantalla, ritmo y cortes, zooms y encuadre**. Música: **no** (lo dijo el usuario). Sonidos: **los que suenan cuando las animaciones «explotan»**.

> Aviso: este reel no es una grabación editada. Es **una animación completa en pixel art** (no sale ninguna persona real). Para replicarlo hay que construir cada escena como animación (por ejemplo con HyperFrames), no cortar un vídeo grabado. Eso lo hace más lento que un estilo de «cara + subtítulos».

## Resumen: 10 reglas

1. **1080×1920, 30 fps, 34,4 s** [MEDIDO].
2. **14 escenas en 34,4 s**: una cada **2,45 s** de media (mínimo 1,40 s, máximo 4,10 s) [MEDIDO en mosaicos].
3. Hay dos tipos de cambio de escena: **«tajo» diagonal** (una línea clara cruza la pantalla en 2–3 fotogramas) y **corte duro**. No hay disolvencias de verdad [MEDIDO].
4. **Cada cambio de escena lleva un golpe de sonido** que empieza **unos 30–60 ms antes** de la imagen nueva. Coinciden 14 de 14 [MEDIDO en el audio].
5. Fondo fijo: una sala oscura en pixel art (estanterías, antorchas, suelo con rejilla y un círculo punteado), **#0D0D11 → #1B1B1F**. Un personaje pixel art (cabeza = logo naranja de Claude) está siempre en el centro, sobre el suelo, con pies en **y≈1310** [MEDIDO].
6. **Una tarjeta-gráfico grande por escena** encima del personaje, centrada, entre **y≈360 y y≈1045**. Entra **creciendo desde pequeña en ~4 fotogramas** y luego se rellena por partes (iconos que aparecen uno a uno, texto que se escribe letra a letra, barras que se llenan) [MEDIDO en mosaicos].
7. **Palabra clave encima de la tarjeta** (y≈309–344, 36 px de alto), escrita **letra a letra** (~14 letras en 10 fotogramas) en una cajita oscura. En **blanco** o en **naranja #BD705C–#CB765D** [MEDIDO].
8. **Subtítulo fijo abajo**: MAYÚSCULAS blancas #FBFBFB, **48 px de alto de letra**, centrado en **x=539**, letra en **y 1376–1423** (73 % del alto), dentro de una **caja negra #050505** de **90 px de alto** (y 1357–1446) con **~28 px de margen** a los lados [MEDIDO].
9. **2–4 palabras por subtítulo**, 40 bloques, uno cada **0,86 s** de media. Cambian de golpe: el primer fotograma sale en gris y al siguiente ya en blanco (fundido de 1 fotograma) [MEDIDO].
10. Paleta: casi negro + gris oscuro + **naranja terracota** como único acento (más rosa/morado solo para Instagram). Sonoridad **−14,1 LUFS**, pico **−1,9 dBFS**, casi mono [MEDIDO].

---

## 1. Datos técnicos [MEDIDO]

- Resolución: 1080×1920 (9:16). Fps: 30 constante (`fps_variable=no`). Duración: 34,387 s.
- Fuente: `info.txt`.

## 2. Estructura y ritmo

Todo es «gráfico» (no hay A-roll con persona). Inicio de cada escena leído en los mosaicos (15 fps, ±0,07 s); los marcados con * se comprobaron a 30 fps (tiras de `ventanas/`, no incluidas).

| # | inicio | fin | dura | qué se ve | entra con |
|---|---|---|---|---|---|
| 1 | 0,00 | 1,83* | 1,83 | Pelea estilo videojuego: Claude contra Instagram, barras de vida arriba. 3 golpes, Instagram cae | — |
| 2 | 1,83* | 5,03* | 3,20 | Ventana de Claude: chip «habilidade» ✓, flecha, tarjeta «único agente de IA» escribiéndose | tajo (3 fot.) + zoom out |
| 3 | 5,03* | 7,57 | 2,53 | Red: logo arriba, contador **0→11** y 11 iconos que van apareciendo y se iluminan | corte duro* |
| 4 | 7,57 | 11,67* | 4,10 | Perfil de Instagram (móvil) que se va rellenando de publicaciones | tajo |
| 5 | 11,67* | 14,13 | 2,47 | Publicación: foto + texto que se escribe | corte duro* |
| 6 | 14,13 | 16,33 | 2,20 | Lista de comentarios que aparecen y respuestas en naranja | tajo |
| 7 | 16,33 | 17,80 | 1,47 | Perfil otra vez, una línea naranja lo «escanea» de arriba abajo y lo mejora | tajo |
| 8 | 17,80 | 19,20 | 1,40 | Calendario semanal: tarjetas que caen una por día | tajo |
| 9 | 19,20 | 22,13 | 2,93 | Red de 11 iconos que se apaga, uno crece hasta ser la tarjeta «viralização» con curva que sube | corte duro |
| 10 | 22,13 | 24,57 | 2,44 | Rejilla de 8 reels; una línea naranja los recorre; los peores se apagan | corte duro |
| 11 | 24,57 | 26,23 | 1,66 | Un reel + gráfica de retención que se dibuja | tajo (`cortes.txt` lo da como «disolvencia 2 fot.») |
| 12 | 26,23 | 29,13 | 2,90 | Notas que caen + ventana de Claude escribiendo «roteiros originais» | tajo |
| 13 | 29,13 | 31,30 | 2,17 | Ventana «instalar»: botón, «skill» se escribe, barra de progreso, ✓ verde | corte duro |
| 14 | 31,30 | 34,39 | 3,09 | CTA: «COMENTE» + **SKILL** gigante naranja que cae letra a letra, caja de comentarios | corte duro |

- 13 cambios de escena en 34,4 s: **uno cada 2,6 s**. Escena más corta: 1,40 s (#8). Más larga: 4,10 s (#4).
- Dentro de cada escena **siempre pasa algo cada 0,1–0,3 s** (un icono, una letra, una barra). Nunca hay más de ~0,5 s sin movimiento [MEDIDO en mosaicos].
- Subtítulos: 40 bloques, uno cada 0,86 s (salen de leer los mosaicos).

## 3. Transiciones

- **Tajo diagonal** [MEDIDO]: una línea fina y clara (color crema/naranja claro) cruza la pantalla en diagonal, de abajo-izquierda a arriba-derecha, en **2–3 fotogramas** (1,833 → 1,900 s comprobado a 30 fps). Debajo, la escena cambia de golpe. Visto en 1,83, 7,57, 14,13, 16,33, 17,80, 24,57 y 26,23 s (solo 1,83 comprobado a 30 fps; el resto en mosaicos de 15 fps).
- **Corte duro** [MEDIDO]: 5,03 y 11,67 s comprobados a 30 fps; 19,20, 22,13, 29,13 y 31,30 s vistos en mosaicos sin línea.
- `cortes.txt` marcó 7 «dudosos/disolvencia» con puntuación baja (0,08–0,19). Es lógico: el fondo y el personaje no cambian, solo cambia la tarjeta.

## 4. Zoom y encuadre

- No hay cara que medir (`medir.py encuadre` no aplica).
- **Escena 1 más cerca**: suelo en y≈915 y personajes grandes. **De la escena 2 en adelante, la cámara está más lejos**: suelo en y≈1170, personaje más pequeño. El cambio se hace de golpe con el tajo de 1,83 s [MEDIDO en fotogramas 0,600 s y 6,933 s].
- **Crecimiento de tarjetas** [MEDIDO en mosaicos]:
  - 1,93 → 2,13 s: la ventana de Claude crece desde una barra pequeña (~4 fotogramas).
  - 20,13 → 20,40 s: un icono de la red crece hasta ocupar la tarjeta grande (~4 fotogramas).
  - 26,66 → 26,80 s: la ventana de ideas crece.
  - 29,13 → 29,26 s: la ventana «instalar» entra desde arriba-derecha.
- El encuadre no se mueve durante las escenas: no hay zoom lento ni temblor de cámara [SUPOSICIÓN: no lo medí con números, a ojo es fijo].

## 5. Subtítulos [MEDIDO con `medir.py` en 6,933, 13,333, 22,667 y 33,000 s]

- Posición: letra en y **1376–1423** (centro y≈1400, **72,9 %** del alto). Centrado en x=538–539.
- Tamaño: **48 px de alto** (mayúsculas). Ancho según el texto: 416 px («AO MESMO TEMPO») a 761 px («A ESCREVER SUAS PUBLICAÇÕES»).
- Color: blanco **#FBFBFB**.
- Caja: negra **#050505**, y **1357–1446** (90 px de alto), ~28 px de margen a cada lado de la letra (x 304–775 para «AO MESMO TEMPO»). Esquinas un poco redondeadas [SUPOSICIÓN, a ojo].
- Fuente: pixel/bitmap condensada, mayúsculas, con tildes (Ã, Ç, Ê). **No sé el nombre**.
- Palabras por bloque: 2–4. No hay palabra destacada dentro del subtítulo: el destacado va en la palabra clave sobre la tarjeta (regla 7).
- Entrada: cambio de golpe con 1 fotograma en gris (fundido de 1 fotograma). Sin movimiento.

## 6. Textos en pantalla y gráficos

- **HUD de pelea** (solo escena 1): icono de Claude + «CLAUDE» + barra naranja a la izquierda; «INSTAGRAM» + barra rosa + logo a la derecha; y 315–395. La barra de Instagram baja con cada golpe (0,60 → 1,33 s).
- **Palabra clave sobre la tarjeta**: cajita oscura, mayúsculas pixel, 36 px de alto, y 309–344, escrita letra a letra. Ejemplos: «AO MESMO TEMPO» (naranja), «SEU PERFIL» (blanco) → «CRIAÇÃO DE CONTEÚDOS» (naranja), «COMENTÁRIOS» (blanco) → «RESPOSTAS» (naranja), «REELS» (blanco) → «MELHOR DESEMPENHO» (naranja), «IDEIAS» (blanco) → «PARA VOCÊ MODELAR» (naranja). Patrón que veo: **primero lo que es en blanco, luego el beneficio en naranja** [SUPOSICIÓN: interpretación del patrón].
- **Tarjetas**: estilo «interfaz de app en pixel art» (ventana de Claude, móvil de Instagram, lista de comentarios, calendario, rejilla de reels, gráfica). Borde fino, fondo #1E1E1E aprox., detalles en naranja.
- **Texto que se escribe solo** dentro de las tarjetas, en minúsculas monoespaciadas («habilidade», «único agente de IA», «viralização», «roteiros originais», «skill», «guia completo»).
- **CTA final**: «COMENTE» (blanco en caja, y≈300–340) + **«SKILL» gigante** naranja con brillo (y 390–499, 110 px de alto, 457 px de ancho), que cae letra a letra entre 31,73 y 32,13 s, con chispas «+» blancas alrededor. Debajo, caja de comentarios donde se escribe «SKILL» y Claude responde «guia completo». «PRA VOCÊ TESTAR» en naranja bajo la tarjeta.
- **Explosiones**: golpe con silueta blanca del rival + estallido de rayos blancos (0,57, 0,70, 0,93 s); el rival se deshace en partículas (1,0–1,4 s). En 6,9–7,4 s salen chispas naranjas del personaje.

## 7. Color [MEDIDO con píxeles]

- Fondo: **#0D0D11** (arriba) · **#16161A** (medio) · **#1B1B1F** (suelo).
- Acento único: **naranja terracota #BD705C – #CB765D**.
- Texto: blanco **#FBFBFB** sobre caja **#050505**.
- Colores secundarios solo dentro de los gráficos (rosa/morado de Instagram, azul del botón «Follow», verde del ✓).
- Luz cálida de antorchas a los lados.

## 8. Sonido [MEDIDO, limitado]

**No he escuchado el audio.** Lo que sé:

- Sonoridad **−14,1 LUFS**, LRA 1,7 LU (muy parejo, comprimido), pico **−1,9 dBFS**. Fuente: `audio/medidas.txt`.
- Sin silencios por debajo de −45 dB. Casi mono (lateral 39 dB por debajo del central).
- Música: **no** (lo dijo el usuario). En el espectrograma hay una franja fija entre ~215 y ~390 Hz todo el rato; no sé qué es (puede ser un ambiente o un zumbido de fondo) [SUPOSICIÓN].
- **Golpes de sonido** (picos de cambio brusco del espectro, medidos con un script propio; ±0,02 s):

| segundo | fuerza (× mediana) | qué pasa en imagen |
|---|---|---|
| 0,54 | 6,2× | 1.er golpe de la pelea (destello 0,567) |
| 0,69 | 12,4× | 2.º golpe |
| 0,87 | 12,5× | 3.er golpe / Instagram explota |
| 1,74 | 7,8× | tajo → escena 2 |
| 4,97 | 7,3× | corte → escena 3 |
| 7,50 | 10,2× | tajo → escena 4 |
| 11,64 | 6,5× | corte → escena 5 |
| 14,08 | 9,7× | tajo → escena 6 |
| 16,30 | 8,7× | tajo → escena 7 |
| 17,73 | 9,5× | tajo → escena 8 |
| 19,16 | 8,9× | corte → escena 9 |
| 22,11 | 7,8× | corte → escena 10 |
| 24,54 | 9,4× | tajo → escena 11 |
| 26,18 | 8,6× | tajo → escena 12 |
| 29,11 | 7,8× | corte → escena 13 |
| 31,27 | 8,0× | corte → escena 14 (CTA) |

- Conclusión: **cada cambio de escena y cada golpe de la pelea lleva un impacto**, 30–60 ms antes de la imagen. Que sea un «whoosh», un «golpe» o una «explosión» es interpretación mía [SUPOSICIÓN].
- Golpes más suaves (4–6×) en 5,48, 6,54, 7,22, 13,62, 15,13… coinciden con iconos que aparecen o barras que se llenan. Pueden ser «clics» de interfaz o solo consonantes de la voz; no lo sé [SUPOSICIÓN].
- En 3,7–4,3 s se ven líneas tonales horizontales (~1300–1700 Hz) mientras se escribe «único agente»: parece un sonido con tono (¿«ding» o tecleo?) [SUPOSICIÓN].

## 9. Receta para replicar

1. Lienzo 1080×1920 a 30 fps. Fondo fijo de sala oscura (#0D0D11 → #1B1B1F) con un personaje-mascota en el centro (pies en y≈1310).
2. Dividir el guion en **escenas de 1,4–4 s** (media 2,5 s): **una idea = una tarjeta**.
3. Cada escena: la tarjeta (y 360–1045, centrada) **crece en 4 fotogramas** y se rellena con un elemento nuevo cada 0,1–0,3 s.
4. Encima de la tarjeta, la palabra clave escrita letra a letra (blanco para lo que es, naranja para el beneficio).
5. Abajo, subtítulo en MAYÚSCULAS, 2–4 palabras, 48 px, caja negra y 1357–1446. Cambio de golpe al ritmo de la voz (~0,86 s por bloque).
6. Cambio de escena: **alternar tajo diagonal (2–3 fotogramas) y corte duro**. Más o menos la mitad de cada.
7. Poner un **impacto de sonido 1–2 fotogramas antes** de cada cambio de escena y en cada «explosión».
8. Abrir con un **gancho de acción** (pelea de 1,8 s más cerca) y abrir la cámara al pasar a la escena 2.
9. Cerrar con la CTA: palabra gigante en naranja que cae letra a letra con chispas + caja de comentarios.
10. Mezclar la voz a **−14 LUFS**, pico ≤ −1,9 dBFS, sin música.

## 10. Lo que no se pudo determinar

- Nombre de las fuentes (subtítulo pixel condensado; texto de tarjetas monoespaciado). Descritas por lo que se ve.
- Con qué programa está hecha la animación.
- Qué sonidos exactos son (no escuché el audio) y qué es la franja grave constante.
- Los tajos de 7,57 / 14,13 / 16,33 / 17,80 / 24,57 / 26,23 s solo los vi a 15 fps; la duración exacta (2–3 fotogramas) solo está comprobada en el de 1,83 s.
- Si las esquinas de la caja del subtítulo son redondeadas y cuánto.

## 11. Zonas seguras de Instagram

Zona útil: y 260 → 1790; 120 px libres a la derecha desde y 1298.

| elemento | posición en el reel | ¿seguro? | al replicar |
|---|---|---|---|
| HUD de pelea | y 315–395 | sí | igual |
| Palabra clave | y 309–344 | sí (49 px por debajo del límite de arriba) | igual |
| «SKILL» gigante | y 390–499 | sí | igual |
| Tarjetas | y 360–1045, x 58–1021 | sí (están por encima de y 1298, pueden llegar al borde) | igual |
| Personaje | y≈1090–1320 | sí | igual |
| Subtítulo | y 1357–1446, caja hasta x≈947 en el más largo | sí, pero justo: el margen derecho mínimo es 133 px (la regla pide 120) | limitar el subtítulo a **≤ 4 palabras / ≤ 790 px de caja** para no pasar de x 960 |

Nada del reel cae en zona tapada. No hace falta mover nada; solo vigilar el ancho de los subtítulos largos.
