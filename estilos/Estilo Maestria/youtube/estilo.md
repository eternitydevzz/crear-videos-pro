# estilo-nuevo.md — Estilo de YouTube (v2)

**Estado:** probado y aprobado en el vídeo completo «Vende Sistemas IA en USA» (YouTube 2, 12:54, cerrado).
**Vídeo de referencia:** `video YouTube 2/Vende Sistemas IA en USA.mp4`.
**Proyectos de referencia (el código):** `video YouTube 2/todas las versiones/` — un proyecto por minuto (`… estilo nuevo`, `- min 2` … `- min 10`, `- cierre`). Ver §13.
**Versiones anteriores:** v1 (solo el minuto 1) en `estilo-nuevo.v1.bak`; v0 en `estilo-nuevo-v0-antiguo.md`. Referencias de imagen: `estilo-nuevo/referencias/`.

Cada regla dice de dónde sale:
- **[DECISIÓN]**: lo pidió el presentador (la frase entre comillas es suya).
- **[CÓDIGO]**: valor del código del vídeo final.
- **[MEDIDO]**: medido en el vídeo final.

Si una regla de aquí choca con lo que diga el presentador en un vídeo nuevo, manda lo que diga él, y se actualiza esta ficha.

---

## 0. El estilo en 12 reglas
1. **Horizontal 1920×1080 a 30 fps.** Voz + efectos + **música por bloques** (§9).
2. **Colores: azul y blanco.** Azul de marca `#0050E0`; pantallas azules `#2f74ff → #1157df → #003fab`; texto oscuro `#101010`; rojo solo para errores `#E5484D`; verde para lo «bueno» (check, dinero).
3. **Cada pieza entra con su palabra:** el elemento 0,10 s antes de su palabra, la escena 0,06 s antes (2 fotogramas). Nunca un panel vacío esperando su contenido [DECISIÓN].
4. **Nada encima del micrófono.** Los motions sobre la cara van **siempre a la derecha** y **detrás del presentador** (§4).
5. **Centrado:** título + objeto son **un bloque** centrado en su zona libre. En blur o b-roll a pantalla completa, **en el centro exacto** (≈ 540 px de alto) [DECISIÓN 22–23-oct, «PON LAS ANIMACIONES EN EL CENTRO»].
6. **Fino, con margen y simetría:** nada gordo, pegado, gigante ni vacío [DECISIÓN].
7. **Glass para los motions de la derecha** (cristal translúcido azul) [DECISIÓN].
8. **Sin destellos ni fotogramas muertos:** de una pieza a pantalla completa a otra se pasa directo; nunca asoma la cara un instante ni parpadea un subtítulo [DECISIÓN].
9. **Zoom de la cara solo tras un punto,** nunca a mitad de frase [DECISIÓN].
10. **Mezcla de planos con ~10 s de cara** entre transiciones (§2) [DECISIÓN].
11. **Motion vivo y distinto:** cada motion con su propia idea animada; nada se queda quieto; nunca listas de texto con emojis [DECISIÓN].
12. **Pausas cortas:** las pausas de la voz se dejan en ~0,12 s; nunca se quitan enteras.

## 1. Estructura del vídeo
- **Gancho (0–1:40):** cara a pantalla completa con la cifra contando abajo y notificaciones de pago a la derecha; ritmo alto con pantallas azules, blurs, b-rolls y cámara reducida.
- **Cuerpo, por bloques:** cada bloque abre con una **pantalla azul de título** (§5) y mezcla cara + motions glass, cámara reducida con tarjetas claras, blurs y b-rolls.
- **Cierre:** llamada a la acción (QR, que se escanea **una sola vez** y se queda hasta que termina de explicar la llamada) [DECISIÓN] y **pantalla final** (§10).

