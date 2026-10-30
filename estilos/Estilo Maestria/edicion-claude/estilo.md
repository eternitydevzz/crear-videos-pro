# estilo.md — Estilo «Edición Claude» (v2)

**Estado:** aprobado (9,5/10) después de 7 pasadas.
**Vídeo de referencia:** `Edición Claude 1 - pasada 7.mp4` (esta carpeta). **Proyecto que lo genera:** `proyecto/build.py` → `index.html` + `compositions/*.html` (HyperFrames 0.8.114).
**Origen:** parte del reel de referencia analizado en el **Anexo A** (abajo, sin cambios) y suma todo lo que el presentador decidió en 7 pasadas.

Cómo se obtuvo cada dato:
- **[MEDIDO]**: sale del MP4 final o de pistas separadas con ffmpeg.
- **[CÓDIGO]**: valor exacto en `build.py` o `index.html`.
- **[DECISIÓN]**: lo pidió el presentador.
- **[SUPOSICIÓN]**: no comprobado.

---

## 0. El estilo en 12 reglas
1. Vertical **1080×1920 a 30 fps**, unos 37 s. El presentador habla a cámara y se alterna con **gráficos de interfaz sobre fondo claro**.
2. **Un cambio de plano cada 1,9 s de media**. Los planos del presentador (A-roll) duran como mucho unos 2,5 s y los gráficos **3 s como máximo** [DECISIÓN].
3. Los silencios de más de 0,3 s se **cortan**, dejando 0,05 s a cada lado.
4. Cada gráfico **ilustra literalmente lo que se dice** en ese momento, y cada elemento aparece **justo con su palabra**.
5. Las animaciones **arrancan 0,1 s antes** de la palabra, y los cortes de escena **2 fotogramas antes** de la palabra que los dispara.
6. Subtítulos **palabra a palabra**, con **1 palabra destacada por frase en MAYÚSCULAS a 132 px** [DECISIÓN].
7. Sobre A-roll, los subtítulos van **debajo de la barbilla** (y = 1090) [DECISIÓN]. Sobre gráficos van **abajo, sin bajar de 1535 px**. En las escenas con pastilla de título van **124 px debajo del contenido**.
8. Paleta: **fondo #F5F6F8 + tinta #101010 + azul #0050E0**. Naranja Claude solo en el logo. Tarjetas blancas con sombra suave.
9. Títulos de escena en **pastilla con borde azul**, MAYÚSCULAS en Spline Mono y dos tonos (azul oscuro #14256B + azul #0050E0) [DECISIÓN].
10. Música de fondo que **baja sola bajo la voz** (*carve*), unos 16 dB por debajo de ella. Entre 20 y 25 efectos en 37 s, todos anclados a una palabra o a la entrada de una escena.
11. **Volumen final con ganancia fija + limitador**. Nunca usar `loudnorm` dinámico, porque borra los volúmenes que fijó el presentador (ver §9).
12. Todo lo importante va **dentro de la zona segura de Instagram** (ver §8).

---

## 1. Formato y entrega [MEDIDO]
- 1080×1920, 30 fps, H.264, **37,40 s**, audio AAC 48 kHz a 256 kbps.
- Sonoridad final **-15,9 LUFS integrado, pico -2,0 dBFS**.
- Nombre del archivo: `<título> - pasada N.mp4`, en la carpeta del vídeo. Cada pasada se entrega entera para que el presentador la vea.

## 2. Flujo de trabajo (en este orden)
1. **Guion:** el texto de los subtítulos es **el guion del presentador, palabra por palabra** [DECISIÓN]. Whisper solo sirve para los **tiempos**. Si el audio dice algo que no está en el guion (aquí «Si no quieres perderte»), se le pregunta al presentador.
2. **Corte de silencios:** `silencedetect=noise=-30dB:d=0.3`, dejando 0,05 s de margen a cada lado y un fundido de 0,01 s en cada unión. Resultado de este vídeo: 13 silencios quitados, de 42,04 a **36,93 s** [MEDIDO].
3. **Transcripción con tiempos por palabra**, sobre el vídeo ya cortado:
   `whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-small.bin -l es -ojf -dtw small -nfa`
   - `-nfa` es obligatorio: sin él, DTW devuelve -1 en todos los tiempos.
   - **Regla de tiempos validada** [MEDIDO]:
     - Primera palabra después de cada corte: usar `offsets` (error medio ±0,05 s en 12 cortes).
     - Resto de palabras: usar `t_dtw − 0,14 s`. Los `offsets` se desvían hasta 0,5 s en frases largas; DTW coincide con los huecos de energía de la voz (consonantes «p», «g», «k»).
     - Palabras que Whisper pega: se separan con los tokens DTW.
   - Ortografía: se corrigen las tildes del guion (vídeo, editó, estás, aún, tipografías, Haré, cómo) [DECISIÓN].
4. **Plan de escenas:** tabla con los planos de A-roll y los gráficos, cada corte anclado a una palabra. Se le enseña al presentador antes de construir.
5. **Primera pasada completa** y, después, ajustes por rondas. Antes de cambiar algo visual, se le enseña **un fotograma** al presentador [DECISIÓN].

## 3. Estructura y ritmo (vídeo final) [MEDIDO + CÓDIGO]
- 21 planos: **9 de A-roll** (12,98 s, el 35 %, media 1,44 s, entre 0,55 y 2,56 s) y **12 gráficos** (24,42 s, el 65 %, media 2,03 s, entre 1,17 y 2,92 s).
- 20 cambios en 37,4 s, **uno cada 1,87 s**.
- Al detectar los cortes en el MP4 final, 18 de 20 coinciden con el plan con un error de ±0,03 s. Los 2 que no detecta (18,48 y 35,56) son transiciones con desenfoque, no cortes secos.

| # | Inicio | Dur. | Tipo | Se dice | Qué se ve |
|---|---|---|---|---|---|
| 1 | 0,00 | 2,80 | G | «Este vídeo… lo guionizó Claude, lo editó Claude» | Pastilla «VÍDEO HECHO **100% CON AI**» parpadeando · móvil con tu vídeo dentro + «REC» · chips «✓ GUION ✻» y «✓ EDICIÓN ✻» |
| 2 | 2,80 | 1,80 | A 116 % | «y ni siquiera soy yo, porque adivina» | — |
| 3 | 4,60 | 1,72 | G | «Es un clon que también hizo Claude» | Tarjeta con tu vídeo, escáner azul + rejilla, se divide en 3 · pastilla «Clon IA hecho con ✻ Claude» |
| 4 | 6,32 | 2,06 | A 100 % | «Y es que ya no tienes excusa» | — |
| 5 | 8,38 | 2,92 | G | «el AI te hace todo, te guioniza, te clona, te edita y te sube» | Pastilla «EL AI TE HACE **TODO**» · 4 tarjetas Guioniza/Clona/Edita/Sube que se marcan ✓ con cada palabra · barra lateral que se llena |
| 6 | 11,30 | 0,55 | A 116 % | «el contenido» | — |
| 7 | 11,85 | 1,99 | G | «Y no, no soy diseñador, ni programador» | Tarjetas «Diseñador» y «Programador» tachadas en rojo + ✕ + temblor |
| 8 | 13,84 | 2,56 | A 116 % | «y aún así pude lograr resultados como los que estás viendo ahora» | — |
| 9 | 16,40 | 2,08 | G | «Puedes cambiar las tipografías, los colores» | «Aa» que cambia de fuente cada 0,13 s · paleta de 5 colores · «Aa» cambia de color cada 0,09 s |
| 10 | 18,48 | 1,47 | G | «incluso añadir motion graphics» | Anillo que se expande · 8 formas que estallan desde el centro · «MOTION» letra a letra + «graphics» en serif cursiva |
| 11 | 19,95 | 1,31 | A 100 % | «No me costó nada» | — |
| 12 | 21,26 | 2,07 | G | «porque todo lo hizo con código» | Terminal oscuro que escribe letra a letra con el logo de Claude · chip «✻ todo con *código*» |
| 13 | 23,33 | 2,09 | G | «reels, anuncios, YouTube» | 3 tarjetas que entran desde 3 lados: logo Instagram «Reels», megáfono «Anuncios», logo YouTube |
| 14 | 25,42 | 1,53 | A 116 % | «tu app, tu negocio, lo que quieras» | — |
| 15 | 26,95 | 1,97 | G | «vender este servicio a empresas» | Tarjeta «Propuesta: Vídeos con IA *para tu marca*» + botón Enviar · línea discontinua · 3 tarjetas «Empresa» con ✓ verde |
| 16 | 28,92 | 1,20 | A 100 % | «como hacen nuestros alumnos» | — |
| 17 | 30,12 | 1,17 | G | «y ganar miles todos los meses» | Gráfico de 5 barras ENE–MAY «+$» · «*miles*, cada mes» |
| 18 | 31,29 | 1,19 | A 116 % | «Haré una clase en vivo» | Insignia roja «● EN VIVO» (y = 1420) con el punto latiendo |
| 19 | 32,48 | 2,30 | G | «crear y escalar tu agencia AI a $10K al mes» | Gráfica de línea que sube · en «$10K» la gráfica se difumina y entra «$10K» gigante en azul + rayos + temblor + «*al mes*» |
| 20 | 34,78 | 0,78 | A 100 % | «Si no quieres perderte» | — |
| 21 | 35,56 | 1,84 | G azul | «comenta YO y te doy acceso» | Fondo azul · «*Comenta*» serif · «YO» gigante blanco · burbuja de comentario «tú · ahora: YO ♥» · fundido a negro de 0,3 s |

## 4. A-roll (el presentador a cámara) [CÓDIGO]
- Vídeo a pantalla completa (`object-fit: cover`). La voz va en una pista separada y continua, y el vídeo va mudo.
- **Dos encuadres alternos:** 100 % y **116 %**. Escalan desde el **borde superior** (`transform-origin: 50% 0%`), para que la cara no suba hacia los subtítulos.
- **Empuje lento dentro de cada plano:** de ×z a ×(z + 0,04) durante todo el plano, lineal.
- Corte seco entre plano y gráfico. El gráfico entra con su propia animación (ver §6, SCENE_IN).

## 5. Gráficos (diseño) [CÓDIGO]
### 5.1 Fondo y materiales
- **Fondo** #F5F6F8 con **cuadrícula** de 72 px (líneas de 2 px en rgba(16,16,16,.045)).
- **Dos brillos radiales azules**, rgba(0,80,224,.20) → transparente: uno de 1000 px arriba a la izquierda (−380, −380) y otro de 1100 px abajo a la derecha (−420, −200).
- **Tarjetas:** blancas, radio 36 px, sombra `0 30px 80px rgba(16,24,40,.14), 0 4px 14px rgba(16,24,40,.06)`.
- **Cierre:** fondo azul radial (#2f74ff → #0050E0 → #0038a8) y texto blanco.

### 5.2 Paleta
| Uso | Color |
|---|---|
| Fondo | #F5F6F8 |
| Texto / tinta | #101010 |
| Acento (destacadas, checks, líneas) | **#0050E0** |
| Parte oscura de la pastilla de título | #14256B |
| Logo Claude / avatar | #D97757 |
| Tachados, ✕, EN VIVO | #E5484D |
| Confirmación (✓ empresas) | #16A34A |
| Terminal | #111827 (barra #1c2333) |
| Texto secundario | #5b6170 / #6b7280 (contraste ≥ 3:1) |

### 5.3 Tipografías (en `assets/fonts`, declaradas con @font-face en **cada** escena)
- **Hanken Grotesk 500/700:** subtítulos, títulos de tarjeta y cifras.
- **Spline Sans Mono 500:** etiquetas, pastillas de título y terminal (MAYÚSCULAS y espaciado amplio).
- **Newsreader 500 cursiva, en azul:** palabras de acento dentro de los gráficos (*graphics*, *código*, *miles*, *al mes*, *Comenta*, *para tu marca*).
- **No cambiar la tipografía de un elemento sin preguntar al presentador** [DECISIÓN].

### 5.4 Pastilla de título (según la maqueta del presentador) [DECISIÓN + CÓDIGO]
- Centrada horizontalmente, **top 252 px**, padding 14×40 px, **borde 4 px #0050E0**, radio completo, fondo rgba(255,255,255,.92), sombra `0 14px 34px rgba(0,80,224,.14)`.
- Spline Mono **44 px**, espaciado de letras 5 px, en MAYÚSCULAS. Primera parte en #14256B y parte final en #0050E0: «VÍDEO HECHO **100% CON AI**», «EL AI TE HACE **TODO**».
- En la escena 1 **parpadea durante toda la escena**: encendido y apagado cada 0,17 s, 16 cambios [DECISIÓN].
- **Espacios fijos:** el contenido empieza en **y = 421** y el subtítulo **124 px debajo** del contenido. Escena 1: móvil de 437×815 px (top 421), subtítulo en 1360, chips GUION (120, 629) y EDICIÓN (675, 985). Escena de pasos: tarjetas de 780×190 px cada 235 px desde 421, subtítulo en 1440.

### 5.5 Logos
- Claude: SVG oficial en naranja #D97757 (`assets/logos/claude.svg`).
- Instagram y YouTube: dibujados en SVG con su forma y colores.
- Aparecen **cuando se nombra la marca** [DECISIÓN].

## 6. Animaciones [CÓDIGO]
Todo con GSAP, posiciones redondeadas al fotograma (1/30 s). Sin azar ni relojes.

| Nombre | Desde | Hasta | Duración / curva | Uso |
|---|---|---|---|---|
| **SCENE_IN** | escala 1,12, desenfoque 18 px, opacidad 0,2 | 1 / 0 / 1 | 0,22 s `power3.out` | Entrada de casi todos los gráficos |
| **IN** | y +90 px, escala 0,92, desenfoque 14 px, opacidad 0 | posición final | 0,32 s `power3.out` | Tarjetas, textos, terminal (admite x, giro o y propios) |
| **POP** | escala 0, giro −12° | escala 1, giro final | 0,30 s `back.out(2.4)` | Chips, ✓, ✕, insignias, puntos |
| Check de lista | círculo gris → relleno azul + ✓ con `back.out(3)` | | 0,08 s + 0,22 s | Con su palabra; la tarjeta se desplaza 26 px a la derecha y vuelve |
| Tachado | línea roja escala X 0 → 1 | | 0,14 s `power3.out` + ✕ POP + temblor ±18 px (4 × 0,05 s) | «Diseñador / Programador» |
| Golpe de cifra | escala 2,4 → 1 | | 0,28 s `back.out(1.8)` + rayos 0,3 → 1,5 + temblor ±14 px | «$10K» |
| Escritura | texto carácter a carácter | | 0,5 s la primera línea, 0,16 s las demás + cursor que parpadea cada 0,16 s | Terminal |
| Parpadeo | opacidad 1 ↔ 0 | | cada 0,17 s | Pastilla de la escena 1 |
| Empuje A-roll | ×z → ×(z + 0,04) | | todo el plano, lineal | A-roll |
| Fundido final | negro de 0 a 1 | | 0,30 s | Últimos 0,3 s |

**Sincronía** [CÓDIGO + DECISIÓN]:
- Cada animación ligada a una palabra empieza **0,10 s antes** (`LEAD`), para que esté visible justo cuando suena.
- Cada corte de escena entra **0,06 s (2 fotogramas) antes** de su palabra (`PRE`).
- Comprobado con fotos tomadas 0,1 s después de 14 palabras clave: en todas, la animación ya está visible [MEDIDO].

## 7. Subtítulos [CÓDIGO + DECISIÓN]
- **Trozos de 2 a 7 palabras** (36 trozos para 150 palabras, media 4,2), cortados por sentido. Un trozo aparece cuando suena su primera palabra y se apaga en 2 fotogramas justo antes del siguiente.
- **Cada palabra aparece cuando suena:** desenfoque 10 px → 0, y +14 px → 0, opacidad 0 → 1, en 0,12 s `power2.out`.
- **1 destacada por trozo** (36 en 37,4 s, una cada 1,04 s):
  - Va en su propia línea, en **MAYÚSCULAS**, a **132 px**, con interlineado 1,05 y espaciado de letras −4 px.
  - Entra con escala 0,7 → 1 y desenfoque 14 → 0, en 0,16 s `back.out(2.5)`.
  - **Mismo tamaño para todas, sin reducir las largas** [DECISIÓN]. Ojo: «PROGRAMADOR» mide 944 px y ocupa casi todo el ancho.
- **Línea normal:** Hanken 700, 46 px, interlineado 1,25, separación entre palabras 14 px, centrada, caja de x 90 a 990.
- **Color:**
  - Sobre A-roll: blanco con sombra `0 4px 24px rgba(0,0,0,.55)`.
  - Sobre gráfico claro: #101010, con la destacada en #0050E0.
  - Sobre el azul final: blanco.
- **Posición:**

| Dónde | Ancla | Por qué |
|---|---|---|
| A-roll | **parte superior en y = 1090**, crece hacia abajo | Debajo de la barbilla. La barbilla está en y ≈ 830–870 del original y llega a ≈ 1045 con el 116–120 % [MEDIDO, DECISIÓN] |
| Gráficos | **parte inferior en y = 1535**, crece hacia arriba | Límite de la zona segura de Instagram |
| Escenas con pastilla | parte superior a **124 px** del contenido (1360 / 1440) | Maqueta del presentador |

## 8. Zona segura de Instagram [DECISIÓN, plantilla del presentador]
- Nada importante por encima de **250 px** ni por debajo de **1535 px**. Márgenes: 70 px a la izquierda y 55 px a la derecha.
- Por debajo de **y = 1110**, la columna de iconos ocupa **193 px** a la derecha, así que el texto centrado solo puede medir **694 px**.
- Los bloques se centran **dentro de la zona segura** (el centro está en y ≈ 892), no en la pantalla completa.
- El presentador aceptó que en las escenas con pastilla el subtítulo baje un poco más (hasta y ≈ 1615–1695 en las frases de 3 líneas).

## 9. Sonido [MEDIDO + CÓDIGO]
### 9.1 Pistas
| Pista | Archivo / ajuste | Nivel medido en el final |
|---|---|---|
| Voz | `voz.m4a` (sacada del vídeo cortado; en bruto -24,9 LUFS), volumen 1 | — |
| Música | **«Central Cee – Doja (Instrumental)» desde el segundo 0, sin recortar** [DECISIÓN]. El beat sube solo en 15,25 s (de -42 a -3 dB). Volumen 0,30 | Sola: -34,7 LUFS. Intro -46,0 dB RMS, con beat bajo la voz -33,3, sin voz al final -29,1. **Unos 16 dB por debajo de la voz** |
| Efectos | 24, ver tabla 9.3 | Pista sola: -29,0 LUFS (mono) |

### 9.2 Bajada de la música bajo la voz (*carve* de HyperFrames, fuerza 0,8)
- 6 bandas centradas en 160, 250, 400, 1000, **1600** y 2500 Hz, con q 2,06: −7,4 dB cada una y **−14,8 dB en 1600 Hz**.
- Curva de nivel de 2.397 puntos, que baja hasta **−19,2 dB** cuando habla el presentador.
- Comando: `node <plugin>/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed musica --voice voz`. `build.py` lo ejecuta en cada regeneración.

### 9.3 Efectos (volumen FINAL en `data-volume`, ya con el −50 % aplicado) [CÓDIGO + DECISIÓN]
| s | Efecto | Vol. | Ligado a | Origen |
|---|---|---|---|---|
| 0,00 | Riser (8,07 s, completo) | 0,19 | inicio | `Editar video 1/sfx/Riser.mp3` [DECISIÓN] |
| 1,00 | Wow (2,60 s) | 0,18 | — | `sfx/Wow.wav` [DECISIÓN] |
| 1,34 | pop | 0,28 | «guionizó» (chip GUION) | launches/pr-to-video |
| 2,26 | pop | 0,28 | «editó» (chip EDICIÓN) | ídem |
| 4,64 | scan-scifi-reveal (suena 5,3 s) | 0,08 | entrada del clon | launches/cloud-render/candidates |
| 8,33 | swish | 0,24 | entrada de los pasos | pr-to-video |
| 9,24 · 9,86 · 10,32 | click ×3 | 0,22 | «guioniza» · «clona» · «edita» | pr-to-video |
| 11,10 | ux-chime | 0,24 | «sube» | pr-to-video |
| 12,62 | whoosh-slide | 0,23 | «diseñador» (tachado) | pr-to-video |
| 13,46 | impacto | 0,08 | «programador» (tachado) | `sfx/impacto` |
| 16,35 | whoosh | 0,24 | entrada de las tipografías | `sfx/whoosh` |
| 17,77 | sparkle-twinkle | 0,05 | «colores» | cloud-render/candidates |
| 18,48 | despegue | 0,13 | entrada de motion graphics | `sfx/despegue` |
| 21,46 | type-short | 0,24 | terminal | pr-to-video |
| 23,48 · 23,74 | pop ×2 | 0,28 | «reels» · «anuncios» | pr-to-video |
| 24,40 | whoosh-morph | 0,24 | «YouTube» | pr-to-video |
| 28,66 | success | 0,05 | «empresas» | pr-to-video |
| 30,12 | subida | 0,10 | entrada de las barras | `sfx/subida` |
| 31,90 | ding | 0,15 | «vivo» | `sfx/ding` |
| 34,26 | ding | 0,15 | «$10K» (sustituye al bass-drop) | `sfx/ding` |
| 36,00 | chime | 0,14 | «YO» | pr-to-video |

Todos están copiados y clasificados en `stock completo/sonidos/`. El origen exacto de cada uno está en `stock completo/_origen.txt`.

**Cómo se llegó a estos volúmenes:**
1. El presentador los fijó uno a uno (riser 38, wow 36, clicks 44…).
2. Se eliminó el riser-build y el bass-drop de «$10K» se cambió por un ding [DECISIÓN].
3. Después se bajaron **todos a la mitad (−6 dB)**, porque seguía oyéndolos fuertes, y así los aprobó: «los sonidos ya están bien» [DECISIÓN].

**Dato medido:** aun así, los pops y el wow tienen picos de unos −3,6 dB, al nivel de la voz. Los efectos cortos vienen muy calientes de origen. El presentador aprobó este nivel.

### 9.4 Volumen final (OBLIGATORIO hacerlo así)
`ffmpeg -i render.mp4 -c:v copy -af "volume=8.8dB,alimiter=limit=0.79:attack=5:release=50:level=false" -ar 48000 -c:a aac -b:a 256k salida.mp4`
- Es una ganancia **fija** de +8,8 dB, calculada para que la voz suene igual en todas las pasadas, más un limitador a ≈ −2 dB.
- **No usar `loudnorm`.** Aunque se le pida `linear=true`, se cambia solo a modo `dynamic`, comprime la mezcla y anula los volúmenes que fija el presentador. Ese fue el motivo de «lo siento igual» en las pasadas 3 y 4.

## 10. Preferencias del presentador (aplicar siempre)
- El guion manda sobre Whisper. Si el audio no coincide con el guion, preguntarle.
- Gráficos de 3 s como máximo y muchos cambios de plano: «súper dinámico, que se sienta súper pro».
- Unos 20 efectos en 37 s. Que se repitan no es problema.
- Logos solo cuando se nombra la marca. Signo **$** cuando se habla de dinero. El CTA en mayúsculas.
- Subtítulos debajo de la barbilla, nunca encima de la cara.
- Destacadas en MAYÚSCULAS a un único tamaño.
- No cambiar tipografías ni tamaños sin preguntar.
- Respetar su plantilla de zona segura y sus maquetas (espacios, bordes, tamaños).
- Antes de cambiar un diseño, enseñarle **un fotograma** y esperar su visto bueno.
- Elige él la música. La canción va **sin recortar**.
- **Cambio concreto = render solo de ese tramo** (p. ej. «cambia los primeros 3 s» → se renderizan y entregan solo esos segundos). El vídeo entero solo cuando lo pida o en la entrega final [DECISIÓN, 2026-10-15].

## 11. Errores que no hay que repetir (pasaron en este vídeo)
1. Buscar recursos en una sola carpeta. Siempre revisar todas, incluido `~/.cache`, donde estaba el modelo de Whisper.
2. Fiarse de los `offsets` de whisper.cpp en frases largas: llegaron a ir 0,3–0,6 s tarde y las animaciones salieron tarde.
3. `wt("YO")` sin distinguir mayúsculas encontró el primer «yo» del vídeo. Buscar palabras repetidas por aparición exacta.
4. Usar nombres de clase de la página principal (`.word`, `.av`) dentro de las escenas. Chocaron y ocultaron «MOTION» y el avatar.
5. Quitar el límite de duración de los efectos para meter el riser largo. El scan-scifi pasó a sonar 5,3 s.
6. Normalizar con `loudnorm` (ver §9.4).
7. Subtítulos en el centro vertical de la pantalla: tapaban la boca en los planos al 116 %.

## 12. Lo que NO está verificado o quedó pendiente
- El sonido no lo he escuchado yo. Los niveles están medidos; lo que suena bien lo validó el presentador de oído.
- «guionizó / Claude» al inicio y «$10K» tienen un margen de ±0,2 s (los métodos no coincidían; se eligió con la energía de la voz y DTW).
- «PROGRAMADOR» pasa por debajo de la columna de iconos de Instagram (944 px > 694 px).
- El scan-scifi suena 5,3 s (a volumen 0,08).
- El plano de A-roll 4 dura 2,56 s, un poco más de los 2,5 de la regla.
- Las ~120 escenas de motion de `stock completo/motion/` no se usaron todavía.
- Contraste de la etiqueta «REC» del móvil: 2,3:1, por debajo de 3:1 (aviso de HyperFrames).

## 13. Archivos
- `proyecto/build.py`: genera todo. Los tiempos salen de `proyecto/assets/palabras.json`.
- `trabajo/`: guion final, transcripciones (`cortado_dtw.json`), tramos del corte de silencios y vídeo cortado.
- `stock completo/`: 842 recursos copiados y clasificados (sonidos, música, motion, plantillas, logos, fuentes).

---

# Anexo A — Análisis del reel de referencia (original, sin cambios)

## estilo.md — reel DeCFKLUsQPM (tutorial "editar vídeo con Claude + Remotion")

Fuente: https://www.instagram.com/reel/DeCFKLUsQPM/ · analizado con ffmpeg 9.0.2 sobre el .mp4 descargado.
Todo lo medido sale de 427 fotogramas a 10 fps (cada 3.er frame real), fotogramas a 30 fps en puntos clave, puntuación de escena de ffmpeg y el audio. Lo no medido va marcado **[SUPOSICIÓN]**.

### 1. Datos técnicos (medidos)
- 720×1280 (9:16), 30 fps, H.264 ~883 kbps, **42,70 s**, audio AAC 44,1 kHz estéreo.

### 2. Estructura y ritmo de cortes (medido)
Alterna **A-roll** (él hablando a cámara, plano vertical fijo) y **gráficos** (fondo claro con animaciones). Sin saltos dentro del A-roll: cada toma es continua.

| # | Tiempo (s) | Tipo | Duración |
|---|---|---|---|
| 1 | 0,00–3,20 | Gráficos intro (tarjetas; 1,4 / 2,0 / 2,43 cambian de tarjeta; la tarjeta con su vídeo crece a pantalla completa 3,0–3,27) | 3,20 |
| 2 | 3,20–5,43 | A-roll | 2,23 |
| 3 | 5,43–6,80 | Gráfico ("2 pasos") | 1,37 |
| 4 | 6,80–8,43 | A-roll | 1,63 |
| 5 | 8,43–10,43 | Gráfico (móvil) | 2,00 |
| 6 | 10,43–12,47 | A-roll | 2,03 |
| 7 | 12,47–23,30 | Gráficos (3 escenas: 12,47 / 14,47 / 20,10) | 10,83 |
| 8 | 23,30–24,10 | A-roll | 0,80 |
| 9 | 24,10–26,97 | Gráfico (tipografía/colores) | 2,87 |
| 10 | 26,97–29,40 | A-roll | 2,43 |
| 11 | 29,40–32,07 | Gráfico (Remotion/terminal) | 2,67 |
| 12 | 32,07–34,30 | A-roll | 2,23 |
| 13 | 34,30–37,63 | Gráfico (versiones v1-v3) | 3,33 |
| 14 | 37,63–38,77 | A-roll | 1,13 |
| 15 | 38,77–41,90 | Gráfico (SKILL.md) | 3,13 |
| 16 | 41,90–42,70 | A-roll + fundido a negro final | 0,80 |

- Cambios A-roll↔gráfico: **14** en 42,7 s (1 cada 3,05 s). Contando también cambios entre gráficos (1,4 / 2,0 / 2,43 / 14,47 / 20,10): **19** (1 cada 2,2 s).
- A-roll: 8 tomas, 0,80–2,43 s, media 1,66 s (31 % del tiempo). Gráficos: 69 %, tramo más largo 10,83 s.
- Ninguna toma de A-roll pasa de 2,5 s.

### 3. Transiciones (medido, puntuación de escena de ffmpeg)
- **Corte duro** (puntuación ≥0,98): 5,43 · 6,80 · 12,47 · 23,30 · 24,10 · 26,97 · 29,40 · 37,63 · 38,77 (9).
- **Disolvencia corta de 3 fotogramas (0,10 s)**: 8,43 · 10,43 · 32,07 · 34,30 · 41,90 (5). Se ve la mezcla de ambas imágenes a 30 fps.
- **Cambio entre gráficos** (14,43→14,47): el gráfico anterior desaparece en 2 fotogramas; el nuevo entra con animación propia (logo con desenfoque→nítido ~0,07 s; caja de texto sube con fundido ~0,2 s).
- **Final**: fundido a negro de ~0,3 s (42,4–42,7).

### 4. Zoom / encuadre
- **Crecer tarjeta a pantalla completa (3,00–3,27 s)**: tarjeta con esquinas redondeadas, ~33 % del ancho a 3,00 s, llena el cuadro a ~3,27 s (≈8 fotogramas, 0,27 s). Fondo pasa de claro a la sala.
- **Dos escalas de A-roll** (ancho de caja de piel, percentil 5–95 %): 252–256 px en las tomas de 3,4 / 6,9 / 23,4 / 32,3 / 42,1 s; **292 px** (+16 %) en 10,6 / 27,1 / 37,8 s. Es decir, hay tomas con ~1,16× de acercamiento. Medida aproximada, no es detección de cara.
- Sin zoom progresivo dentro de las tomas (de 4,2 s y 28,0 s comprobado fotograma a fotograma: no hay corte ni zoom).

### 5. Subtítulos (medido, con límites)
- **Una frase a la vez, construida palabra a palabra**: cada palabra nueva aparece cada ~0,1–0,3 s. Bloque de **2–6 palabras** visibles (máx. visto: "también está editado con IA", 5 palabras). Al terminar la frase, todo el bloque se desvanece (~0,1–0,2 s) y empieza otro.
- **Palabra destacada: 1 por frase**, ~**30 en 42,7 s** (una cada ~1,4 s). Ejemplos y segundo de entrada: editado 0,7 · IA 3,9 · primero 7,0 · edición 9,5 · creador 11,6 · guárdate 13,3 · pegar 15,0 · estilos 20,5 · ritmo 21,2 · textos 21,6 · colores 22,3 · branding 26,2 · pídeselo 27,7 · instalar 30,5 · exactamente 33,8 · gusta 37,3 · skill 39,8 · replicar 40,7 · nada 42,2.
- **Animación de entrada (palabra normal y destacada)**: primer fotograma desenfocado y pálido, el siguiente (0,1 s) nítido: **desenfoque + fundido ≈ 0,1–0,2 s**. La destacada va en su propia línea (el texto anterior queda arriba, el posterior debajo).
- **Posición**: centrado horizontal (centro x = 353–358 de 720). Sobre A-roll, **arriba**: primera línea a y≈112–150 (9–12 % del alto). Sobre gráficos: **abajo** (y≈916–1060, 72–83 %) o **arriba** (y≈180–250) cuando el gráfico ocupa la parte baja.
- **Ancho**: línea pequeña hasta ~431 px (60 %); palabra destacada hasta ~510 px (71 %). Margen lateral mínimo ~100 px.
- **Tamaño**: línea normal: altura de ascendente ≈19 px (≈27 px con tilde) → fuente **≈28 px**. Palabra destacada: altura de ascendente/mayúscula 56–60 px → fuente **≈78–85 px** (≈ 2,8–3× la normal). Medido sobre fotogramas parados; en transición el tamaño varía.
- **Color**: sobre A-roll, blanco (≈#F0F0F0, sin trazo visible, sombra leve **[SUPOSICIÓN]**) tanto en línea normal como en destacada. Sobre gráficos claros: línea normal casi negra (≈#101010) y **destacada azul ≈#0050E0** (cuantificado a pasos de 16, margen ±16).
- **Fuente**: sans-serif geométrica/grotesca, negrita, letras anchas y compactas, minúsculas con tilde. **No identifico el nombre**; descrito por lo que se ve.

### 6. Textos en pantalla y gráficos (observado, no medido al píxel)
- Textos del propio gráfico (no son subtítulos): etiquetas en mono ("VÍDEO 1 · EDITADO CON IA", "referencia.mp4", "HAZ CAPTURA", "SKILL.md"), títulos de tarjeta y palabras en serif cursiva azul ("pasos", "Sol").
- Grafismos: tarjeta de móvil con sliders, gráfico de barras, tarjeta "SACRIFICAR" a todo el ancho (flash on/off cada ~2 fotogramas a 1,57–1,70 s), logo Claude, ventana de prompt con barra de carga azul (15,7–19,9 s), tira de película con marcador azul (20,1–23,2), checklist que se marca (estilos/ritmo/textos/colores), tarjetas de tipografía "Aa" que rotan estilo y paleta (24,1–26,9), terminal oscuro con escritura carácter a carácter (30,4–32,0), 3 tarjetas v1/v2/v3 con la v3 seleccionada (37,3), nodos que se conectan a SKILL.md (39,8–41,9).
- Estos gráficos son **b-roll ilustrativo hecho en vector/UI**, no metraje. No hay b-roll de vídeo real, salvo recortes pequeños de otras personas dentro de las tarjetas (0–2,4 s, 20,1–23,2 s).

### 7. Color general
- Gráficos: fondo casi blanco (≈#F5F6F8 **[SUPOSICIÓN]** por lectura visual) con brillos radiales azul pálido en las esquinas; tarjetas blancas con sombra suave; acento azul ≈#0050E0; naranja Claude en el logo; terminal ≈#111827 **[SUPOSICIÓN]**.
- A-roll: sala gris-marrón apagada, camiseta blanca, sin filtro de color fuerte aparente **[SUPOSICIÓN]** (no medí gradación).

### 8. Sonido (medido, limitado)
- **-14,2 LUFS integrado**, pico **-0,1 dBFS**, rango de loudness **2,2 LU** (muy comprimido). Sin silencios bajo -45 dB en los 42,7 s (algo suena siempre).
- Estéreo casi mono: canal lateral -41,2 dB frente a -16,8 dB central.
- Energía continua y fuerte bajo 150 Hz (-33 dB bajo 60 Hz). **No puedo decir si hay música**: no separé pistas (sin Demucs/Whisper instalados). **[SUPOSICIÓN]** posible cama musical o solo voz comprimida.
- **Efectos de UI**: dos firmas distintas en el espectrograma: (a) pila de ~5 rayas cortas entre 4,1 y 5,9 kHz, ~0,2 s ("clic/pop"); (b) tono ~1,5 kHz con armónicos, ~0,15–1 s ("ding"). Segundos leídos del espectrograma (±0,1–0,2 s): (a) ~0,25 · ~6,5 · ~14,6 · ~22,5 · ~29,6 · ~39,9 ; (b) ~16,1 (medido 16,12–16,26) · ~26,2 · ~31,6 · ~37,3. Coinciden con la entrada de un elemento gráfico (p. ej. "pasos" 6,5, logo Claude 14,5, logo Remotion 29,4, "SKILL.md" 39,8), pero la sincronía en ms **no la medí**.
- Los últimos ~0,35 s (desde 42,35) pierden todas las frecuencias altas (>2,5 kHz) en el espectrograma: corte/fundido de audio al final **[SUPOSICIÓN]**.

### 9. Receta para replicar (orden)
1. Lienzo 720×1280 a 30 fps.
2. Grabar A-roll continuo; trocear en tomas de 0,8–2,5 s; usar 2 encuadres (100 % y ~116 %).
3. Alternar A-roll y gráficos cada ~2 s: 9 cortes duros y 5 disolvencias de 0,1 s.
4. Gráficos sobre fondo claro con acento azul #0050E0, tarjetas blancas con sombra; cada elemento entra con fundido/desplazamiento de 0,1–0,3 s.
5. Subtítulos: una frase por vez, palabra a palabra con desenfoque+fundido de 0,1–0,2 s, 1 palabra destacada por frase (≈3× el tamaño, azul en gráficos / blanca en A-roll), centrados, arriba sobre A-roll.
6. Efectos de UI cortos (clic de ~0,2 s) al entrar elementos clave y un ding en las confirmaciones.
7. Mezcla ~-14 LUFS, pico ≤ -0,1 dBFS. Cierre con fundido a negro de 0,3 s.

### 10. Lo que NO pude determinar
- Nombre de la fuente de los subtítulos y de la tipografía de los gráficos.
- Si hay música y cuál es el nivel de voz frente a música.
- La sincronía en ms entre efectos de sonido y animaciones.
- Gradación de color real del A-roll y valores hex exactos (leídos con precisión ±16).
- Transcripción con tiempos por palabra: no tengo Whisper; solo tengo los segundos de entrada de las palabras destacadas, leídos de los fotogramas a 0,1 s.
- Las pausas y cadencia exactas de la voz.

---
**Reglas generales aprendidas en vídeos reales:** ver [§15 de la ficha de YouTube](../youtube/estilo.md#15-reglas-aprendidas-en-vídeos-reales-valen-para-todo-el-estilo-maestria).
