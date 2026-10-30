# estilowsp.md — Estilo «WhatsApp Comunidad» (v1)

**Estado:** aprobado después de 5 pasadas.
**Vídeo de referencia:** «Bienvenida comunidad», un vídeo horizontal a cámara de 39,6 s para la comunidad de WhatsApp.
**Proyecto que lo generó:** un proyecto de HyperFrames 0.8.114 con `build.py` (subtítulos, zoom, sonido) y `fx.py` (motions y confeti). Ese `fx.py` es la base de `../motores/motor-formacion/fxlib.py`.
**Estilo del que viene:** «Edición Claude» v2 (`estilo.md` de esta carpeta), en una versión **horizontal, más limpia y sin gráficos a pantalla completa**.

Cómo se obtuvo cada dato:
- **[MEDIDO]**: sale del MP4 o de la grabación, medido con ffmpeg.
- **[CÓDIGO]**: es el valor exacto que hay en `build.py` o `fx.py`.
- **[DECISIÓN]**: lo pidió o lo aprobó el presentador.

---

## 0. El estilo en 10 reglas
1. **Horizontal 1920×1080 a 30 fps** [DECISIÓN]. El presentador a cámara todo el vídeo, sin cortes a gráficos a pantalla completa.
2. **Edición sencilla, minimalista y clean.** Lo importante son los **subtítulos** [DECISIÓN].
3. **Silencios cortados:** las pausas de más de 0,3 s se quitan, dejando 0,05 s a cada lado.
4. **Zoom alterno al 100 % y al 116 %**, con un plano cada 3,6 s de media. Cada cambio de zoom cae en una unión del corte de silencios, para taparla.
5. **Subtítulos palabra a palabra** en blanco y **debajo de la barbilla**. Llevan **1 palabra destacada cada 2 o 3 frases**, no una por frase.
6. **Motions blancos en los laterales, ligados a lo que se dice:** se dice «comunidad» y gira el logo de Maestría, se dice «$100.000» y sale una moneda con un contador. Nada de decoración sin sentido (partículas o formas sueltas) [DECISIÓN].
7. **Premium = 3D, giros, anillo de luz y destellos**, con el **brillo de los efectos de luz al 50 %** [DECISIÓN].
8. **Sorpresa al inicio:** confeti suave **detrás** del presentador en «familia», con su sonido `success.wav` [DECISIÓN].
9. **Color:** solo **+27 % de brillo en el presentador** y el fondo azul intacto. Nada de cambiar el tono de la piel [DECISIÓN].
10. **Volumen final con ganancia fija + limitador.** Nunca `loudnorm` (ver `estilo.md` §9.4).

---

## 1. Formato y entrega [MEDIDO]
- 1920×1080, 30 fps, H.264, 39,6 s. Audio AAC a 48 kHz.
- Sonoridad final de **−16,2 LUFS** con el pico en ≈ −1 dBFS.
- **Versión para WhatsApp «ligera»** (la que eligió el presentador):
  `ffmpeg -i maestro.mp4 -c:v libx264 -preset slower -crf 24 -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k -ar 48000 salida.mp4`
  Da **13,1 MB** frente a 60 MB del maestro, con un SSIM de **0,991** (visualmente igual). Con CRF 22 salen 19,6 MB y SSIM 0,992.
- Para que WhatsApp la comprima lo mínimo, se envía con la opción **HD**. No está verificado cuánto la recomprime WhatsApp.

## 2. Flujo de trabajo (en este orden)
1. **Preguntar antes de empezar:** formato, estilo de subtítulos y extras (zoom, música, efectos).
2. **Revisar el texto con el presentador.** La transcripción de Whisper se le enseña entera y se le pregunta por las dudas: cifras, palabras raras y signos. **El texto del presentador manda sobre el de Whisper.**
3. **Corte de silencios** con `silencedetect=noise=-30dB:d=0.3`, dejando 0,05 s de margen y un fundido de 0,01 s en cada unión. En el vídeo de referencia quitó 6 pausas y lo dejó en 41,33 → 39,60 s.
4. **Tiempos por palabra** sobre el vídeo ya cortado:
   `whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-small.bin -l es -ojf -dtw small -nfa`
   - El tiempo de cada palabra es `t_dtw − 0,14 s`.
   - La primera palabra después de cada corte se ajusta al **inicio medido por energía** (RMS cada 40 ms). Los `offsets` de Whisper fallaron hasta 0,5 s.