## 2. Ritmo y planos
- **Rotación de planos:** pantalla azul → cara central → cara lateral izquierda → cara en círculo → cara lateral derecha → cara central, con blurs entre medias. [DECISIÓN].
- **Unos 10 s de cara hablando** antes de cada transición [DECISIÓN].
- **Sin destellos de cara:** si entre dos escenas quedaría menos de ~1 s de cara, se alarga la primera hasta la segunda. Las escenas entran sin transparencia y los b-rolls sin fundido desde 0 [DECISIÓN].
- **Ningún fotograma muerto:** ni un fotograma de subtítulo apagado, ni un panel que aparece y desaparece. [DECISIÓN].

## 3. Cámara del presentador [CÓDIGO]
| Formato | Cuándo | Cómo |
|---|---|---|
| Pantalla completa | La cara hablando | Zoom alterno **100 % / 116 %** con empuje lento +4 % en cada plano; origen del zoom (920, 640). Sombra inferior de 380 px (negro 38 % → 0). El zoom cambia **solo en la palabra que sigue a un punto** [DECISIÓN]. |
| Apertura a la derecha | Presentar algo importante (país, herramienta, marca) | Sin zoom: el plano se desplaza **320 px a la izquierda en 0,5 s** (power3.out) con desenfoque de movimiento (9 px → 0). «La clave es abrir hacia la derecha», no un zoom fuerte [DECISIÓN]. |
| Blur | Poner algo encima (§6) | Cámara desenfocada **34 px** y **28 % más oscura** (brightness 0,72). |
| Lateral (derecha o izquierda) | Explicar con tarjetas claras (§7) | Recuadro con esquinas de 44 px; el gráfico en el hueco. Sin zoom en la cara. |
| Círculo arriba a la derecha | Listas, pasos, errores 1-2-3 | Cabeza y hombros dentro de un círculo, sin zoom. |

- Entrada a lateral o círculo: el recorte se anima en 0,55 s (power3.inOut). La **vuelta a pantalla completa es de golpe** [DECISIÓN].
- **El micro nunca se oculta** [DECISIÓN].
- **Si se ve la cara del presentador por arriba y por abajo del marco, está mal** [DECISIÓN].

## 4. Motions sobre la cara
- **A la derecha y detrás del presentador:** el panel va detrás de un recorte suyo (persona + silla + micro, webm con transparencia), y su silueta solo tapa el **borde** del panel. Comprobarlo también en los planos con zoom 116 % [DECISIÓN].
- **Separados de la cara:** [DECISIÓN].
- **Estilo glass:** degradado translúcido azul/blanco + borde fino claro + esquinas muy redondeadas + brillo suave, con una etiqueta mono en mayúsculas arriba (p. ej. «EL TRUCO», «SISTEMA PROPIO»). **Sin `backdrop-filter`** (cuelga el render) [CÓDIGO + memoria «render-atascos-cristal»].
- **Una idea visual propia por motion:** iconos, contadores, líneas que conectan, trayectorias. Nunca «cristal + icono + chips» repetido, ni filas de texto con emoji., «super genérico» [DECISIÓN].
- **Finos:** líneas y chips proporcionados al icono; nada tapa textos ni se superpone; nada se queda en blanco o vacío [DECISIÓN].
- **Motion vivo:** lo que entra flota (4–8 px, 1,6–2,4 s por ciclo), late o brilla un poco [DECISIÓN].
- **Logos reales** siempre que se nombra una marca o herramienta [DECISIÓN].
- **Motions blancos sencillos** (chip, bandera, banderas, bocadillo, flecha…, en `motions.py`): a la derecha, cx ≈ 1500–1620, cy ≈ 500. Ej.: «la bandera de USA en blanco» [DECISIÓN].
- **Recordatorio de suscripción:** banner estilo YouTube claro, **3 s**, a la derecha en un tramo de solo cara. Foto en círculo → se abre el banner → «Suscribirse» se pulsa → «Suscrito» → aparece la campana y el botón se aparta. **Roboto**, «@TuCanal», «10K suscriptores», proporción ~4,9 : 1 (534 × 124 px, 569 con la campana), sin hueco entre el ✔ y el botón [DECISIÓN 24-oct; código: función `subs` en `- min 3/proyecto/motions.py`].

