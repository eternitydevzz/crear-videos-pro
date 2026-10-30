---
name: adaptar-fotos
description: Deja fotos listas para subir a Instagram, Facebook o TikTok como si las hubiera hecho un iPhone 18 Pro Max. Mantiene el tamaño original, reduce el ruido solo si hace falta, guarda en JPEG calidad 100 con perfil Display P3, borra todos los metadatos (incluido el manifiesto C2PA de AI) y escribe datos de cámara de iPhone 18 Pro Max variados por foto, fecha y hora, dimensiones reales y ubicación (por defecto Newark, New Jersey). Úsala siempre que el usuario pase fotos y diga "adapta esta", "adáptalas para subir", "quita lo de AI", "que parezca de iPhone", "ponles datos de cámara" o parecido. Para videos sigue usando adaptar-para-subir.
---

# Adaptar fotos

Cada foto que pases sale en `<carpeta>/` lista para subir y el original queda en `<carpeta>_originales/`.

## Antes de empezar: preguntar siempre la fecha

Pregunta al usuario **qué fecha o rango de fechas** quiere en las fotos. Nunca la inventes sin preguntar. (Solo si dice "la que tú veas", eliges tú: días recientes y anteriores a hoy, repartidos, sin que una misma persona aparezca en dos países el mismo día.)

## Pasos

1. Mira cada foto y decide su **escena**: `dia` (exterior con sol), `atardecer` (exterior con luz suave o sombra), `interior` (dentro con luz de día) o `noche` (noche o interior oscuro). La escena decide la hora, la apertura, la exposición y el ISO, para que cuadren con la luz de la foto.
2. Ubicación: Newark, NJ por defecto. Si la foto muestra claramente otro lugar (o el usuario lo dice), pásalo en `lugar` con `zona` (por ejemplo `Europe/Rome`). Si dudas, pregunta.
3. Escribe el plan en una carpeta temporal (`plan.json`):
   ```json
   [{"nombre": "jet-noche", "origen": "/ruta/foto.jpg", "escena": "noche", "fecha": "2026-10-22"},
    {"nombre": "terraza", "origen": "/ruta/t.jpg", "escena": "atardecer", "fecha": "2026-10-04",
     "lugar": {"ciudad": "Verona", "estado": "Veneto", "pais": "Italy", "codigo": "IT",
               "lat": 45.4390, "lon": 10.9947, "zona": "Europe/Rome"}}]
   ```
   `fecha` puede ser solo el día (el script elige la hora según la escena) o `"AAAA-MM-DD HH:MM:SS"`. Si la foto venía como adjunto del chat, cópiala primero a la carpeta de subida y usa esa ruta.
4. Ejecuta:
   ```bash
   bash ~/.config/crear-videos/py "${CLAUDE_PLUGIN_ROOT}/skills/adaptar-fotos/scripts/adaptar_fotos.py" plan.json "<carpeta de subida>"
   ```
5. Comprueba los datos (en Windows: `exiftool -Model -FocalLength -FNumber -ProfileDescription -ImageWidth -GPSLatitude foto.jpg`; en el Mac, como lo ve Finder: `mdls -name kMDItemAcquisitionModel -name kMDItemFocalLength -name kMDItemFNumber -name kMDItemProfileName -name kMDItemPixelWidth -name kMDItemLatitude foto.jpg`) y que "rastros AI" sea 0 en todas. Si no, no darlo por bueno.
6. Responde con lo malo primero, una tabla por foto (tamaño, fecha, f/, exposición, ISO, si se filtró) y el límite de siempre.

## Reglas fijas (decididas por el equipo)

- **Nunca ampliar ni reducir.** Tamaño original siempre.
- **Ruido solo si hace falta**: se filtra si los cuadraditos de compresión pasan de 1,2. A una foto limpia el filtro solo le quita nitidez.
- **Cámara: siempre iPhone 18 Pro Max** con los datos de Apple, no los de la foto: focal **24 mm** (cámara principal, apple.com/iphone-18-pro/specs), apertura ƒ/1.8 de día y ƒ/1.48 con poca luz (las del modelo: 1.48, 1.8, 2.8, 4.0).
- **Variar siempre**: hora, exposición, ISO y subsegundos cambian en cada foto y en cada ejecución.
- **Perfil Display P3** y JPEG calidad 100. El color se convierte, no se reinterpreta (medido: ±2/255).
- Nada de LensModel ni versión de iOS: Apple no publica esos valores para el 18 Pro Max y no se inventan.

## El límite, siempre y sin maquillar

Si la foto lleva una marca de agua invisible en los píxeles, no hay detector para confirmar que desapareció. Meta hoy etiqueta por metadatos (C2PA, IPTC) y eso queda borrado. No está comprobado si Meta mira los datos de cámara ni si Instagram los conserva al subir.
