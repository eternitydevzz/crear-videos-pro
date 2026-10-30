# Estilo «Minecraft»

> **Nota del repo:** esta ficha se hizo con el reel descargado y sus archivos de trabajo (`video.mp4`, `Frames/`, `cortes.txt`, `info.txt`, `audio/`, `transcripcion.md` y `ventanas/`). En el repo solo están la ficha y los **mosaicos**: esos archivos se citan como fuente de los datos, pero no se incluyen. Para tenerlos, pasa el link del reel por `/crear-videos-pro:crear-estilo-videos`.

Reel de referencia: https://www.instagram.com/reel/DeIFvoSPh6m/ (cuenta @sebastiankra.ia, sale en la marca de agua).
Ficha hecha el 16-10-2026. **[MEDIDO]** = sale de un fotograma, de ffprobe o de ffmpeg. **[SUPOSICIÓN]** = interpretación mía.
Lo que el usuario quiere replicar: **los motions**. Música: El usuario pidió no hacer nada con ella.

## Resumen: 10 reglas

1. **No hay persona en cámara.** Los 71,4 s son animación pixel-art de estilo Minecraft sobre un cielo nocturno azul marino con estrellas y una franja de hierba. La voz va en off. [MEDIDO]
2. **Un objeto fijo marca el progreso.** Una «MESA DE CRAFTEO» con 3×3 huecos se queda en pantalla de 8,86 s a 59,8 s. Al final de cada sección, el icono de esa pieza entra volando en su hueco. [MEDIDO]
3. **Hay 9 secciones iguales, de 5,3 s de media (4,3–7,1 s).** Cada una abre con un rótulo pequeño dorado «HUECO N DE 9», un título blanco grande y una pastilla de color con un subtítulo corto. [MEDIDO]
4. **Todo entra con un «pop» con rebote.** El título pasa por estos anchos: 60 % → 87 % → 108 % → **111 %** → 105 % → 100 %, en 0,33 s (5 fotogramas a 15/s). [MEDIDO en «EL CUERPO», 14,00–14,33 s]
5. **Cambia algo cada 0,3–0,7 s.** Dentro de cada sección entra un objeto nuevo por cada idea que dice la voz. Nunca hay más de unos 0,7 s sin movimiento. [MEDIDO en los mosaicos]
6. **Subtítulos tipo karaoke de 1 a 3 palabras**, en mayúsculas, centrados en y≈1520 (78,5 % del alto). La palabra que suena va en amarillo `#F8F850`, las ya dichas en blanco y las que faltan en gris `#808088`. [MEDIDO]
7. **Las etiquetas entran algo giradas** (unos −5°) y con pop: «YA EXISTEN», «HACE COSAS», «ESTA VOZ», «UN POCO», «HACE 7 DÍAS». [MEDIDO que están giradas; el ángulo es SUPOSICIÓN, a ojo]
8. **Texto a máquina dentro de cajas negras** con borde blanco, a unos 36 caracteres por segundo (perfil en 28,4–30,6 s; diálogo en 51,5–53,8 s). [MEDIDO: 19 caracteres en 0,53 s]
9. **Hay 3 transiciones fuertes, nada más:** un destello blanco en 3,07 s, un corte a negro en 51,33 s y una disolvencia de 2 fotogramas en 54,23 s. El resto son cambios de contenido sin transición: el fondo y el suelo nunca se cortan. [MEDIDO]
10. **El vídeo se cierra en bucle.** Acaba (68,6 s) con la misma escena del principio: un robot gris picando una piedra «ENTRENAR UNA IA», y el robot «muere» con ojos en X. [MEDIDO]

---

## 1. Datos técnicos [MEDIDO]
- 1088 × 1936 px, 30 fps, 71,40 s.
- Fotogramas analizados: 1071 (uno de cada dos, 15 por segundo).

## 2. Estructura y ritmo [MEDIDO en los mosaicos]

