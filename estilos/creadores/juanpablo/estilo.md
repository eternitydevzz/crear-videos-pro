# Estilo «Juanpablo»

> **Nota del repo:** esta ficha se hizo con el reel descargado y sus archivos de trabajo (`video.mp4`, `Frames/`, `cortes.txt`, `info.txt`, `audio/`, `transcripcion.md` y `ventanas/`). En el repo solo están la ficha y los **mosaicos**: esos archivos se citan como fuente de los datos, pero no se incluyen. Para tenerlos, pasa el link del reel por `/crear-videos-pro:crear-estilo-videos`.

Sale de 3 reels (misma persona, mismo set, misma edición):
- reel1 = https://www.instagram.com/p/DeP8magAePo/ (80,1 s)
- reel2 = https://www.instagram.com/p/DdSH5grDytg/ (76,4 s)
- reel3 = https://www.instagram.com/p/Dc6YmWBFbOH/ (73,0 s)

Lo que el usuario quiere replicar: **un pop en cada palabra clave y la palabra clave remarcada** (lo que da dinamismo). Sin música. El sonido a replicar es el pop.

Cada dato va marcado **[MEDIDO]** (sale de un fotograma, de una medición o de un recuento) o **[SUPOSICIÓN]** (interpretación mía, con su motivo).

## Resumen: 10 reglas