## 5. Pantallas azules
- Para **títulos de bloque y preguntas**: texto blanco grueso centrado y etiqueta mono encima [DECISIÓN].
- Entran con escala 1,7 → 1 y desenfoque. **Sin borde gris** alrededor del azul [DECISIÓN].
- Tachado blanco solo si encaja [DECISIÓN].

## 6. Blur
- **El blur es para poner algo encima:** nunca blur vacío. Lo que va encima entra a la vez que el blur [DECISIÓN].
- **Variantes:** blur + texto, blur + motion, blur + texto + motion [DECISIÓN].
- **Sin bordes negros:** en esas escenas el fondo es el blur, no un recuadro [DECISIÓN].
- Sobre un b-roll, el blur es **del propio b-roll** (p. ej. la estatua de la libertad en el 3:16, Trump en la noticia del 0:36) [DECISIÓN].

## 7. Cámara reducida con tarjetas claras (estilo «V3»)
- Cámara en lateral o círculo; en el resto, **fondo claro** con tarjetas blancas, sombra suave y acentos azules (estilo de «Recepcionista IA», aprobado) [DECISIÓN].
- Títulos negros; cifras en azul (sin degradado); verde para lo conseguido [DECISIÓN].
- **Listas:** números «1, 2, 3» **sin ceros delante, azules y centrados ópticamente** [DECISIÓN].
- **Escala fina** [memoria «margen-simetria»]: títulos ~40 px/600, cifras 36–46 px/600–700, etiquetas 18–24 px; ≥100 px de aire a la cámara y a los bordes; 28–32 px entre tarjetas; hermanos del mismo alto y alineados.

## 8. B-rolls
- **Se le enseñan al presentador antes de montarlos** (hoja con fotogramas) [DECISIÓN].
- **Entran justo al acabar una frase**, se ven **limpios 1–2 s** (mínimo 1 s) y después pasan a **blur con el motion encima**. Nunca un panel sobre un b-roll nítido [DECISIÓN].
- **Calidad alta y cinematográfica:** nada de 720p reescalado, nada de vídeos verticales recortados, nada genérico; el clip tiene que encajar con lo que se dice [DECISIÓN].
- **3–6 por minuto como mucho** [DECISIÓN].
- **Técnica:** pasar a 30 fps si vienen a 24/25 (`minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir`); estabilizar si tiemblan (`deshake=rx=32:ry=32`; rx múltiplo de 16); si un b-roll se repite en bucle, «que no se note» [DECISIÓN].
- **Fuentes:** Pexels (4K) y Mixkit. Vídeos del iPhone en HDR → tonemap a bt709. Revisar la rotación.

## 9. Sonido y música
- **Efectos** (`proyecto/assets/sfx/`): `pop` 0,22–0,28 · `click` / `mouse-click` 0,22–0,3 · `whoosh` 0,2–0,24 · `ding` 0,15 · `subida` 0,10 · `impacto` 0,08 · `iphone-noti` 0,22. Cada efecto, anclado a una palabra o a una entrada.
- **Ding, nunca `success`** [DECISIÓN].
- **Música por bloques** (un tema por sección, cambia en los cortes) de **Epidemic Sound** [DECISIÓN].
  - **La elige el presentador escuchándola**; yo solo propongo opciones [DECISIÓN].
  - **Nivelada continuamente** para que suene siempre igual [DECISIÓN]: se mide en ventanas de 2 s y se corrige suave (cambios en ~1 s).
  - **Nivel final** que dejó el presentador [MEDIDO]: bloques entre **−33,9 y −38,3 LUFS** con la voz a **−16,5 LUFS**, o sea, **unos 17–22 dB por debajo de la voz**. Los ajustes los pide en % del volumen (20 % = ×0,8 ≈ −1,9 dB).
  - Si una pista arranca floja, se le recorta la intro [DECISIÓN].
  - **Licencia:** conectar el canal en Epidemic y **publicar antes de que acabe la suscripción o la prueba**. El plan Creator no cubre anuncios pagados.
