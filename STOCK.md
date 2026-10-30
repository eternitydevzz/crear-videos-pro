# STOCK

Todo lo que el equipo puede usar en sus vídeos: música, efectos de sonido, motions de HyperFrames, logos, fuentes, plantillas de estilo y vídeos de referencia. Dentro del plugin está en `${CLAUDE_PLUGIN_ROOT}/stock/` (Claude lo encuentra solo).

> **Uso:** repo privado del equipo. La música comercial, las fuentes de pago y los logos de marcas son para uso interno: no los redistribuyas ni los subas a sitios públicos.

## Contenido
- [Carpetas](#carpetas)
- [Estilos](#estilos)
- [Origen](#origen)
- [Detalle por carpeta](#detalle-por-carpeta)

## Carpetas

| Carpeta | Qué hay | Tamaño |
|---|---|---|
| `musica/` | 17 pistas (instrumentales y bandas sonoras de lanzamientos de HyperFrames) | 55 MB |
| `sfx/` | Efectos cortos ordenados por tipo (click, ding, impacto, subidas, teclado, whoosh, brillos, otros) | 7,5 MB |
| `motion/` | Proyectos de HyperFrames con escenas HTML listas para copiar o inspirarse | 3,3 MB |
| `logos/` | Logos de marcas y herramientas (SVG y PNG) | 7,3 MB |
| `fuentes/comunes/` | Fuentes que valen en Mac y Windows (Inter, Figtree, JetBrains Mono, Archivo Black…) | |
| `fuentes/apple/` | `NewYorkItalic.ttf` y `refsans-medium.ttf` (una Helvetica). Solo para Mac | |
| `fuentes/windows/` | Sustitutas en Windows: Newsreader (por New York) y Hanken Grotesk | |
| `plantillas/` | Plantillas y biblioteca de estilos de HyperFrames. Sus `CLAUDE.md` y `AGENTS.md` se renombraron a `*.referencia.md` para que Claude no los tome como instrucciones | 4,5 MB |
| `referencias-videos/` | 4 vídeos de ejemplo de HyperFrames y el proyecto completo `sfx-music-launch/` | 134 MB |

## Estilos

Además del stock, en `estilos/`:
- **`Estilo Maestria/`**: las 4 fichas del equipo (`youtube/`, `formacion/`, `whatsapp-comunidad/`, `edicion-claude/` con las escenas g01–g12), los 2 motores (`motores/motor-youtube/`, `motores/motor-formacion/`) y las herramientas (`herramientas/`).
- **`creadores/`**: 6 estilos analizados de otros creadores (`albert-explosivo`, `animationviral`, `enrique-mex`, `juanpablo`, `minecraft`, `viral2`), cada uno con su `estilo.md` y sus mosaicos.

## Origen

`_origen.txt` dice de dónde sale cada archivo: la mayoría del *HyperFrames student kit* y de los proyectos de lanzamiento de HyperFrames. A los archivos se les quitaron los metadatos (autor, programa, plantilla de Canva) y se renombraron sin espacios; las rutas de `_origen.txt` son las de antes de ordenarlos.

## Detalle por carpeta

### musica
| Archivo | Duración |
|---|---|
| `Central-Cee-Doja-(Instrumental).mp3` | 97.5 s |
| `Every-Living-Breathing-Moment-Clavier-(Piano-Instrumental).mp3` | 146.5 s |
| `Every-Living-Breathing-Moment-Taylor-Do-Blues.mp3` | 127.4 s |
| `LoVibe.-a-good-man-with-a-broken-heart.mp3` | 118.7 s |
| `Me-and-the-Devil-(Instrumental).mp3` | 182.6 s |
| `Radiohead-Everything-In-Its-Right-Place-(Instrumental).mp3` | 267.6 s |
| `The-Weeknd-Playboi-Carti-Timeless-(Instrumental).mp3` | 256.0 s |
| `We-Do-What-We-Want-(Viral-Instrumental-Slowed)-aurelia-dopuu.mp3` | 197.2 s |
| `frame-md-launch-storyboard-framefinal.mp3` | 53.5 s |
| `hyperframes-launch-music.mp3` | 49.8 s |
| `inspector-launch-soundtrack.mp3` | 45.0 s |
| `k3-promo-audio.m4a` | 16.6 s |
| `sfx-music-launch-soundtrack.mp3` | 33.8 s |
| `spacex-launch-launch-music-trimmed.mp3` | 131.7 s |
| `video-projects-music-2.mp3` | 166.1 s |
| `video-projects-music.mp3` | 78.0 s |
| `video-projects-warm-pad.mp3` | 30.0 s |

### sfx
| Carpeta | Archivos (duración) |
|---|---|
| `brillos-magia/` | `scan-scifi-reveal.mp3` (5.3 s), `sfx-twinkle.mp3` (0.5 s), `sparkle-magic.mp3` (3.6 s), `sparkle-twinkle.mp3` (1.8 s), `sparkle.mp3` (3.6 s) |
| `click/` | `click-2.mp3` (0.3 s), `click-3.mp3` (0.3 s), `click-sfx.mp3` (0.6 s), `click.flac` (0.2 s), `click.mp3` (0.1 s), `heygen-liquid-pop-sfx.wav` (6.0 s), `mouse-click.mp3` (0.4 s), `pop-2.mp3` (0.3 s), `pop.mp3` (0.3 s), `toggle.mp3` (0.2 s) |
| `ding/` | `bell-ping.mp3` (1.0 s), `bell.mp3` (1.1 s), `chime-metallic.mp3` (1.9 s), `chime-soft.mp3` (1.2 s), `chime.mp3` (1.3 s), `ding.flac` (0.9 s), `jingle-stinger.mp3` (1.6 s), `jingle-tunes-shimmer.mp3` (9.3 s), `success.mp3` (1.8 s), `ux-chime.mp3` (0.6 s) |
| `impacto/` | `bass-drop-1.mp3` (2.1 s), `honk.mp3` (1.4 s), `impact.flac` (2.3 s) |
| `otros/` | `Wow.wav` (2.6 s), `sfx-production.wav` (5.0 s) |
| `subidas/` | `Riser.mp3` (8.1 s), `depegue.flac` (1.6 s), `riser-2.mp3` (4.4 s), `riser-build.mp3` (3.5 s), `riser-dark-eerie.mp3` (3.8 s), `riser-soft-dreamy.mp3` (6.6 s), `subida.flac` (0.8 s) |
| `teclado/` | `keyboard-typing.mp3` (8.1 s), `keys.mp3` (3.0 s), `teclado-1.flac` (1.1 s), `teclado-2.flac` (0.7 s), `teclado-3.flac` (0.7 s), `teclado-4.flac` (0.7 s), `tokens.mp3` (3.6 s), `type-short.mp3` (0.9 s), `type.mp3` (1.5 s), `typenew.mp3` (0.1 s) |
| `whoosh/` | `sfx-whoosh-2.mp3` (0.4 s), `sfx_whoosh_min1.flac` (0.5 s), `swish.mp3` (0.5 s), `whoosh-morph.mp3` (1.0 s), `whoosh-slide.mp3` (0.3 s), `whoosh.mp3` (0.7 s) |

### referencias-videos
| Archivo | Duración |
|---|---|
| `ais-live-ad.mp4` | 49.7 s |
| `curiosity-reel-1.mp4` | 45.6 s |
| `curiosity-reel-2.mp4` | 32.0 s |
| `youtube-showreel.mp4` | 15.0 s |

### motion
| Proyecto | Escenas HTML |
|---|---|
| `HF-heygen-stripe/` | 9 |
| `aisoc-app-release/` | 11 |
| `aisoc-hype/` | 7 |
| `aisoc-lesson-5-1/` | 9 |
| `claude-design-send-hyperframes-launch/` | 6 |
| `claude-edit-intro/` | 7 |
| `claude-paper-launch/` | 11 |
| `cloud-render-launch/` | 10 |
| `codex-five-hour-limit-replica/` | 3 |
| `figma-launch/` | 11 |
| `frame-md-launch-storyboard/` | 9 |
| `golden-ratio-demo/` | 8 |
| `hyperframes-launch/` | 16 |
| `hyperframes-sizzle/` | 33 |
| `linear-promo-30s/` | 8 |
| `liquid-brand-refraction/` | 6 |
| `may-shorts-18/` | 10 |
| `may-shorts-19/` | 13 |
| `may-shorts-6/` | 10 |
| `pr-to-video-launch/` | 10 |
| `sfx-music-launch/` | 7 |
| `spacex-launch/` | 12 |
| `texture-launch-video/` | 1 |
| `timeline-launch/` | 10 |
| `variables-launch/` | 9 |
| `vfx-heygen-combined/` | 1 |
| `website-to-hyperframes/` | 2 |

### logos
`AIS-Logo-PNG.png`, `Claude_AI_symbol.svg`, `bg-stripe.png`, `claude-logo.png`, `claude.png`, `claude.svg`, `clickup-mark.png`, `codex.png`, `codex.svg`, `cursor-2.png`, `cursor-grab-2.svg`, `cursor-grab.svg`, `cursor-point.svg`, `cursor.png`, `cursor.svg`, `figma-cursors.svg`, `figma-logo-pieces.svg`, `figma-logo-pills.svg`, `gemini.png`, `heygen-hyperframes-lockup.png`, `heygen-lockup-official.svg`, `heygen-logo-2.png`, `heygen-logo-2.svg`, `heygen-logo-3.png`, `heygen-logo.png`, `heygen-logo.svg`, `heygen-prism-official.svg`, `heygen-wordmark-official.svg`, `hf-logo-light.png`, `hf-logo.svg`, `hyperframes-logo.svg`, `linear-logo.svg`, `linear-symbol.svg`, `nav-logo-lottie.svg`, `nav-logo-wrap.svg`, `openai.svg`, `stripe-logo.png`, `stripe-raw.png`, `tesla-chart.svg`, `tesla-logo.svg`, `tesla-road.svg`

### fuentes
- **comunes/**: `691cda762a35b6bc5a28ffaa_JetBrainsMono-Regular.woff2`, `69971a00a3295036497e1a28_AnthropicSans-Roman-Web.woff2`, `69971a016067bf14b9b8f48d_AnthropicSans-Italic-Web.woff2`, `69971a1551eb6cda0d656e8a_AnthropicSerif-Roman-Web.woff2`, `69971a15a9fb8c1107a3570e_AnthropicSerif-Italic-Web.woff2`, `69971a2e55d24d61bc045b1a_AnthropicMono-Roman-Web.woff2`, `69971a2eb93743112c30fe9c_AnthropicMono-Italic-Web.woff2`, `ABCSolarDisplay-Bold.otf`, `ABCSolarDisplay-Bold.woff2`, `ArchivoBlack-400.woff2`, `ArchivoBlack-fs.woff2`, `BungeeShade-Regular.woff2`, `Figtree-Variable.woff2`, `GalaxieCopernicus-Book.woff2`, `Heebo-900.ttf`, `Inter-400.ttf`, `Inter-500.ttf`, `Inter-600.ttf`, `Inter-Variable-2.woff2`, `Inter-Variable.woff2`, `JetBrainsMono-Variable.woff2`, `SplineSansMono-normal-400-latin-53329b.woff2`, `SplineSansMono-normal-500-latin-ext-62a811.woff2`, `TTNormsPro-Bold.woff2`, `TTNormsPro-DemiBold.otf`, `TTNormsPro-Medium.woff2`, `TTNormsPro-Regular.woff2`, `TTNormsPro-SemiBold.woff2`, `TT_Norms_Pro_Mono_Regular.woff2`
- **apple/**: `NewYorkItalic.ttf`, `refsans-medium.ttf`
- **windows/**: `HankenGrotesk-normal-600-latin-ext-d9a6a0.woff2`, `HankenGrotesk-normal-600-latin-fe1634.woff2`, `Newsreader-italic-400-latin-78bd98.woff2`, `Newsreader-italic-500-latin-ext-e36b6b.woff2`, `Newsreader-normal-600-latin-ext-7a09be.woff2`, `Newsreader-normal-600-latin-f0c28d.woff2`

### plantillas
`style-library/01-vox-explainer/`, `style-library/02-kallaway/`, `style-library/_blueprint/`, `style-templates/dark-graph-paper-template/`, `style-templates/left-glass-popout/`