5. **Medir dónde está la cara** (barbilla, centro) con una rejilla sobre fotogramas. En la referencia, la barbilla está en y ≈ 680–740 y la cara en x ≈ 920.
6. **Enseñar fotogramas antes de renderizar** cada cambio visual, y después renderizar la pasada completa.
7. **Medir cada sonido nuevo dentro del render** antes de entregar (ver §7).

## 3. Zoom y encuadre [CÓDIGO]
- **11 planos**, alternando 1,00 y 1,16, con un empuje lento de +0,04 dentro de cada plano.
- `transform-origin: 920px 600px`, para que la cara quede en su sitio y la barbilla baje como mucho a ≈ 770 px.
- Los cambios de plano caen en las palabras que abren frase, y **en la unión del corte de silencios** si hay una a menos de 0,5 s. Fuera de esas uniones, el cambio entra 0,06 s antes de la palabra.
- Aviso [MEDIDO]: al 116–120 % el pelo roza el borde superior. El presentador lo aceptó.

## 4. Subtítulos [CÓDIGO + DECISIÓN]
- **Caja:** de x 260 a 1660 y **top = 800 px**, creciendo hacia abajo.
- **Línea normal:** Hanken Grotesk 700, **64 px**, interlineado 1,2, 18 px entre palabras, en **blanco** con sombra `0 4px 24px rgba(0,0,0,.55)`.
- **Destacada:** en su propia línea, en MAYÚSCULAS, a **112 px**, interlineado 1,05 y espaciado de letras −3 px. Se le quita la puntuación final.
- **9 destacadas en 27 trozos** (una cada 3). En la referencia fueron FAMILIA, BIENVENIDA, EXCLUSIVO, RÁPIDO, CLASE, $100.000, GRATIS, DINERO y PERDER?.
- **Entrada de cada palabra:** desenfoque de 10 px → 0, y +14 px → 0, opacidad 0 → 1, en 0,12 s con `power2.out`.
- **Entrada de la destacada:** escala 0,7 → 1 y desenfoque de 14 px → 0, en 0,16 s con `back.out(2.5)`.
- Cada trozo tiene 2–7 palabras cortadas por sentido, y se apaga en 2 fotogramas justo antes del siguiente.
- **Degradado inferior:** 380 px de negro al 38 % → transparente, para que se lea el texto.

## 5. Motions [CÓDIGO + DECISIÓN]
### 5.1 Reglas
- Todos van en **blanco**. Solo se usa el azul **#0050E0** en detalles (el $, la cerradura, las estrellas de la bandera, el ✓) y el rojo **#E5484D** en «EN VIVO».
- Van **a un lado del presentador**: izquierda en cx ≈ 270–300 y derecha en cx ≈ 1590–1620, a y ≈ 330–400. Nunca encima de la cara ni de los subtítulos (todo por encima de y < 760).
- Se **alterna el lado** de un motion a otro.
- Cada uno **arranca 0,1 s antes de su palabra** (`LEAD`) y dura entre 2 y 3 s. Sale con opacidad → 0, escala 0,8 y y −30, en 0,3 s.
- **Envoltorio común** (`box()`), con el brillo al 50 %:
  - Entrada: escala 0,35 → 1, en 0,5 s con `back.out(1.7)`.
  - **Anillo de luz:** borde de 3 px en blanco al 45 %, escala 0,3 → 1,9, en 0,8 s.
  - **Halo:** degradado radial blanco al 22 %, a opacidad 0,4.
  - Flotación suave de ±8–10 px.
