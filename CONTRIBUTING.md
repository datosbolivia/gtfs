# Guía de contribución

¡Gracias por tu interés en colaborar con Datos Bolivia! Este documento te guiará a través de los pasos necesarios para comenzar a trabajar en el proyecto.

## Introducción

Este repositorio refleja el trabajo comunitario de Datos Bolivia en torno a los datos de transporte público.

El objetivo principal es **publicar datos en formato GTFS** para que los [mapas en línea](https://mobilitydatabase.org/gtfs-feature-tracker) (Google Maps, Apple Maps y todos los mapas "libres") incluyan los transportes públicos en los cálculos de itinerario.

Más información sobre el formato GTFS (en español) en la página https://gtfs.org/es/getting-started/.

## Comienza aquí

### Requisitos previos

Antes de empezar, asegúrate de tener instalado:

- **Git** - para clonar y trabajar con el repositorio
- **Python 3.8+** - para ejecutar los scripts de validación
- **Java (JRE/JDK 11+)** - para ejecutar el validador GTFS de MobilityData
- **Make** - para ejecutar los comandos de construcción y validación
- **pip** - el gestor de paquetes de Python (generalmente viene con Python)

### Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/datosbolivia/gtfs.git
   cd gtfs
   ```

2. **Instala las dependencias de Python:** (asegúrate de estar en un entorno virtual si lo deseas)

   ```bash
   pip install -r scripts/requirements.txt
   ```

3. **Configura el proyecto:**

   ```bash
   make
   ```

   Este comando:
   - Instala los hooks de pre-commit
   - Valida el formato de los archivos CSV
   - Genera los GTFS y el sitio web
   - Valida el resultado

4. **Verifica que todo funcione:**

   Abre `dist/index.html` en tu navegador para ver el sitio generado.

### Herramientas de desarrollo

El proyecto usa las siguientes herramientas para mantener la calidad de los datos:

- **Pre-commit hooks** - validan y formatean los datos automáticamente
- **GTFS Validator** - valida los archivos GTFS según el estándar de MobilityData
- **CSV Linter** - verifica el orden de columnas y el formato de los archivos

Todas estas herramientas se configuran automáticamente con `make setup-hooks`.

## Flujo de trabajo

### Estructura del repositorio

```
.
├── data/              # Archivos de datos GTFS (CSV)
├── scripts/           # Scripts para generar y validar GTFS
├── Makefile           # Comandos de construcción
├── README.md          # Información del proyecto
└── CONTRIBUTING.md    # Esta guía
```

### Cómo contribuir

1. **Crea una rama para tu cambio:**

   ```bash
   git checkout -b nombre-descriptivo-del-cambio
   ```

2. **Realiza tus cambios** en los archivos de `data/`

3. **Valida tus cambios localmente:**

   ```bash
   make lint           # Verifica el formato
   make build          # Genera los GTFS
   make validate-gtfs  # Valida con MobilityData
   ```

   O simplemente:

   ```bash
   make  # Ejecuta todos los pasos anteriores
   ```

4. **Haz commit de tus cambios:**

   ```bash
   git add .
   git commit -m "Descripción clara del cambio"
   ```

   Los hooks de pre-commit se ejecutarán automáticamente y corregirán el formato si es necesario.

5. **Sube tu rama:**

   ```bash
   git push origin nombre-descriptivo-del-cambio
   ```

6. **Abre una Pull Request (PR)** en GitHub

### Validación de cambios

- Cada modificación debe hacerse mediante una **Pull Request (PR)**, lo que permite validar los cambios con una GitHub Action antes de modificar el GTFS.
- Los hooks de pre-commit validan los cambios localmente antes de hacer push.
- **Importante:** No mergear una PR sin haber validado manualmente el GTFS antes, para evitar que se publique un GTFS con errores.

Para validar un GTFS manualmente antes de hacer merge:

1. Genera el GTFS con `make build`
2. Verifica el GTFS en:
  - https://gtfs-validator.mobilitydata.org
  - https://ttezer.github.io/gtfs-analyzer/
  - https://validator.blinktag.com/
  - https://transport.data.gouv.fr/validation (con precaución porque no parece muy actualizado, pero detecta errores en la ubicación de los stops por ejemplo)
  - https://gtfsvtor.mecatran.com/utw-test/web/pub/gtfsvtor (con precaución porque no parece muy actualizado, pero detecta errores en la ubicación de los stops por ejemplo)
  - https://reflect.foursquareitp.com/validator/ (cuidado: requieren tu email)

También se puede probar el cálculo de itinerario localmente con [Motis](https://github.com/motis-project/motis#quick-start):

- crear un directorio dedicado
- descargar el binario de Motis desde la página de [releases](https://github.com/motis-project/motis/releases) y extraerlo en la carpeta `tar -xf motis...tar.bz2`
- descargar el dump OSM de Bolivia desde [Geofabrik](https://download.geofabrik.de/south-america/bolivia-latest.osm.pbf): ver https://download.geofabrik.de/south-america/bolivia.html para más detalles.
- copiar el archivo GTFS en el mismo directorio
- ejecutar los comandos:

  ```bash
  ./motis config my.osm.pbf gtfs.zip  # generates a minimal config.yml
  ./motis import                      # preprocesses data
  ./motis server                      # starts a HTTP server on port 8080
  ```
- entrar a http://localhost:8080/ y usar generar un itinerario.

## Comandos disponibles

### Make

| Comando | Descripción |
|---|---|
| `make` (o `make all`) | Ejecuta: setup-hooks, lint, build y validate-gtfs |
| `make build` | Genera el sitio (GTFS + archivos `index.html`) en `dist/` |
| `make lint` | Verifica el orden de columnas y formato de los archivos CSV |
| `make fix-columns` | Corrige automáticamente el orden de columnas y formato |
| `make validate-gtfs` | Valida los GTFS con el validador de MobilityData |
| `make setup-hooks` | Instala los hooks de pre-commit |
| `make create_gtfs` | Genera los archivos GTFS en `dist/` |
| `make create_indexes` | Genera los archivos `index.html` |
| `make clean` | Elimina archivos temporales (`dist/`, `.cache/`) |

### Pre-commit hooks

El repositorio usa [pre-commit](https://pre-commit.com/) para validar y formatear los datos automáticamente.

**Hooks configurados:**

| Hook | Cuándo se ejecuta | Descripción |
|---|---|---|
| `gtfs-csv-lint` | antes de commit (pre-commit) | Corrige automáticamente el orden de columnas y formato de los archivos `data/*.txt` |
| `gtfs-validator` | antes de push (pre-push) | Valida los GTFS con el validador de MobilityData |

> El hook `gtfs-csv-lint` aplica correcciones automáticas. Si modifica archivos, el commit será rechazado para que revises y añadas los cambios corregidos con `git add` antes de volver a hacer commit.

## Buenas prácticas

- **Idioma:** El idioma principal de los archivos de datos es el castellano (es).

- **Alcance:** Un GTFS corresponde a una sola agencia de transporte (o grupo coherente de agencias). Esto permite delegar la responsabilidad de la publicación de los datos a la agencia correspondiente.

- **Calidad:** Se recomienda empezar con lo mínimo, pero con calidad, y luego ampliar si se puede. Para cada GTFS, trataremos de analizar y publicar las funcionalidades incluidas y las fechas de actualización.

- **Validación:** El GTFS será generado, validado y publicado automáticamente usando una GitHub Action. El esfuerzo principal está en la generación y actualización de los datos.

## Alternativa: editores en línea

Alternativamente, puedes usar un editor en línea para editar los archivos de datos, por ejemplo https://gtfs-viz-production-f1a4.up.railway.app (https://github.com/gabrielAHN/gtfs-viz).

Hay más herrammientas en https://gtfs.org/resources/overview/ o github.com/andredarcie/awesome-gtfs.

## Cómo colaborar

Existen varias formas de colaborar:

- **Únete al grupo** [Datos Bolivia en Telegram](https://t.me/+AWyKECHAM9IyZWZh)
- **Comenta en** https://github.com/public-transport/transitous/issues/2318
- **Abre una issue** en https://github.com/datosbolivia/gtfs/issues (podemos tener una issue por cada proyecto de nuevo GTFS, es decir, por "agencia")

## Publicación

Toda actualización de la rama principal (push en main) genera automáticamente los GTFS y el sitio, y los publica en https://datosbolivia.github.io/gtfs/.

## Dudas o problemas

Si tienes problemas durante la instalación o contribución, abre una issue en el repositorio o contacta al grupo de Telegram.

¡Gracias por tu contribución!