- **Mezcla final:** ganancia fija hasta **−16,5 LUFS** y luego `alimiter=limit=0.79:attack=5:release=50:level=false`. **Nunca `loudnorm`.**

## 10. Subtítulos
- Estilo de «yt defg»: **Helvetica Neue 67 px, blanco**, sombra `0 2px 8px rgba(0,0,0,.75)`, una línea abajo (caja en top 905, alto 110) [DECISIÓN].
- **Palabra clave:** una por frase, en **New York Italic** (×1,08) dentro de un recuadro azul (fondo `rgba(32,72,152,.55)`, borde `#5888E0`) con dos tiradores.
- **Solo en momentos clave:** una frase lleva subtítulo solo si va **entera sobre la cara a pantalla completa** y dura **≥ 1 s**. Nunca uno que aparece y desaparece [DECISIÓN].
- Nunca repetir a la vez lo que ya dice un gráfico [DECISIÓN].

## 11. Tipografía
- **Hanken Grotesk 700:** titulares y cifras.
- **Spline Sans Mono 500:** etiquetas en MAYÚSCULAS con mucho espaciado.
- **Newsreader Italic 500** (cursiva): **acento** en una palabra o al final de una frase. Premium = **glass**; la cursiva es solo un acento [DECISIÓN].
- **Helvetica Neue Bold:** números grandes de listas.
- **Roboto:** solo en elementos que imitan a YouTube (banner de suscripción).

## 12. Cierre, YouTube y entrega
- **Pantalla final:** pantalla azul (`#2f74ff → #1157df → #003fab`) con el logo de Maestría y «Mira el siguiente vídeo y suscríbete»; **sin cajas dibujadas** (YouTube pone sus elementos encima, el de suscribirse es un círculo, y el espectador puede ocultarlos); **fundido de 0,5 s**; **6 s**; la música del último bloque sigue debajo al mismo nivel y se apaga al final [DECISIÓN].
- **Duración objetivo:** si se pasa, se acorta el cierre y se acelera todo el vídeo hasta la cifra exacta (YouTube 2: 12:54 = ×1,0199; la voz mantiene el tono con `atempo`) [DECISIÓN].
- **Descripción:** link de la llamada arriba, capítulos con los tiempos reales del vídeo final (primero 0:00, cada uno de 10 s o más).
- **Miniatura** (Codex): se parte de la cara de `retrato.jpg` y de las miniaturas propias como referencia de estilo; texto en Helvetica/Arial Bold con franja; traje; **cada intento con un prompt completo desde cero**, nunca corrección sobre corrección; los pagos que aparezcan tienen que ser **reales** [DECISIÓN].

## 13. Flujo de trabajo y código
1. **Un proyecto por minuto** (copiar el último minuto como base). En cada uno: `trabajo/palabras.json` (palabras con tiempo), `trabajo/spec.txt` (frases con `|`, la clave entre `*…*`) y `acortar_pausas.py`.
2. **Escenas** en `scenes_b.py` (una por frase, atadas a sus palabras); pantallas azules en `textcards.py`; motions en `motions.py`. `bash ~/.config/crear-videos/py build.py` y revisión con `npx hyperframes@0.8.114 snapshot --at …`: centrado, sin destellos, nada encima del micro, nada vacío.
3. **Antes de cambiar un diseño, un fotograma al presentador**; si pregunta «¿qué opinas?», responder y esperar.
4. **Render:** el primero del minuto, completo y por **trozos de ~20 s** cortados en inicios de escena (`proyecto/renders/trozos.sh` + `../herramientas/unir_trozos.py`), con `PRODUCER_LOW_MEMORY_MODE=false` y un vigilante que repite el trozo si se cuelga. **Después, nunca otro completo:** solo el tramo que cambia con `../herramientas/ventana.py <proyecto> A B salida.mp4` (A en un hueco entre escenas) y se pega fotograma a fotograma; si cambian los sonidos del tramo, también se cambia su audio igualando el volumen. **Un solo render a la vez**; no envolver `ventana.py` en otro `nice`.
5. **Montaje:** `lista-completo.txt` + `ffmpeg -f concat -c copy`. Luego la música por bloques nivelada (§9), el cierre (§12) y la mezcla final.
6. **Comprobar antes de entregar:** número de fotogramas, que imagen y audio duren lo mismo, LUFS, fotogramas en las uniones, y escuchar o medir la música por bloques.