- **3D:** `perspective: 1100px`. El grosor se hace con 8–10 capas grises (#aab4cc o el logo en gris) separadas en Z.

### 5.2 Catálogo (vídeo de referencia)
| Palabra | Motion | Lado | Sonido (volumen) |
|---|---|---|---|
| comunidad | **Logo Maestría** que gira 360° en 3D con grosor, reverso legible, anillo y un brillo azulado que lo cruza | der. | whoosh-morph 0,24 |
| acceso / exclusivo | Candado que entra girando 180° y se abre con «exclusivo». Pastilla «ACCESO» y 3 destellos | izq. | click 0,22 + sparkle 0,05 |
| inteligencia | Chip que se dibuja trazo a trazo (`strokeDashoffset`) y se enciende con «AI». El halo late | der. | type-short 0,24 |
| avanza… rápido | Flecha que sale disparada en diagonal (−30°) con 6 líneas de velocidad en bucle, a escala ×1,5 | izq. | whoosh-slide 0,23 |
| clase | Pantalla con ▶ y la insignia roja «● EN VIVO» latiendo, a escala ×1,15 | der. | ding 0,15 |
| cinco | «5» gigante (280 px) que cae de golpe con temblor, más «SISTEMAS AI» | izq. | impacto 0,08 |
| Estados Unidos | Bandera en blanco: las franjas se dibujan, las estrellas aparecen y ondea | der. | whoosh 0,24 |
| $100.000 | **Moneda $ en 3D** que gira 720°, contador +$0 → +$100.000 en 1 s y 4 destellos | izq. | ding 0,15 + subida 0,10 |
| fácil de instalar | Tarjeta «INSTALANDO» con barra y % que cuentan, y luego «LISTO ✓», a escala ×1,3 | der. | click 0,22 + success 0,05 |
| gratis | «$0» de golpe con temblor, más «GRATIS». Vuelve a latir en el segundo «gratis?» | izq. | pop 0,28 |
| hacer dinero | 6 monedas que caen girando en 3D y se apilan (3 + 2 + 1) con rebote | der. | whoosh-slide 0,23 + sparkle 0,05 |
| ¿te lo vas a perder? | **Logo Maestría** otra vez girando como cierre | izq. | whoosh-morph 0,24 + chime 0,14 |

- Etiquetas de los motions: Hanken 700, 32 px, espaciado de letras 6 px, en MAYÚSCULAS.
- **Logo:** `Downloads/Maestria/Maestria logo.png` (576×576, fondo blanco). Se pasa a **blanco transparente** así: se recorta, se escala ×3 y `alpha = (255 − luma) × 1,7`. Quedan `assets/logos/maestria-blanco.png` y `maestria-gris.png` (para el grosor).

## 6. Confeti de inicio [CÓDIGO + DECISIÓN]
- Se lanza en **«familia» − 0,1 s**, con **70 papelitos** en blanco, #dbe6ff, #a9c3ff y #f4f7ff (rectángulos de 10–14×16–26 px y círculos).
- Salen de detrás de los hombros (x = 960 ± 160–260, y 560–680), suben entre 360 y 600 px y caen girando. **Desaparecen antes de los 2,9 s.**
- **Va detrás del presentador:** el orden de capas es vídeo → confeti → recorte del presentador (`persona-inicio.webm`, 0–3,4 s).
  - El recorte se hace con `hyperframes remove-background inicio.mp4 -o persona-inicio.webm --device cpu --quality best` sobre los primeros 3,5 s del vídeo cortado. Tardó 3,6 min en CPU.
- **Sonido:** `landing-codigomaestria/sonidos/success.wav`, copiado con **+6 dB** y a **volumen 0,8**. Así su pico queda igual que el del pop aprobado (−12,6 dBFS).

## 7. Sonido [MEDIDO + CÓDIGO]
- Hay **voz y efectos, sin música** [DECISIÓN]: 20 efectos en 39,6 s.
- Base de efectos: swish al empezar (0,24), pop en «bienvenida» (0,28), ding en «$100.000» (0,15), pop en «gratis» (0,28) y chime en «perder?» (0,14). Más uno por cada motion (§5.2).
- Los volúmenes son los ya aprobados en `estilo.md` §9.3. Los archivos están en `stock completo/sonidos/`.
- **Un sonido nuevo se iguala por PICO, no por LUFS.** El objetivo es que su pico en la mezcla esté en ≈ −12,6 dBFS, igual que el pop: `pico del archivo + 20·log10(volumen)`.
- **Comprobar siempre que se oye:** se resta el render sin el sonido del render con él, en la ventana del sonido. Tiene que quedar a unos −26 dB RMS o más, con la voz a ≈ −13 dB.
- **Volumen final:** `ffmpeg -i render.mp4 -c:v copy -af "volume=1.8dB,alimiter=limit=0.79:attack=5:release=50:level=false" -ar 48000 -c:a aac -b:a 256k maestro.mp4`. Los +1,8 dB valen para esta voz (en bruto, −19,1 LUFS). Con otra grabación hay que recalcularlos para llegar a ≈ −16 LUFS.

## 8. Color [MEDIDO + DECISIÓN]
- **Solo +27 % de brillo en la persona.** El fondo azul queda igual: se midió una diferencia de ≤ 1/255 en 3 momentos.
- Se aplica a la grabación (`aroll.mp4`) **antes** de renderizar, nunca al render final, para no tocar los gráficos ni los subtítulos:
  ```
  [0:v]split=3[a][b][c];
  [b]curves=all='0/0 0.35/0.46 1/1',format=yuva444p[br];
  [c]format=yuva444p,chromakey=color=0x526BF9:similarity=0.12:blend=0.08,alphaextract[m];
  [br][m]alphamerge[p];[a][p]overlay=format=auto,format=yuv420p
  ```
- Al recorte del confeti (`persona-inicio.webm`) se le aplica la misma `curves` (conservando la transparencia), para que el color no salte a los 3,4 s. Se midió: 121 → 118 → 117, sin salto.
- `0x526BF9` es el azul medido del fondo de esta grabación. **Con otro fondo hay que medirlo de nuevo.**
- La camiseta y las manos también suben un poco; el presentador lo aceptó.
- **Descartado:** corregir el tono de la piel con `selectivecolor`. La piel pasó de 342° a 25°, pero quedó amarilla.
- Se guardan siempre los originales: `aroll-original.mp4` y `persona-inicio-original.webm`.

## 9. Preferencias del presentador (aplicar siempre)
- Un motion solo tiene sentido si **ilustra lo que se dice**. Lo «premium» tiene que hacer pensar «guau, esto no lo hace cualquiera».
- Logo de Maestría **en blanco**, con giro 360°.
- Efectos de luz suaves, con el brillo al 50 %.
- Antes de un cambio grande, **enseñar una muestra corta en movimiento** (9 s) o fotogramas, y luego hacer el resto.
- Color natural: no tocar el tono de la piel. Si la cara se ve apagada, subir solo el brillo de la persona.
- El sonido lo elige él cuando no hay uno adecuado en el stock. No descargar nada sin su OK.

## 10. Errores que no hay que repetir (pasaron en este vídeo)
1. **Entender «motions» como decoración** (líneas, partículas, formas). El presentador quería gráficos ligados a palabras.
2. **`<img>` con `inset:0` dentro de una capa 3D:** sale a su tamaño natural (el logo salió gigante encima de la cara). Hay que usar `width:100%; height:100%`.
3. **Girar un logo 360° sin reverso:** se ve el texto al revés. Hay que poner una cara trasera con `rotateY(180deg)` y `backface-visibility:hidden`.
4. **Tweens con posición negativa en la línea de tiempo de GSAP:** desplazan TODO (desaparecieron los subtítulos). Nunca empezar antes de 0.
5. **30 o más elementos con `filter: blur`:** HyperFrames avisa de que la captura puede salir en negro. Usar `box-shadow`.
6. **Igualar un efecto corto por LUFS:** el `success.wav` quedó 26 dB bajo la voz y no se oía. Hay que igualarlo por pico y medirlo en el render.
7. **Flecha y ✓ demasiado cerca del borde o de la cabeza:** comprobar con capturas en los planos al 116 %.
8. Con ffmpeg 8 se usa `-/filter_complex archivo.txt` (no `-filter_complex_script`), y `-fps_mode` en vez de `-vsync`.

## 11. Lo que NO está verificado
- Ninguna pasada la he escuchado ni visto entera en movimiento. El sonido y la fluidez los validó el presentador.
- Cuánto recomprime WhatsApp el archivo al enviarlo.
- Puede quedar un ligero contorno en los bordes del recorte o de la máscara de brillo (pelo, orejas con luz azul).

---
**Reglas generales aprendidas en vídeos reales:** ver [§15 de la ficha de YouTube](../youtube/estilo.md#15-reglas-aprendidas-en-vídeos-reales-valen-para-todo-el-estilo-maestria).