1. **Tres capas de texto, todas centradas (x = 540):** título arriba (y 272-390), píldoras de palabra clave en el centro-bajo (desde y 1180) y un subtítulo pequeño debajo (y 1525-1558). [MEDIDO]
2. **La palabra clave va en una píldora:** caja blanca (#FEFEFD), 115 px de alto, esquinas redondeadas de ≈11 px, letra negra (#020202) muy gruesa de 64 px (de lo alto de la «d» a la base) y ≈26 px de margen por cada lado. [MEDIDO]
3. **Una píldora = una o dos palabras.** Se van apilando hacia abajo: la segunda empieza 39 px por debajo de la primera y se ven hasta **3 píldoras** a la vez. [MEDIDO]
4. **La píldora entra de golpe** (en 1 fotograma, sin crecer ni fundirse) y sale de golpe cuando acaba la frase. Dura **0,45-0,8 s**. [MEDIDO a 30 fps]
5. **El pop suena con la píldora:** empieza 29-76 ms después de que la píldora se vea (lo normal, ≈40-50 ms, es más o menos 1 fotograma) y dura **120-230 ms** (mediana 130 ms). De 79 pops, 73 caen justo al aparecer una píldora y los 6 restantes también, en píldoras que el detector automático no vio porque iban sobre grabaciones de pantalla. [MEDIDO]
6. **Es el mismo pop siempre:** su espectrograma tiene la misma silueta en los 3 reels (un bloque de ruido de ≈2 a 16,5 kHz con tres «almenas» arriba, en ≈17 kHz). [MEDIDO como forma; cómo suena: no lo he oído]
7. **Lleva pop alrededor de la mitad de las píldoras** (≈48 %, ≈63 % y ≈48 %). **Nunca llevan pop las cifras** (20 $, 70 %, 7.000, 3, 1º…), ni las palabras apiladas bajo una cifra, ni el CTA «comenta + PALABRA». **Casi siempre lo llevan** las palabras de acción o de concepto (convertir, locura, construye, memoria…). Con las marcas no hay patrón fijo. [MEDIDO, recuento a ojo]
8. **Ritmo de pops: 16-27 por minuto**, con una separación mediana de 0,9-3,3 s entre uno y otro. [MEDIDO]
9. **Se habla a cámara con jump cuts y se meten tramos de grabación de pantalla** (un portátil grabado con el móvil, con la cámara moviéndose), que ocupan el **23-33 %** del vídeo, repartidos en 3-5 tramos de 1,7-9,7 s. [MEDIDO aprox., ±0,5 s]
10. **Sin música.** La voz va masterizada a **−14 LUFS**, pico de **−0,6 a −0,9 dBFS**, casi mono y sin ningún silencio. [MEDIDO; lo de la música lo confirmó el usuario]

## 1. Datos técnicos [MEDIDO]

| | reel1 | reel2 | reel3 |
|---|---|---|---|
| Resolución | 1080×1920 | 1080×1920 | 1080×1920 |
| fps | 29,97 | 29,97 | 30 |
| Duración | 80,1 s | 76,4 s | 73,0 s |

## 2. Estructura y ritmo

**Tipos de plano:**
- **A-roll:** él sentado en una silla gamer, con sudadera gris pardo y fondo de estantería roja y blanca; plano medio, la cara en el tercio superior.
- **Gráfico/B-roll:** la pantalla de un portátil grabada con el móvil (GitHub, Google AI Studio, webs de demo), con un movimiento de cámara lento.

**Tramos de grabación de pantalla [MEDIDO aprox. con cortes.txt y una tira de 1 fotograma/s; ±0,5 s]:**

| reel | tramos de grabación de pantalla (s) | total | % |
|---|---|---|---|
| 1 | 16,0-25,7 · 27,7-33,5 · 41,2-50,4 | 24,6 s | 31 % |
| 2 | 12,7-18,7 · 26,9-35,1 · 48,6-51,6 | 17,2 s | 23 % |
| 3 | 6,1-12,0 · 17,6-19,3 · 26,6-34,5 · 38,9-43,6 · 47,8-51,6 | 24,1 s | 33 % |

- **Duración de los planos:** grabación de pantalla, de 1,7 a 9,7 s. Habla a cámara: hasta ≈16 s seguidos, pero con jump cuts dentro.
- **Jump cuts en A-roll:** he comprobado dos a 30 fps (reel1, 4,87 s y 8,68 s): la postura y la mano saltan de un fotograma al siguiente. cortes.txt marca otros 10-30 «dudosos» por reel, pero algunos son solo la entrada de una píldora (también sube la puntuación), así que **no he contado el total de jump cuts**. [MEDIDO 2; el resto SIN COMPROBAR]
- **El título se va con el primer jump cut** (reel1: está hasta 4,84 s y desaparece en 4,87 s, en el corte). En los reels 2 y 3 la tira de 1 fps es coherente con eso (se va hacia los 5 s y los 3-4 s). [MEDIDO en reel1; SUPOSICIÓN en 2 y 3]
- **Cierre:** «comenta + "PALABRA"» y, después, «seguirme / compartirlo», todo en píldoras. [MEDIDO, igual en los 3]

## 3. Transiciones [MEDIDO]

- **Casi todo es corte duro.** Algunos cambios entre cámara y pantalla aparecen como «disolvencia de 2 fotogramas» (reel1 16,02 s; reel2 14,98 y 26,93 s; reel3 6,07, 17,60 y 34,53 s), es decir, ≈0,07 s. En el mosaico a 15 fps se ven como un cambio seco.
- No hay barridos, zooms de transición ni efectos.

## 4. Zoom y encuadre

- En los mosaicos no se ve ningún zoom animado ni ningún punch-in claro entre tomas. [SUPOSICIÓN: la medida automática del encuadre (caja de piel) no sirve aquí, porque las manos se meten en la caja; lo he juzgado a ojo]
- La grabación de pantalla tiene un movimiento de cámara suave y real (hecho con el móvil, no en la edición). [SUPOSICIÓN: lo deduzco del temblor y la perspectiva]

## 5. Subtítulos y palabra clave

### 5a. Píldora de palabra clave (lo principal) [MEDIDO en reel1, 1,668 s, con medir.py]

| | Valor |
|---|---|
| Caja | blanca #FEFEFD, opaca, sin sombra visible |
| Alto de caja | 115 px (6,0 % del alto) |
| Ancho | se ajusta a la palabra: 283 px para «mirar», 330 px para «videos» (hasta ≈640 px en palabras largas) |
| Esquinas | redondeadas, radio ≈11 px (medido a ojo en una ampliación 4×) |
| Texto | negro #020202, fuente sans muy gruesa (heavy/black), minúsculas tal como se dice; números, siglas y la palabra del CTA en MAYÚSCULAS entre comillas («"EXPERTO"», «"SKILL"») |
| Tamaño de letra | 64 px de lo alto de la «d» a la base; 46 px de alto de minúscula |
| Margen interior | ≈26 px a izquierda y derecha, 25-27 px arriba y abajo |
| Posición | 1.ª píldora en y 1180-1294 (61,5-67,4 %), centrada en x = 540 |
| Apilado | 2.ª en y 1333-1448 (39 px de hueco); se ven hasta 3 a la vez |
| Entrada / salida | de golpe, en 1 fotograma; todas salen juntas al acabar la frase |
| Duración | 0,45-0,8 s (ejemplos: «mirar» 1,30-1,93; «perfección» 36,30-37,00; «capacidades» 39,64-40,44) |

- La posición se mantiene encima de la grabación de pantalla; sobre gráficos baja como mucho a y ≈1240. [MEDIDO con el detector]
- **Qué palabras van en píldora:** el sustantivo o el verbo que lleva la idea de la frase, no los artículos ni los conectores. Dos píldoras apiladas cuando la idea son dos palabras («mirar / videos», «agente / especializado», «memoria / entre / prompt»). [MEDIDO, listas en `reelN/transcripcion.md`]
- **Cuántas:** 44 en el reel1, ≈54 en el reel2 y ≈50 en el reel3, o sea **35-42 por minuto**. [MEDIDO, recuento a ojo; sobre la grabación de pantalla se me puede haber escapado alguna]

### 5b. Subtítulo pequeño [MEDIDO]

- Blanco #FCFBFA, letra fina/regular sin contorno, 34 px de alto («mirar videos», sin descendentes).
- y 1525-1558 (79,4-81,1 %), centrado. Siempre en la misma altura, debajo de las píldoras.
- 1-3 palabras por bloque; cambia cada ≈0,3-0,6 s y sin animación (se reemplaza de golpe). [MEDIDO en mosaicos a 15 fps]
- Repite lo que se dice, incluida la palabra que sale en la píldora.

### 5c. Título (gancho) [MEDIDO]

- Blanco #FCFCFC, sans muy gruesa y con un contorno o sombra oscuros finos alrededor de la letra (se ve en el fotograma a tamaño completo).
- 2 líneas: y 272-333 (62 px de alto, ancho 738) y 342-390 (49 px de alto, ancho 562), es decir, 14,2-20,3 % del alto. Centrado.
- Solo en los primeros segundos (reel1: 0-4,84 s).
- Textos: «Ahora Claude puede ver videos de Youtube», «Esta skill te ahorra más del 70% de tokens», «La skill que hace paginas con efecto scroll de Apple».

## 6. Textos en pantalla y gráficos

- Fuera de las tres capas de texto **no hay gráficos añadidos**: ni flechas, ni emojis, ni barras de progreso, ni logotipo. [MEDIDO en los 38 mosaicos del reel1 y en las tiras y hojas de recortes de los reels 2 y 3]
- Los «gráficos» son grabaciones reales de la pantalla. Sobre ellas siguen saliendo píldoras y subtítulos.

## 7. Color [MEDIDO en fotogramas]

- Texto: blanco casi puro (#FCFCFC-#FEFEFD) y negro (#020202). Ningún color de acento en los textos.
- Escena: rojo de la estantería, blanco y gris; sudadera gris pardo; luz cálida. Las grabaciones de pantalla son en modo oscuro.

## 8. Sonido [MEDIDO, limitado: no he escuchado el audio]

| | reel1 | reel2 | reel3 |
|---|---|---|---|
| Sonoridad integrada | −14,2 LUFS | −14,2 LUFS | −14,1 LUFS |
| Pico | −0,7 dBFS | −0,6 dBFS | −0,9 dBFS |
| LRA | 4,1 LU | 4,2 LU | 3,7 LU |
| Silencios (< −45 dB, > 0,1 s) | ninguno | ninguno | ninguno |
| Estéreo | casi mono (lateral 21 dB por debajo) | casi mono (23 dB) | casi mono (23 dB) |
| Pops | 21 (15,7/min) | 34 (26,7/min) | 24 (19,7/min) |
| Separación mediana entre pops | 3,34 s | 0,93 s | 1,66 s |

- **Música:** no hay (lo confirmó el usuario).
- **El pop [MEDIDO como forma]:** un bloque de ruido de banda ancha de ≈2 a 16,5 kHz, de 120-230 ms, con el borde de arriba cortado a 16,5 kHz y tres «almenas» en ≈17 kHz. La silueta es idéntica en los 3 reels, así que es el mismo archivo de sonido pegado una y otra vez. En la banda de 12-16 kHz queda +40 a +54 dB por encima de la mediana; la voz, en esa banda, solo llega a +25-30 dB. Todos los segundos están en `reelN/audio/tramos_agudos.txt` (filas con +40 dB o más).
- **Su volumen frente a la voz** no lo he medido en dB absolutos.
- Que le llame «pop» es cosa del usuario, que lo ha oído. Por el espectro podría ser un pop, un «swish» corto o un clic con cola de ruido. [SUPOSICIÓN]
- **Sincronía [MEDIDO]:** 79 de 79 pops caen sobre la aparición de una píldora, entre +29 y +76 ms después (≈1 fotograma). Ningún pop suena sin píldora.

## 9. Receta para replicar (en orden)

1. **Grabar:** a cámara, plano medio, fondo con color; además, grabar con el móvil la pantalla del portátil mientras se navega por lo que se explica.
2. **Montaje:** quitar pausas con jump cuts (corte duro). Meter 3-5 tramos de grabación de pantalla de 2-10 s, hasta un 25-33 % del total, justo cuando se nombra la herramienta o se enseña algo.
3. **Título:** 2 líneas, blanco, sans gruesa con contorno oscuro fino, centrado en y ≈272-390. Visible desde 0 s hasta el primer jump cut (≈3-5 s).
4. **Subtítulo pequeño:** blanco, letra fina, 34 px de alto, centrado en y 1525-1558; 1-3 palabras por bloque, en corte seco.
5. **Píldoras:** en cada frase, elegir 1-2 palabras clave (≈35-42 por minuto). Caja blanca de 115 px de alto, radio ≈11 px, margen de 26 px, letra negra muy gruesa de 64 px; la primera en y 1180, centrada; las siguientes 39 px más abajo (máximo 3). Entran de golpe cuando se dice la palabra y salen todas juntas al acabar la frase (0,45-0,8 s).
6. **Pop:** el mismo archivo siempre, de 120-230 ms, colocado 1 fotograma después de que salga la píldora. Va en las palabras de acción o de concepto. **No va** en cifras, en las palabras apiladas bajo una cifra ni en «comenta + PALABRA». Se copia el original: lo lleva ≈la mitad de las píldoras, 16-27 pops por minuto (decisión del usuario, 10/10/2026).
7. **Cierre:** «comenta» + «"PALABRA"» en mayúsculas entre comillas, y después «seguirme» y «compartirlo».
8. **Audio:** solo voz, sin música, a −14 LUFS y pico ≈−0,7 dBFS.

## 10. Lo que no se pudo determinar

- **Nombre de la fuente** de las píldoras y del título: una sans geométrica muy gruesa, de minúsculas redondas, con la «a» de dos pisos. No sé cuál es.
- **El archivo de sonido del pop** y su nombre: solo tengo su forma en el espectrograma, no lo he escuchado.
- **Volumen del pop frente a la voz** en dB absolutos.
- **App de edición:** no hay ninguna marca que la delate.
- **Número exacto de jump cuts:** solo he comprobado 2.
- **Por qué unas píldoras llevan pop y otras no** en las palabras normales («skill / nueva» y «agente / especializado» no lo llevan; «mirar / videos» sí). Puede que sea a criterio del editor.

## Archivos de apoyo

- `reelN/pildoras_y_golpes.tsv`: apariciones de píldora detectadas automáticamente (fallan sobre las grabaciones de pantalla).
- `reelN/audio/tramos_agudos.txt`: tramos de 12-16 kHz; los de +40 dB o más son los pops.
- `reelN/hoja_pildoras/hoja_*.jpg`: recorte de cada píldora y cada pop, con su segundo y «POP / sin pop».