| Archivo | Qué hace |
|---|---|
| `build.py` | Cámara (zoom, lateral, círculo, blur, apertura), recortes detrás del presentador, subtítulos, motions, sonidos e `index.html`. **Hay 10 versiones (una por minuto); la más completa es la del minuto 10.** |
| `scenes.py` | Base común: colores, fuentes, CSS y JS compartidos (`IN`, `POP`, `CNT`, `SCENE_IN`…). Igual en los 10 minutos. |
| `scenes_b.py` | Escenas del minuto y piezas reutilizables (`gin`, `gout`, `s_card`, `stats_card`, `broll`, `panel`, `biblio`, `mini_ruta`…). |
| `textcards.py` / `motions.py` | Pantallas azules / motions blancos (`chip`, `flag`, `flags`, `bubble`, `bulb`, `subs`…). |

### Motor único y herramientas (desde)
- **Plantilla para un vídeo nuevo:** `../motores/motor-youtube/plantilla/`. Se copia como `proyecto/` del vídeo nuevo, junto a una carpeta `trabajo/` con `palabras.json` y `spec.txt`, y se ponen en `assets/` `aroll.mp4`, `voz.m4a`, `palabras.json`, `recorte/` y `broll/`.
  - `piezas.py`: todas las piezas reutilizables y los iconos, **copiados tal cual** de YouTube 2. Comprobado: el minuto 10 generado con `piezas.py` sale **idéntico byte a byte** al original.
  - `build.py` (el del minuto 10, con `CUTOUTS = []`), `scenes.py`, `motions.py` (con el banner `subs`), `textcards.py` y `scenes_b.py` vacíos con ejemplos; fuentes (incluida Roboto), efectos y los 21 logos.
- **Herramientas** en `../herramientas/`:
  - `ventana.py`: renderizar solo un tramo [A, B].
  - `pegar.py`: pegar tramos renderizados en el vídeo base al fotograma exacto.
  - `unir_trozos.py`: juntar los trozos del primer render.
  - `musica_bloques.py` + `musica_bloques.ejemplo.json`: música por bloques, nivelación, volumen por bloque, cierre y mezcla (§9). Comprobado: con el ejemplo da los niveles de YouTube 2 con ±0,1 dB.

## 14. Errores que no se repiten
- Decidir diseño sin preguntar; entregar algo sin haberlo comprobado.
- Motions descentrados, gordos, pegados a la cara, vacíos o todos iguales.
- Blur sin nada encima; panel o subtítulo que aparece y desaparece; un fotograma muerto.
- B-rolls genéricos, de baja calidad o desincronizados de la frase.
- Elegir música por etiquetas sin que el presentador la escuche.
- Rehacer renders completos por cambios pequeños.

## 15. Reglas aprendidas en vídeos reales (valen para todo el Estilo Maestria)
Salen de las correcciones de las revisiones de vídeos reales. Si chocan con una regla de arriba, manda la de arriba.