| Inicio | Fin | Dur. | Tipo | Qué pasa |
|---|---|---|---|---|
| 0,00 | 3,66 | 3,66 | Gancho | Robot blanco con pico pica una piedra gris «ENTRENAR UNA IA» con barra «ENTRENANDO…». Título «¿TU PROPIO JARVIS?». A 1,46 entra «DEJA DE PICAR PIEDRA» (pixel, naranja) y a 2,93 «NO SE ENTRENA» con «ENTRENA» tachado en rojo. Destello en 3,06 y el robot muere (ojos X) de 3,13 a 3,6 |
| 3,66 | 5,46 | 1,80 | Giro | Título verde brillante «SE CRAFTEA». La escena anterior se va por la izquierda, la mesa de crafteo cae desde arriba (3,86→3,93) y se abre como ventana con pop (4,00–4,06). Pastilla verde «COMO EN MINECRAFT» a 4,66 |
| 5,46 | 8,86 | 3,40 | Presentación | Título «9 HUECOS». Los números 1–9 entran uno a uno, cada ~0,07–0,13 s (5,5–6,26). Pastilla «9 PIEZAS DE TU JARVIS» (6,33). Los iconos llenan los huecos (6,53–6,86) y un check verde por hueco (7,33–8,0). Etiqueta verde «YA EXISTEN» (7,4). A 8,53–8,86 la mesa se encoge y baja bajo la hierba |
| 8,86 | 14,00 | 5,14 | Hueco 1 | LA CASA: portátil que cae, servidor, «SERVIDOR EN LA NUBE», «ON 24 H» y el fondo pulsa a azul |
| 14,00 | 21,13 | 7,13 | Hueco 2 | EL CUERPO: robot gris que cae, logo Hermes Agent, «0 €», cofre, «</>», «CÓDIGO ABIERTO», bocadillo «bla bla bla», «SOLO HABLA», anillo de escaneo y el robot se enciende (ojos cian), «HACE COSAS», bloques que crecen |
| 21,13 | 26,53 | 5,40 | Hueco 3 | EL CEREBRO: 3 Pokéballs en una repisa, pastilla roja «¡ELIGE TU CEREBRO!». De cada bola sale un logo (Claude, OpenAI, Gemini). El robot cambia de color con un anillo (naranja → morado → naranja) y «Y LO CAMBIAS» |
| 26,53 | 31,33 | 4,80 | Hueco 4 | QUIÉN ERES: dos robots y una caja negra con texto a máquina (TRABAJO / OBJETIVO / GUSTOS) |
| 31,33 | 35,66 | 4,33 | Hueco 5 | MEMORIA: círculo de carga «GUARDANDO…», logo Honcho, bocadillo de pensamiento con check, «HACE 7 DÍAS» |
| 35,66 | 40,60 | 4,94 | Hueco 6 | HABILIDADES: un marco tipo Tetris donde caen bloques de colores; luego «¡HABILIDAD APRENDIDA!» y los bloques se borran |
| 40,60 | 45,26 | 4,66 | Hueco 7 | HERRAMIENTAS: barra de inventario de 9 casillas que se llena con Gmail, Calendar, Docs y Chrome, cada uno con su miniatura |
| 45,26 | 51,33 | 6,07 | Hueco 8 | CANALES: 3 bloques «?» de Mario; el robot salta y los golpea y salen Telegram, WhatsApp y Slack. Logo ElevenLabs, onda de voz y «ESTA VOZ» |
| 51,33 | 54,23 | 2,90 | Huevo de pascua | Corte a negro: corazón rojo pixel y caja de diálogo con avatar pixel del creador, a máquina: «NO LA ESTOY GRABANDO YO. ES MI VOZ CLONADA.» |
| 54,23 | 59,80 | 5,57 | Hueco 9 | LA CARA: cursor que dibuja un anillo HUD cian alrededor del robot, paneles laterales, «CLAUDE DESIGN», caja de código, «UN POCO» |
| 59,80 | 61,40 | 1,60 | Clímax | «9 DE 9» en cian. La mesa sube y crece al centro; la flecha se llena, el resultado brilla con rayos y el robot sale de la mesa (60,86–61,26) |
| 61,40 | 64,60 | 3,20 | Recompensa | «¡MISIÓN CUMPLIDA!» amarillo cursiva + «TU JARVIS», anillo HUD y 3 avisos «¡LOGRO CONSEGUIDO!» que entran por la derecha en 62,13, 63,00 y 63,93 |
| 64,60 | 68,60 | 4,00 | CTA | «COMENTA» + pastilla cian ««IA»» (65,0). Un cofre crece (64,73–64,93), se abre (66,2) y salen libros de colores (66,26–66,8). «RECURSOS GRATUITOS DE IA» (66,93) |
| 68,60 | 71,40 | 2,80 | Cierre en bucle | Vuelve la escena del gancho con el robot gris. «EL RESTO…» + pastilla roja «SIGUE PICANDO PIEDRA» (70,53). El robot muere (70,33) |

