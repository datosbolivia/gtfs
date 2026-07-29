# Datos de transporte público en Bolivia

Este repositorio refleja el trabajo comunitario de Datos Bolivia en torno a los datos de transporte público.

El objetivo principal es **publicar datos en formato GTFS** para que los [mapas en línea](https://mobilitydatabase.org/gtfs-feature-tracker) (Google Maps, Apple Maps y todos los mapas "libres") incluyan los transportes públicos en los cálculos de itinerario.

Más información sobre el formato GTFS (en español) en la página https://gtfs.org/es/getting-started/.

## Estado del proyecto

El proyecto está empezando. Los primeros pasos son:

1. realizar un inventario de los datos e iniciativas existentes en Bolivia acerca del transporte público. La discusión se encuentra en https://github.com/public-transport/transitous/issues/2318.
2. si existen GTFS de calidad suficiente, proponerlos para inclusión en los catálogos de GTFS ([Transitous](https://transitous.org/doc/#adding-a-region), [Mobility Database](https://mobilitydatabase.org/contribute), [Transitland](https://www.transit.land/documentation/atlas#how-to-add-a-new-feed)),
3. juntar esfuerzos para generar, mantener y publicar nuevos GTFS de manera comunitaria, agencia por agencia (Teleférico, La Paz Bus, Mi Tren, etc.)

## Cómo colaborar?

Puedes unirte al grupo [Datos Bolivia en Telegram](https://t.me/+AWyKECHAM9IyZWZh), comentar en https://github.com/public-transport/transitous/issues/2318, o [abrir una issue aquí](https://github.com/datosbolivia/gtfs/issues) (podemos tener una issue por cada proyecto de nuevo GTFS, es decir, por "agencia").

## Buenas prácticas para la publicación de GTFS

El idioma principal de los archivos es el castellano (es).

Un GTFS corresponde a una sola agencia de transporte (o grupo coherente de agencias). La idea es que se podría delegar o transferir la responsabilidad de la publicación de los datos a una agencia (digamos el Teleférico) si es pertinente. También puede ayudar a repartir los esfuerzos de la comunidad.

El GTFS será generado, validado y publicado automáticamente usando una GitHub Action. El esfuerzo principal está en la generación y actualización de los datos.

Cada modificación de los datos se tiene que hacer mediante una Pull Request, lo que permite validar los cambios con una GitHub Action antes de modificar el GTFS.

Se recomienda empezar con lo mínimo, pero con calidad, y luego ampliar si se puede. Para cada GTFS, trataremos de analizar y publicar las funcionalidades incluidas, y las fechas de actualización.

## Código

El código para generar y validar los GTFS se encuentra en scripts/ y Makefile. Se utiliza el inglés. Para generar los GTFS (se requiere [make](https://www.gnu.org/software/make/)):

```bash
make
```

Eso genera el sitio, con los GTFS y los archivos index.html, se encuentra en dist/. Se puede abrir el archivo dist/index.html en un navegador para explorarlo.

Para validar un GTFS manualmente:

1. generar el GTFS con `make`
2. subir el GTFS en https://gtfs-validator.mobilitydata.org, y verificar que no haya errores (o warnings, si es posible).

Toda actualización de la rama principal (push en la rama main) genera automáticamente los GTFS y el sitio, y los publica en https://datosbolivia.github.io/gtfs/. No validar una PR (pull request) sin haber validado el GTFS manualmente antes, para evitar que se publique un GTFS con errores.