**Composición**
- **Centrado:** título + objeto forman **un bloque**, y ese bloque va centrado (±30 px) en la zona libre: la pantalla entera en b-rolls y blurs (centro vertical ≈ 540 px), o el hueco que deja la cámara en lateral o círculo. Solo se deja sitio abajo si esa escena lleva subtítulo. Las notificaciones son la excepción: van en una esquina.
- **Tamaño y aire:** ≥100 px de aire a la cámara y a los bordes; 28–32 px entre tarjetas. Títulos ~40 px/600, cifras 36–46 px/600–700, etiquetas 18–24 px; 800 solo para cifras héroe. Elementos hermanos del mismo alto y alineados.
- **Nada encima del micrófono** (entra por la izquierda): los motions sobre la cara van a la derecha. Si no caben, se hacen más pequeños; no se mueven a la izquierda.
- **Detrás del presentador:** en las escenas de cristal, el panel va detrás de su recorte (webm con alfa, `CUTOUTS` en `build.py`), y la cabeza o el hombro solo tapan el **borde**. Comprobarlo también con el zoom al 116 %.
- **Cada motion, distinto y fino:** una idea visual propia (iconos SVG, contadores, trayectorias), nada amontonado ni encima del texto, ningún hueco en blanco, iconos que se entiendan a la primera. Nada de tarjetas blancas con listas y emojis.
- **De una referencia se sacan ideas, no el estilo:** se rehacen con los materiales del vídeo actual para que todo sea coherente. Si no está claro si se quiere copiar o inspirarse, se pregunta.

**Ritmo**
- **~10 s de cara hablando antes de cada transición**, rotando el tipo de plano: fondo azul → cara central → lateral izquierda → círculo → lateral derecha → central, con blurs entre medias.
- **Sincronía:** cada escena entra 0,3–0,5 s antes de la primera palabra que ilustra; su primer elemento entra con el cristal. Ningún panel se ve vacío.
- **Sin destellos de cara:** entre dos piezas a pantalla completa no puede asomar la cara un instante. Si queda un hueco de cara de menos de ~1 s, se alarga la primera escena. Las escenas entran sin transparencia.
- **Zoom de la cara solo al acabar una frase con punto**, en la palabra que abre la siguiente; nunca a mitad de frase.

**B-rolls y subtítulos**
- **B-rolls:** 3–6 por minuto como mucho, enseñados antes en una hoja de fotogramas para que el usuario elija. Cada uno 0,5–2 s limpio y luego blur fuerte con el motion encima. Cifras y cálculos van como blur o cristal, no como b-roll. (Mixkit funciona; Pexels y Pixabay dieron error 403.)
- **Subtítulos solo en momentos clave:** una frase lleva subtítulo solo si va entera sobre la cara a pantalla completa y dura ≥1 s. Después de renderizar se revisa la franja de subtítulos buscando textos de ≤10 fotogramas.
- **Subtítulos horizontales (1920×1080):** línea base y≈985, 67 px, blanco puro, sombra negra en todas las palabras salvo las que van dentro del marco azul. Fuentes: Helvetica Neue + New York Italic.

**Sonido**
- Para confirmaciones y logros, `ding.m4a`; **no** `success.mp3`. Evitar tachados «raros» con sonidos que no pegan.
- La intro de Maestría va con su volumen tal cual.
- Texto junto al logo de Maestría: **Didot Bold** (solo existe en macOS; en Windows, la serif más parecida y avisar). El resto de textos, Hanken.

**Render y cambios**
- **Cambio pequeño = operación mínima:** unir con `ffmpeg -f concat -c copy` si coinciden los formatos; cambiar solo el audio con `-c:v copy`; cambiar un tramo renderizando solo ese tramo (`../herramientas/ventana.py`) y pegándolo (`../herramientas/pegar.py`). «Renderiza el vídeo completo» significa «entrégamelo montado», no volver a renderizarlo entero.
- Después de unir: duración = suma de las partes, sincronía con `ffprobe`, 2–3 s alrededor de la unión sin errores y un fotograma justo después del corte.
- **Renders largos por trozos de ~20 s** cortados en inicios de escena, con `PRODUCER_LOW_MEMORY_MODE=false` (en un ordenador de 8 GB pasó de ~7,7 a ~17 fotogramas/s) y un vigilante que repite el trozo si el registro pasa 45 s sin moverse. Si un render se corta, regenerar `index.html` con `build.py`.
- Nada de `backdrop-filter: blur()` con recortes webm: el cristal es degradado translúcido + borde + brillo.