- **Cortes de escena:** 17 bloques, uno cada **4,2 s** de media. Los huecos duran entre 4,33 y 7,13 s.
- **Dentro de cada bloque**, el movimiento lo marca la voz: entra un elemento nuevo con cada sustantivo importante.
- De los 25 «dudosos» de `cortes.txt`, los de 5,43, 21,13, 26,50, 31,30, 35,63, 40,57, 45,27, 51,33, 59,77 y 68,57 son **cambios de sección**: cambia el contenido de golpe, pero el fondo, la hierba y la mesa siguen. Los demás son elementos que entran con pop. Esto lo he comprobado leyendo los mosaicos, no con `ventana.sh` a 30 fps.

## 3. Transiciones [MEDIDO]
- **3,07 s** – destello claro de 2 fotogramas: la imagen se aclara a gris azulado, a la vez que el robot muere.
- **3,90 s** – cambio de escena: la piedra y el robot salen por la izquierda y la mesa cae desde arriba. No es una disolvencia de vídeo, aunque `cortes.txt` la marque así.
- **51,33 s** – corte duro a negro.
- **54,23 s** – disolvencia de 2 fotogramas desde el negro a la escena, pasando por un gris claro.
- **Cambios de sección:** el título viejo se va de golpe y el nuevo entra con pop. Los objetos de la sección anterior desaparecen en el mismo fotograma.

## 4. Movimiento, zoom y encuadre [MEDIDO salvo donde se indica]
- **No hay zoom de cámara ni cara.** Los «zooms» son escalados de objetos:
  - La mesa encoge y baja en 8,53–8,86 s (0,33 s).
  - La mesa sube y crece en 59,80–60,06 s.
  - El cofre crece en 64,73–64,93 s.
- **Pop de título:** empieza al ~60 % del tamaño final, pasa al 111 % y se asienta en 100 % en 0,33 s. El «9 HUECOS» hace lo mismo: 403 → 611 px de ancho (pico) → 541 px final, en 5,47–5,87 s.
- **Objetos que caen desde arriba:** portátil (10,06–10,33), robot (14,53–14,66) y mesa (3,86). Al tocar el suelo salen unas rayitas de polvo a los lados.
- **Personajes:** respiran o botan poco a poco. El robot salta para golpear los bloques «?» (47,0–48,6).
- **Anillos HUD cian:** se dibujan como un arco que se cierra (55,6–55,93; 61,33–61,8).
- **Pulso de fondo:** el cielo se aclara a azul `#3A5A9A` aprox. en 12,46–13,4 s, con «ON 24 H». El color del fondo es [SUPOSICIÓN] a ojo.

## 5. Subtítulos [MEDIDO en 22,2 s y 9,6 s]
- **Posición:** centrados en x. Altura de mayúscula **56 px** (y 1493–1548 de 1936, centro en el **78,5 %**).
- **Fuente:** sans-serif muy gruesa, en mayúsculas, sin borde ni caja. No sé el nombre.
- **De 1 a 3 palabras por bloque.** La mayoría tiene 2.
- **Karaoke por palabra:**
  - La palabra que suena, en amarillo `#F8F850`.
  - Las ya dichas, en blanco `#FAFAFA`.
  - Las que faltan, en gris `#808088`.
  - La última palabra del bloque se queda amarilla hasta que cambia el bloque.
  - El bloque nuevo aparece entero en gris unos 0,07 s y luego empieza a iluminarse.
  - La palabra activa **no crece**: no vi cambio de tamaño en los mosaicos. No lo medí píxel a píxel.
- **Siempre hay exactamente una palabra destacada** (la que suena), del mismo tamaño que las demás.
- **Los números van con letra** en el subtítulo («NUEVE HUECOS») y **con cifra** en el título («9 HUECOS», «9 DE 9»).
- **Marca de agua:** avatar redondo + «@sebastiankra.ia» en tipografía monoespaciada gris, centrada en y≈1765.

## 6. Textos en pantalla y gráficos [MEDIDO]
- **Rótulo de sección:** «HUECO N DE 9», pixel-font dorada `#E8C030`, letras muy espaciadas, en y≈125–145.
- **Título:** sans gruesa blanca con sombra oscura. Altura de mayúscula **67 px**, y 176–242. Centrado. Excepciones:
  - «SE CRAFTEA»: verde con brillo.
  - «9 DE 9»: cian.
  - «¡MISIÓN CUMPLIDA!»: amarillo cursiva.
