# Mi Teleférico

Para Mi Teleférico, publicamos un GTFS de tipo "Schedule". Ver https://gtfs.org/documentation/schedule/reference/ para los detalles de los archivos y de los campos, así como las buenas prácticas: https://gtfs.org/documentation/schedule/schedule-best-practices/.

Creo que no tiene sentido generar un GTFS de tipo "Realtime", porque no hay información de tiempo real, y además las cabinas de teleférico llegan de manera continua, no son como los buses o trenes.

Para todos los archivos:
- no incluí los campos vacíos para todas las líneas,
- los campos se ordenan automáticamente según el [GTFS Schedule Reference](https://gtfs.org/documentation/schedule/reference/) mediante el linter (`make lint`). Los campos de identificación van a la izquierda, y los campos menos importantes a la derecha,
- para los códigos (***_id), tratamos de que el código sea auto-explicativo cuando se pueda, y que empiece por un prefijo que indica la tabla (por ejemplo: `rc_` para `rider_category`).

## agency.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#agencytxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#agencytxt).

### código

`agency_id`: solo hay un registro, y puse "ag/mi_teleferico".

### justificaciones

Nada especial.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## stops.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#stopstxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#stopstxt).

### código

`stop_id`: el formato es `st/estacion_central/station/001` para el stop de tipo `station` de la Estación Central, y `st/estacion_central/stop/001` para el primer punto de tipo `stop` (andenes de la línea roja) en la Estación Central. Primero el prefijo `st`. Luego el nombre de la estación en minusculas, con espacios remplazados por guiones bajos. Luego, el tipo de "stop" (ver `location_type`), y luego el número de punto (`001`, `002`, `003`, ...) de forma iterativa. Los subcampos están separados por `/`.

### justificaciones

Para la ubicación de los stops de tipo `stop`, usé las coordenadas de OSM (por ejemplo, https://www.openstreetmap.org/node/2838067901 para los andenes de la línea Roja en la Estación Central).

Para la ubicación de los stops de tipo `station`, usé las coordenadas del punto de la etiqueta del polígono de la estación en OSM (por ejemplo, https://www.openstreetmap.org/way/549632678#map=19/-16.491656/-68.144576, mientras la estación es https://www.openstreetmap.org/relation/8703332).

Para los nombres, evité poner `Estación` al inicio, como recomendado en https://gtfs.org/documentation/schedule/best-practices/#stopstxt. Excepción: `Estación Central`, porque se refiere a la estación central de trenes.

En `stop_desc`, copié la información en https://www.miteleferico.bo/lineas/linea-roja, y mencioné que son andenes, con el nombre de la línea cuando corresponda.

En #29, en varias estaciones, se creó dos stops: uno para ida, y uno para vuelta, separados de algunos metros. Ver #16.

Puse `stop_access` a `0` en todos los stops, porque no se puede acceder a los andenes directamente desde la calle, hay que ingresar a la estación primero.

### campos no incluidos

- `stop_code`: no existe tal código de estación, se usa el nombre completo en los carteles.
- `tts_stop_name`: no creo que sea necesario, todos los nombres de estaciones deberían ser pronunciables.
- `zone_id`: ver https://github.com/datosbolivia/gtfs/issues/14.
- `stop_url`: hay una página oficial para la línea Roja: https://www.miteleferico.bo/lineas/linea-roja, y haciendo clic en una estación, se actualiza el estado interno de la página para mostrar los detalles de esa estación, pero no hay una URL directa hacia esta página.
- `stop_timezone`: se utiliza la zona horaria de la agencia (`America/La_Paz`) por defecto.
- `level_id`: ver https://github.com/datosbolivia/gtfs/issues/17.
- `platform_code`: no existe tal código de plataforma (es más para estaciones de trenes, con múltiples plataformas paralelas).

## routes.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#routestxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#routestxt).

### código

`route_id`: prefijo `ro/` y el color de la línea en minúsculas (`Línea Amarilla` -> `ro/amarilla`). Para la línea Morada, como está discontinuida en la estación Faro Murillo, puse dos rutas con los códigos `ro/morada_1` y `ro/morada_2`.

### justificaciones

Para los colores, busqué un plano del teleférico y usé la pipeta para copiar los colores. Ver https://github.com/datosbolivia/gtfs/issues/2#issuecomment-5096536344.

Para `route_sort_order`, seguí el orden en https://www.miteleferico.bo/nuestras-lineas.

Para `route_desc`, describí las dos zonas que conecta cada línea para dar más contexto.

### campos no incluidos

- `continuous_pickup`: no aplica
- `continuous_drop_off`: no aplica (no trates de saltar de una cabina de teleférico, por favor)
- `network_id`: creo que no aplica, pero revisar en https://github.com/datosbolivia/gtfs/issues/14.
- `cemv_support`: ya está definido en `agency.txt`, no es necesario repetirlo en `routes.txt` ya que es el mismo valor para todas las líneas.

## trips.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#tripstxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#tripstxt).

### código

`trip_id`: el formato es `roja/16_de_julio/semana` para el trayecto de la línea Roja hacia la estación 16 de Julio en días de la semana: primero el código de la línea, luego el nombre de la estación de destino (minusculas y guiones bajos en vez de espacios), y luego el código del servicio (`semana` o `fin_de_semana`). Los tres subcampos están separados por `/`.

### justificaciones

Para cada ruta, hay cuatro trips: dos direcciones, y uno para la semana y otro para fin de semana. Por ejemplo, para la línea Roja, hay cuatro trips: `roja/16_de_julio/semana`, `roja/16_de_julio/fin_de_semana`, `roja/estacion_c/semana` y `roja/estacion_c/fin_de_semana`.

Para la dirección, hay que ser coherente entre las líneas, para que la dirección `0` sea la misma para dos líneas sucesivas.

Para `trip_headsign`, utilicé los datos de OSM (por ejemplo: https://www.openstreetmap.org/relation/9845910), que son más precisos que el sitio del teleférico (lo que importa es lo que los usuarios del teleférico ven cuando buscan su camino en la estación). Pero en algunos casos, tuve que corregir porque el nombre mostrado en la estación no era el mismo, por ejemplo: `INALMAMA - Héroes de la Revolución` en la estación del monumento Busch. Usé el nombre completo `INALMAMA - Héroes de la Revolución` aunque son dos idiomas (aymara y castellano), porque es lo que se ve en la estación. Hay que verificar `trip_headsign` en los paneles en las estaciones: ver https://github.com/datosbolivia/gtfs/issues/22.

### campos no incluidos

- `trip_short_name`: no aplica, es más para trenes
- `block_id`: podría ser necesario para la línea Morada, porque tuve que cortarla en dos rutas distintas, pero no se cobra trasbordo cuando uno pasa de `morada_1` a `morada_2` (por lo menos, eso supongo). Ver https://github.com/datosbolivia/gtfs/issues/14.
- `safe_duration_factor`: no aplica
- `safe_duration_offset`: no aplica

## stop_times.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#stop_timestxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#stop_timestxt).

### código

`stop_sequence`: el número de la parada en la línea, empezando por `1` en la primera estación de la línea, y incrementando por 1 para cada parada sucesiva.

### justificaciones

Como incluímos el archivo `frequencies.txt`, no es necesario poner los horarios de llegada y salida de cada cabina en cada estación en cada momento del día. Como recomendado en [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#frequenciestxt), puse unicamente una entrada para el horario ficticio `00:00:00` en la primera estación, y en las siguientes estaciones, para definir el tiempo de recorrido.

Para los tiempos de recorrida entre estaciones, use los valores en el sitio del teleférico. Por ejemplo, en [Línea Roja](https://www.miteleferico.bo/lineas/linea-roja): estación central -> cementerio: 5 min 09 s, cementerio -> 16 de julio: 5 min 38 s. Si más adelante logramos tener más informacón sobre los cambios de velocidad, podremos ajustar, y eventualemente crear más "trips" según la velocidad (ver https://github.com/datosbolivia/gtfs/issues/24).

Puse `timepoint` como `0`, porque el tiempo de recorrida entre estaciones solo es aproximado. Depende de la velocidad del cable, que puede variar según la fecha, la hora, el flujo de pasajeros.

### campos no incluidos

- `location_group_id`: no aplica
- `location_id`: no aplica
- `stop_headsign`: se usa el valor de `stop_headsign` del "trip". Hay que verificar si el panel de destino cambia según la parada, en tal caso, habría que poner el valor de `stop_headsign` en cada parada. Ver https://github.com/datosbolivia/gtfs/issues/22.
- `start_pickup_drop_off_window`: no aplica
- `end_pickup_drop_off_window`: no aplica
- `pickup_type`: no aplica
- `drop_off_type`: no aplica
- `continuous_pickup`: no aplica
- `continuous_drop_off`: no aplica
- `shape_dist_traveled`: Se podría poner un valor, basado en los valores de `shapes.txt`, para indicar la distancia recorrida desde el inicio del trayecto (ver https://github.com/datosbolivia/gtfs/issues/23).
- `pickup_booking_rule_id`: no aplica
- `drop_off_booking_rule_id`: no aplica

## calendar.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#calendartxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#calendartxt).

### código

`service_id`: puse `se/semana` para los días de la semana, y `se/fin_de_semana` para los fines de semana y feriados.

### justificaciones

Puse `20260701` como `start_date` y `20261231` como `end_date`. Significa que habrá que ampliar `end_date` antes del fin del año, y regularmente. Otra opción es poner un rango más amplio, por ejemplo `2026001` -> `20301231`. Ver https://github.com/datosbolivia/gtfs/issues/25.

Añadí `service_name`, aunque no está en el estándar, porque es recomendado en https://gtfs.org/documentation/schedule/schedule-best-practices/. Se muestra como info en el validador de GTFS https://gtfs-validator-results.mobilitydata.org/, pero está bien. Es útil para que los desarrolladores puedan entender mejor el significado de `service_id`.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## calendar_dates.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#calendar_datestxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#calendar_datestxt).

### código

No se definen códigos en este archivo.

### justificaciones

Puse los próximos feriados en 2026 en La Paz, según https://www.feriados.com.bo/: 6 de agosto, 7 de agosto, 2 de noviembre y 25 de diciembre. Para estos cuatro días, di de baja el servicio `se/semana` y di de alta el servicio `se/fin_de_semana`, porque se aplica el horario de fin de semana en feriados.

Abrá que actualizar este archivo, porque el estándar recomienda no incluir datos del pasado (https://gtfs.org/documentation/schedule/schedule-best-practices/). Ver https://github.com/datosbolivia/gtfs/issues/25.

Añadí `service_name`, aunque no está en el estándar, pero es recomendado en https://gtfs.org/documentation/schedule/schedule-best-practices/. Se muestra como info en el validador de GTFS https://gtfs-validator-results.mobilitydata.org/, pero está bien. Es útil para que los desarrolladores puedan entender mejor a qué se refiere la excepción de servicio, por ejemplo: `Día de la Patría (feriado nacional)`.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## fare_attributes.txt

## fare_rules.txt

## timeframes.txt

No incluido, porque las tarifas son fijas, sin importar el momento del día o de la semana.

## rider_categories.txt

### código

- `rider_category_id`: solo hay dos tipos de pasajeros: General y Preferencial o Estudiantil. Los códigos son: `rc/general` y `rc/preferencial`.

### justificaciones

En realidad, hay tres tipos de pasajeros: General, Preferencial y Estudiantil. Pero como la tarifa preferencial y la tarifa estudiantil son las mismas, no vale la pena distinguirlos aquí.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## fare_media.txt

## fare_products.txt

## fare_leg_rules.txt

## fare_leg_join_rules.txt

## fare_transfer_rules.txt

## areas.txt

## stop_areas.txt

## networks.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#networkstxt).

### código

- `network_id`: solo hay una red, se puso `ne/rim`.

### justificaciones

El nombre de la red es Red de Integración Metropolitana.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## route_networks.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#route_networkstxt]

### código

No se definen códigos en este archivo.

### justificaciones

Se crea una entrada por cada ruta del teleférico, todas para la red `ne/rim`.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## shapes.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#shapestxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#shapestxt).

### código

- `shape_id`: el formato es `sh/roja/16_de_julio` para el trayecto de la línea Roja hacia la estación 16 de Julio: primero el prefijo `sh`, luego el código de la línea, y luego el nombre de la estación de destino (minusculas y guiones bajos en vez de espacios). Los subcampos están separados por `/`.

### justificaciones

Por el momento, solo incluye un punto por estación. Idealmente, tendríamos la ubicación de cada poste de la línea, entre las estaciones. La información está en OpenStreetMap. Ver https://github.com/datosbolivia/gtfs/issues/23.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## frequencies.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#frequenciestxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#frequenciestxt).

### código

No se definen códigos en este archivo.

### justificaciones

Utilicé este archivo para indicar el tiempo de espera entre dos cabinas sucesivas, y los horarios de servicio de cada línea. De esta forma, el archivo `stop_times.txt` es más simple, y solo sirve para indicar la duración de viaje entre estaciones.

Medí `headway_secs` a 20 segundos entre dos cabinas. Escuché que el tiempo entre cabinas cambia según la hora del día o el día de la semana (al igual que el tiempo de recorrida entre estaciones, obviamente), porque adaptan la velocidad al flujo de pasajeros. Podremos adecuar eso más adelante si el cambio es significativo. A notar que se cambió de 20s a 12s (o 9s) según la línea, en #29. La discusión se encuentra en https://github.com/datosbolivia/gtfs/issues/24.

### campos no incluidos

- `block_id`: no está en el estándar, pero las [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#frequenciestxt) mencionan que se puede incluir. Tal vez sea necesario para la línea Morada (ver https://github.com/datosbolivia/gtfs/issues/14).

## transfers.txt

## pathways.txt

## levels.txt

## location_groups.txt

## location_group_stops.txt

## locations.geojson

## booking_rules.txt

## translations.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#translations.txt), [Ejemplo](https://gtfs.org/documentation/schedule/examples/translations/).

### código

No se definen códigos en este archivo.

### justificaciones

La idea es traducir en inglés lo que vale la pena. Solo pueden traducirse los campos de tipo Text, en algunos archivos.

- `agencia.txt`: no se traduce nada. Solo se puede traducir el nombre de la agencia (Mi Teleférico) - no hay razón para traducirlo, porque es un nombre propio.
- `stops.txt`: se traduce `stop_desc`. Dentro de los campos que llenamos, solo se pueden traducir el nombre y la descripción de la estación. El nombre es lo que se ve en los carteles, no se traduce. Al contrario, es útil traducir la descripción.
- `routes.txt`: se traduce `route_desc`. Dentro de los campos que llenamos, solo se pueden traducir el nombre corto, el nombre largo y la descripción de la línea. Los dos nombres son lo que se ve en los carteles, no se traducen. Al contrario, es útil traducir la descripción.
- `trips.txt`: no se traduce nada. Dentro de los campos que llenamos, solo se puede traducir el texto del cartel `trip_headsign`. Pero no se traduce, es lo que el usuario ve.
- `stop_times.txt`: no se traduce nada. Ninguno de los campos que llenamos es de tipo Text.
- `pathways.txt`: no se traduce nada. No hemos creado `pathways.txt` todavía. Volver a analizar si lo creamos.
- `levels.txt`: no se traduce nada. No hemos creado `levels.txt` todavía. Volver a analizar si lo creamos.
- `feed_info.txt`: no se traduce nada. Solo se puede traducir nuestro nombre (Datos Bolivia) y la versión del feed: no tiene sentido traducirlos.
- `attributions.txt`: no se traduce nada. Solo se puede traducir nuestro nombre (Datos Bolivia): no tiene sentido traducirlo.

### campos no incluidos

- `record_sub_id`: no se requiere para `stops` y `routes`.
- `field_value`: es una forma alternativa a `record_id` para identificar el texto traducido. Usamos `record_id` porque es más robusto a cambios en los valores de los textos, así que no usamos `field_value`.

## feed_info.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#feed_infotxt).

### código

No se definen códigos en este archivo.

### justificaciones

Puse `Datos Bolivia` como `feed_publisher_name`.

Puse `default_lang` a `en`, para que los usuarios de GTFS con otro idioma que el español vean las traducciones al inglés.

Puse `feed_start_date` y `feed_end_date` a las mismas fechas que en `calendar.txt`, es importante que sea el mismo porque sino implica que no hay servicio en las fechas que faltan. Ver https://github.com/datosbolivia/gtfs/issues/25.

Para `feed_version`, inicie con `1`. Sería bueno incrementarlo para cada cambio, o por lo menos para cada cambio importante. Nota: solo es para información de los desarrolladores.

### campos no incluidos

- `feed_contact_email`: como comunidad, no tenemos un email de contacto. Con la URL de las issues de GitHub, es suficiente.

## attributions.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#attributionstxt).

### código

- `attribution_id`: puse `at/datos_bolivia`, porque es la organización que genera los datos (data producer). Ver https://gtfs.org/documentation/schedule/examples/attributions/.

### justificaciones

Di la atribución a Datos Bolivia, porque entiendo que es una referencia hacia la organización que genera los datos (data producer), segun https://gtfs.org/documentation/schedule/examples/attributions/. Hay algo de redundancia con `feed_info.txt`.

### campos no incluidos

- `agency_id`: vacío para indicar que se aplica a todo el juego de datos.
- `route_id`: vacío para indicar que se aplica a todo el juego de datos.
- `trip_id`: vacío para indicar que se aplica a todo el juego de datos.
- `attribution_email`: no tenemos un email de contacto como comunidad.
- `attribution_phone`: no tenemos un teléfono de contacto como comunidad.
