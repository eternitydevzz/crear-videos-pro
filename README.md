<div align="center">

# Crear Vídeos Pro

**Copia el estilo de edición de cualquier reel y edita tus vídeos con él, con Claude Code y HyperFrames.**

![Mac](https://img.shields.io/badge/Mac-probado-000000?logo=apple&logoColor=white)
![HyperFrames](https://img.shields.io/badge/HyperFrames-0.8.114-5B5BD6)
![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-en%20local-10A37F)
![Claude](https://img.shields.io/badge/Claude%20Code-plugin-D97757?logo=anthropic&logoColor=white)

Un plugin de Claude Code con 5 skills de edición, el Estilo Maestria, 6 estilos de otros creadores y todo el stock del equipo. Transcribe en tu ordenador, sin gastar créditos.

<table>
  <tr>
    <th>📥 El reel de referencia</th>
    <th>✨ El reel hecho con este repo</th>
  </tr>
  <tr>
    <td><img src="docs/img/portada/reel-original.png" alt="Fotograma del reel original de Viral2: gráficos de pixel art con un personaje y tarjetas" width="100%"></td>
    <td><img src="docs/img/portada/mi-reel-fotograma.png" alt="Fotograma del reel «K.O.» hecho con el repo: Claude deja K.O. a LinkedIn en pixel art" width="100%"></td>
  </tr>
  <tr>
    <td align="center"><sub>Original de Viral2, en portugués </sub></td>
    <td align="center"><sub>Mismo estilo, otro tema: «K.O.»</sub></td>
  </tr>
</table>

</div>

---

## 📈 Resultados reales

El reel «K.O.» hecho con este flujo:

| 👁️ Visualizaciones | ❤️ Me gusta | 💬 Comentarios |
|:---:|:---:|:---:|
| **142 mil** | **4.898** | **3.058** |

<table>
  <tr>
    <td width="40%"><img src="docs/img/portada/mi-reel-vistas.png" alt="Captura del reel con 142 mil visualizaciones" width="100%"></td>
    <td><img src="docs/img/portada/mi-reel-likes-comentarios.png" alt="Captura con 4.898 me gusta y 3.058 comentarios" width="100%"><br><br>
    <img src="docs/img/portada/perfil-1.png" alt="Perfil de Instagram cristianews.ai con 31 mil seguidores" width="100%"><br>
    <img src="docs/img/portada/perfil-2.png" alt="Perfil de Instagram josenews.ai con 9.595 seguidores" width="100%"></td>
  </tr>
</table>

Las cuentas que lo usan: **cristianews.ai** (31 mil seguidores) y **josenews.ai** (9.595 seguidores).

## 🎞️ Galería

Motions hechos con este repo:

| | | | |
|:---:|:---:|:---:|:---:|
| <img src="docs/img/galeria/motion-1.jpg" alt="Organigrama de 11 funciones" width="180"> | <img src="docs/img/galeria/motion-2.jpg" alt="Rejilla de reels" width="180"> | <img src="docs/img/galeria/motion-3.jpg" alt="FATALITY: Claude contra CapCut" width="180"> | <img src="docs/img/galeria/motion-4.jpg" alt="Claude contra YouTube" width="180"> |
| <img src="docs/img/galeria/motion-5.jpg" alt="Tomas repetidas en ondas de audio" width="180"> | <img src="docs/img/galeria/motion-6.jpg" alt="Trofeo de viralidad" width="180"> | <img src="docs/img/galeria/motion-7.jpg" alt="Comenta CLASE con gráfica" width="180"> | |

## ▶️ Vídeo de ejemplo

[![Ver el vídeo en YouTube](docs/img/video-miniatura.jpg)](https://www.youtube.com/watch?v=UPa0uNzbH1s&t=83s)

<sub>Haz clic en la imagen: se abre en YouTube en el minuto 1:23.</sub>

## Qué hace

| Skill | Qué hace | Cómo se activa |
|---|---|---|
| 🔍 `crear-estilo-videos` | Pasas el link de un reel y saca una ficha (`estilo.md`) con valores medidos: cortes, ritmo, subtítulos, color, sonido y transcripción | «Copia el estilo de este reel» |
| 🎬 `editar-con-estilo` | Edita tu vídeo a cámara con una ficha: corta silencios, subtítulos palabra a palabra, motions con HyperFrames, música y efectos | «Edita mi vídeo con el estilo Maestria» |
| 🔁 `variaciones-video` | 5 versiones de un vídeo con ganchos, encuadres e inicios distintos, más 5 descripciones | «Hazme 5 variaciones para Trial Reels» |
| 📤 `adaptar-para-subir` | Deja imágenes y vídeos listos para subir: JPEG 1080, sin metadatos, con la ubicación | «Adáptalos para subir» |
| 📸 `adaptar-fotos` | Fotos al tamaño original, en Display P3, con datos de cámara y ubicación | «Adapta estas fotos» |

En Claude Code se llaman con el prefijo del plugin: `/crear-videos-pro:crear-estilo-videos`. También basta con pedirlo con tus palabras.

## Cómo funciona

```mermaid
flowchart LR
    A["🔗 Link de un reel"] --> B["🔍 crear-estilo-videos<br/><i>mide y escribe la ficha</i>"]
    B --> C["📄 estilo.md"]
    D["🎥 Tu vídeo a cámara"] --> E["🎬 editar-con-estilo"]
    C --> E
    E --> F["✂️ Silencios fuera<br/>🗣️ Tiempos por palabra"]
    F --> G["📋 Plan de escenas<br/><i>lo apruebas tú</i>"]
    G --> H["🎞️ Primeros 10 s<br/><i>lo apruebas tú</i>"]
    H --> I["🏁 Vídeo completo"]
    I --> J["🔁 variaciones-video<br/>📤 adaptar-para-subir"]
```

## Cómo encaja todo

```mermaid
flowchart TB
    U["🧑 Tú, en Claude Code"] --> P["🧩 Plugin crear-videos-pro"]
    P --> S["⚙️ skills/<br/>5 skills + _comun"]
    P --> E["🎨 estilos/<br/>Estilo Maestria + creadores"]
    P --> K["📦 stock/<br/>música, sfx, motions, logos, fuentes"]
    S --> H["🎞️ Plugin HyperFrames"]
    S --> W["🗣️ Whisper en local"]
    S --> M["📁 ~/crear-videos/<br/>tus vídeos y tus estilos"]
```

El plugin se sustituye entero al actualizar: **lo tuyo vive fuera**, en `~/crear-videos/` (vídeos y estilos nuevos) y `~/.config/crear-videos/` (ajustes y tu clave).

## Mac y Windows

| | 🍎 Mac | 🪟 Windows 10 / 11 |
|---|---|---|
| **Guía** | [INSTALAR.md](INSTALAR.md#mac) | [INSTALAR.md](INSTALAR.md#windows) |
| **Instalar** | `bash mac/instalar.sh` | `windows\instalar.cmd` |
| **Actualizar** | `bash mac/actualizar.sh` | `windows\actualizar.cmd` |
| **Programas** | Homebrew: ffmpeg, exiftool, yt-dlp, Python, Node, whisper-cpp, gh | winget: ffmpeg (Gyan), ExifTool, yt-dlp, Python 3.13, Node LTS, gh + zip oficial de whisper.cpp |

El plugin solo, dentro de Claude Code (2.1.275 o más), es `/plugin install crear-videos-pro --marketplace eternitydevzz/crear-videos-pro`, pero **sin el instalador las skills no funcionan**: les faltan el Python del equipo, Whisper y el modelo.

**Lo más fácil:** clona el repo, abre Claude Code en la carpeta y dile *«instálame esto»*. Sigue [INSTALAR.md](INSTALAR.md) y te dice lo que tienes que hacer tú (contraseña del Mac, iniciar sesión en GitHub, tu clave).

## Lo que necesitas

| | |
|---|---|
| 🤖 **Claude Code** con un plan de pago | Pro, Max, Team o Enterprise. El plan gratis no incluye Claude Code |
| 🐙 **Acceso al repo** | Es privado: acepta la invitación y conecta GitHub con `gh auth login` |
| 🔑 **Tu clave de [ScrapeCreators](https://scrapecreators.com)** (opcional) | Solo para bajar un reel cuando yt-dlp falla. Cada persona usa la suya |
| 💾 **~1,2 GB libres** | ~640 MB del plugin (Claude Code guarda dos copias) + 488 MB del modelo de Whisper |

## Estructura

```
.claude-plugin/   el plugin y su marketplace
skills/           las 5 skills y _comun/ (código común y comprobar.py)
estilos/          Estilo Maestria/ (4 fichas, 2 motores, herramientas) y creadores/ (6 estilos)
stock/            música, sfx, motions, logos, fuentes, plantillas y vídeos de referencia
mac/  windows/    instalar y actualizar
docs/             flujo.md e imágenes del README
pruebas/          comprobación de enlaces
```

- [INSTALAR.md](INSTALAR.md): instalación paso a paso.
- [STOCK.md](STOCK.md): qué hay en el stock y en los estilos.
- [CLAUDE.md](CLAUDE.md): el manual del repo para Claude.
- [docs/flujo.md](docs/flujo.md): el flujo de trabajo completo.

## Lo que no hace

- No publica en Instagram ni en YouTube.
- No escucha el audio: lo mide. Lo que digas tú de la música y los sonidos manda.
- No sustituye tu ojo: hay que aprobar el plan, los primeros 10 segundos y cada pasada.
- No va rápido en un ordenador de 8 GB: los renders largos se hacen por trozos.
- La música, las fuentes de pago y los logos del stock son para uso interno del equipo.

## Actualizar

```bash
bash mac/actualizar.sh
```

En Windows: `windows\actualizar.cmd`. Después, abre una sesión nueva de Claude Code.

## Versiones probadas

| Pieza | Versión |
|---|---|
| macOS | 26.6.2 |
| Claude Code | 2.1.296 |
| HyperFrames | 0.8.114 |
| ffmpeg | 9.0.2 |
| whisper.cpp | 1.9.4 |
| Python | 3.14.7 · Pillow 13.0.0 · numpy 2.5.4 |