- **Pastilla bajo el título:** rectángulo redondeado con borde claro y texto pixel en blanco, en y≈280–330. Colores vistos:
  - rojo `#781820` («¡ELIGE TU CEREBRO!», «SIGUE PICANDO PIEDRA»)
  - verde («COMO EN MINECRAFT»)
  - azul oscuro con borde cian («9 PIEZAS DE TU JARVIS», «LE ESCRIBES POR EL MÓVIL»)
  - cian (««IA»»)
  - naranja oscuro («CLAUDE DESIGN»)
- **Etiquetas de objeto:** pixel-font pequeña, amarilla/naranja o cian, giradas un poco, con pop.
- **Iconos:** logos reales (Hermes, Claude, OpenAI, Gemini, Honcho, Gmail, Calendar, Docs, Chrome, Telegram, WhatsApp, Slack, ElevenLabs) en tarjetas blancas cuadradas con esquinas redondeadas y su nombre en pixel-font debajo.
- **Referencias a videojuegos** [SUPOSICIÓN por cómo se ven]:
  - Minecraft: mesa, inventario, hierba, «¡LOGRO CONSEGUIDO!»
  - Pokémon: Pokéballs
  - Tetris: bloques que caen
  - Super Mario: bloques «?»
  - Undertale: caja de diálogo con corazón rojo

## 7. Color [MEDIDO, valores redondeados a pasos de 8]
- **Cielo:** degradado de `#081028` (arriba) a `#000810` (abajo), con estrellas blancas sueltas y una rejilla muy tenue.
- **Suelo:** franja de hierba verde pixel con tierra marrón, en y≈1010–1100.
- **Acentos:**
  - amarillo `#F8F850` (palabra activa)
  - dorado `#E8C030` (rótulo de hueco)
  - cian (ojos del robot, HUD, «9 DE 9»)
  - rojo `#781820` (pastillas de alerta)
  - verde (checks, «SE CRAFTEA»)
- **Personaje principal:** robot pixel. Es gris, se vuelve naranja al elegir cerebro y lleva antena cian.

## 8. Sonido [MEDIDO, limitado]
- **Medidas:**
  - Volumen medio −14,3 LUFS, rango 3,3 LU, pico −0,5 dBFS.
  - No hay silencios por debajo de −45 dB.
  - Casi mono: lo lateral queda 41 dB por debajo de lo central.
- **No he escuchado el audio.**
- **Música:** El usuario pidió no hacer nada con ella. En los espectrogramas se ve una banda horizontal continua en ~215–390 Hz durante todo el vídeo, que podría ser un fondo musical. No lo afirmo.
- **Sonidos** (El usuario pidió revisarlos). Todo esto es lectura de espectrogramas, ±0,2 s. En los espectrogramas son líneas horizontales finas en escalera (tonos puros que suben o bajan), un patrón propio de efectos chiptune, tipo 8 bits [SUPOSICIÓN]. Coinciden con estos momentos de la imagen:

| Segundo | Forma en el espectrograma | Qué pasa en la imagen |
|---|---|---|
| 4,0–4,3 | racimo de tonos agudos | se abre la mesa de crafteo |
| 6,6–6,7 | 3 tonos agudos (2,7 / 5 / 10 kHz) | entran las piezas en los huecos |
| 12,4–12,9 | escalera de tonos que sube | «ON 24 H» y pulso azul |
| 15,3–15,6 | barrido que sube | aparece el logo de Hermes |
| 16,6–17,4 | escalera que sube | «0 €», cofre, «</>» |
| 20,0–20,4 | tonos que bajan | el robot se enciende |
| 24,8–25,0 | escalones | el robot cambia de color |
| 27,3–27,6 | barridos diagonales que suben | se abre la caja negra |
| 32,8–33,0 | barrido que sube | logo de Honcho |
| 33,4–34,8 | muchos tonos sostenidos | bocadillo de pensamiento y check |
| 40,0–40,4 | tonos | «¡HABILIDAD APRENDIDA!» |
| 47,3–48,3 | peine regular de armónicos | el robot golpea los bloques «?» |
| 51,5–53,9 | patrón repetido muy regular | texto a máquina del diálogo: parecen pitidos por letra |
| 61,0–61,6 | tonos | sale el robot / «¡MISIÓN CUMPLIDA!» |
| 61,6–63,8 | banda grave fuerte y sostenida (215–390 Hz) | logros: podría ser un acorde de fanfarria [SUPOSICIÓN] |
| 65,0–65,8 | tonos | pastilla «IA» y cofre |

**Regla práctica** [SUPOSICIÓN]: cada pop importante lleva su «blip» corto de 8 bits, y el texto a máquina lleva un pitido por letra.

## 9. Receta para replicar los motions
1. **Lienzo:** 1080×1920, 30 fps. Fondo con degradado `#081028` → `#000810`, estrellas sueltas y una rejilla tenue. Franja de hierba pixel en y≈1000–1090.
2. **Guion en N piezas.** Ponle un objeto que se va llenando y se queda en pantalla todo el vídeo (aquí, la mesa 3×3). Cada sección dura 4,5–7 s y deja su icono en el hueco al terminar.
3. **Plantilla de sección:**
   - Al empezar, entra con pop el rótulo «HUECO N DE 9» + título + pastilla.
   - Con cada idea de la voz, entra un objeto pixel o un logo con pop o cayendo desde arriba.
   - Al terminar, el icono vuela a su hueco.
4. **Pop estándar:** escala 0,6 → 1,11 → 1,0 en 0,33 s (ease-out con rebote). Para objetos que caen: caída rápida y rayitas de polvo al tocar el suelo.
5. **Etiquetas:** pixel-font, giradas unos −5°, con pop.
6. **Karaoke:** 1–3 palabras, centrado en y≈1505 (en 1920). Palabra activa en amarillo `#F8F850`, dichas en blanco, pendientes en gris `#808088`.
7. **Cajas de texto a máquina:** a ~36 caracteres por segundo, para listas o datos.
8. **Ritmo:** algo nuevo cada 0,3–0,7 s. Ningún tramo quieto de más de 0,7 s.
9. **Gancho y cierre con la misma escena:** el gancho muestra el problema («picar piedra»), con un destello y la «muerte» del personaje. El cierre vuelve a esa escena para hacer el bucle.
10. **Clímax:** la pieza final completa, con brillo y rayos, «¡MISIÓN CUMPLIDA!» y avisos de logro que entran por la derecha.
11. **CTA:** palabra clave en pastilla cian y un cofre que se abre.

## 10. Lo que no se pudo determinar
- **Nombres de las fuentes:** la sans gruesa de subtítulos y títulos, la pixel-font de etiquetas y la monoespaciada de la marca de agua. Solo las describo.
- **Con qué programa se hizo** (After Effects, código, una app…): no se puede saber.
- **Si hay música y qué sonidos exactos son:** no he escuchado el audio.
- **El ángulo exacto de las etiquetas giradas y los colores del pulso azul:** a ojo, no medidos.
- **Qué es el cuadrado claro de arriba a la derecha** (x 976–1057, y 31–112): se ve en casi todo el vídeo. Puede ser un icono de la propia grabación.
- **Los cambios dudosos de `cortes.txt`:** no los miré a 30 fps uno a uno; los clasifiqué con los mosaicos a 15 fps.

## 11. Zonas seguras de Instagram
Medidas en 1080×1920: el reel mide 1088×1936, así que multiplico por 0,992. Zona libre: y 260 → 1790; 120 px libres a la derecha por debajo de y 1298.

| Elemento | Posición en el reel (1920) | ¿Seguro? | Posición al replicar |
|---|---|---|---|
| «HUECO N DE 9» | y≈124–144 | **NO** (tapado por arriba) | y≈275–295 |
| Título de sección | y≈175–240 | **NO** | y≈310–377 |
| Pastilla bajo el título | y≈278–328 | sí, pero hay que bajarla porque sube el título | y≈405–455 |
| Cuadrado de arriba a la derecha | y≈31–111 | **NO** | no lo copio |
| Escena (objetos, robot) | y≈350–1000 | sí | bajar ~120 px solo si choca con la pastilla; **no encoger** |
| Mesa de crafteo | y≈1030–1385, x hasta ~873 | sí (no llega a x 960) | igual |
| Subtítulos | y≈1480–1535 | sí | igual (y≈1505) |
| Marca de agua | y≈1750 | sí, justo (límite 1790) | igual o subir a ~1730 |

Que el bloque de arriba quepa sin chocar con los objetos es [SUPOSICIÓN]. Hay que comprobarlo dibujando las zonas sobre fotogramas del render.
