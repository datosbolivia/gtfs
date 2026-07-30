# Mi Teleférico

Para Mi Teleférico, publicamos un GTFS de tipo "Schedule". Ver https://gtfs.org/documentation/schedule/reference/ para los detalles de los archivos y de los campos, así como las buenas prácticas: https://gtfs.org/documentation/schedule/schedule-best-practices/.

Creo que no tiene sentido generar un GTFS de tipo "Realtime", porque no hay información de tiempo real, y además las cabinas de teleférico llegan de manera continua, no son como los buses o trenes.

Para todos los archivos:
- no incluí los campos vacíos para todas las líneas,
- ordene los campos poniendo los campos de identificacióna a la izquierda, y los campos menos importantes a la derecha,
- para los códigos (***_id), establecí un tamaño constante para facilitar el alineamiento vertical. También traté de que el código sea auto-explicativo cuando se pueda.

## agency.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#agencytxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#agencytxt).

### código

`agency_id`: solo hay un registro, y puse "mi_teleferico".

### justificaciones

Nada especial.

### campos no incluidos

- `agency_fare_url`. Ver https://github.com/datosbolivia/gtfs/issues/14.

## stops.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#stopstxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#stopstxt).

### código

`stop_id`: el formato es `estacion_c/stat/001` para el stop de tipo `station` de la Estación Central, y `estacion_c/stop/001` para el primer punto de tipo `stop` (andenes de la línea roja) en la Estación Central. Primero el nombre de la estación en minusculas, con espacios remplazados por guiones bajos, y truncando a 10 caracteres. Luego, el tipo de "stop" (ver `location_type`, codificada con 4 caracteres: `stop`, `stat`, `entr`, `gene`, `boar`), y luego el número de punto (`001`, `002`, `003`, ...) de forma iterativa. Los tres subcampos están separados por `/`.

### justificaciones

Para la ubicación de los stops de tipo `stop`, usé las coordenadas de OSM (por ejemplo, https://www.openstreetmap.org/node/2838067901 para los andenes de la línea Roja en la Estación Central).

Para la ubicación de los stops de tipo `stat`, usé las coordenadas del punto de la etiqueta del polígono de la estación en OSM (por ejemplo, https://www.openstreetmap.org/way/549632678#map=19/-16.491656/-68.144576, mientras la estación es https://www.openstreetmap.org/relation/8703332).

Para los nombres, evité poner `Estación` al inicio, como recomendado en https://gtfs.org/documentation/schedule/best-practices/#stopstxt. Excepción: `Estación Central`, porque se refiere a la estación central de trenes.

En `stop_desc`, copié la información en https://www.miteleferico.bo/lineas/linea-roja, y mencioné que son andenes, con el nombre de la línea cuando corresponda.

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

`route_id`: usar las cuatro primeras letras del color, en minúsculas (`Línea Amarilla` -> `amar`). Para la línea Morada, como está discontinuida en la estación Faro Murillo, puse dos rutas con los códigos `mor1` y `mor2`.

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

`trip_id`: el formato es `roja/16_de_julio/semana` para el trayecto de la línea Roja hacia la estación 16 de Julio en días de la semana: primero el código de la línea, luego el nombre de la estación de destino (11 carácteres, minusculas, y guiones bajos en vez de espacios), y luego el código del servicio (`semana` o `fin_de`). Los tres subcampos están separados por `/`.

### justificaciones

Para cada ruta, hay cuatro trips: dos direcciones, y uno para la semana y otro para fin de semana. Por ejemplo, para la línea Roja, hay cuatro trips: `roja/16_de_julio/semana`, `roja/16_de_julio/fin_de`, `roja/estacion_c/semana` y `roja/estacion_c/fin_de`.

Para la dirección, hay que ser coherente entre las líneas, para que la dirección `0` sea la misma para dos líneas sucesivas.

Para `trip_headsign`, utilicé los datos de OSM (por ejemplo: https://www.openstreetmap.org/relation/9845910), que son más precisos que el sitio del teleférico (lo que importa es lo que los usuarios del teleférico ven cuando buscan su camino en la estación). Pero en algunos casos, tuve que corregir porque el nombre mostrado en la estación no era el mismo, por ejemplo: `INALMAMA - Héroes de la Revolución` en la estación del monumento Busch. Usé el nombre completo `INALMAMA - Héroes de la Revolución` aunque son dos idiomas (aymara y castellano), porque es lo que se ve en la estación. Hay que verificar `trip_headsign` en los paneles en las estaciones: ver https://github.com/datosbolivia/gtfs/issues/22.

### campos no incluidos

- `trip_short_name`: no aplica, es más para trenes
- `block_id`: podría ser necesario para la línea Morada, porque tuve que cortarla en dos rutas distinctas, pero no se cobra trasbordo cuando uno pasa de `mor1` a `mor2` (por lo menos, eso supongo). Ver https://github.com/datosbolivia/gtfs/issues/14.
- `shape_id`: llenar cuando se tenga el archivo de `shapes.txt`. Ver https://github.com/datosbolivia/gtfs/issues/23.
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
- `shape_dist_traveled`: no tenemos `shapes.txt` todavía. Se podría poner un valor una vez se tenga `shapes.txt`, para indicar la distancia recorrida desde el inicio del trayecto (ver https://github.com/datosbolivia/gtfs/issues/23).
- `pickup_booking_rule_id`: no aplica
- `drop_off_booking_rule_id`: no aplica

## calendar.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#calendartxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#calendartxt).

### código

`service_id`: puse `semana` para los días de la semana, y `fin_de` para los fines de semana y feriados.

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

Puse los próximos feriados en 2026 en La Paz, según https://www.feriados.com.bo/: 6 de agosto, 7 de agosto, 2 de noviembre y 25 de diciembre. Para estos cuatro días, di de baja el servicio `semana` y di de alta el servicio `fin_de`, porque se aplica el horario de fin de semana en feriados.

Abrá que actualizar este archivo, porque el estándar recomienda no incluir datos del pasado (https://gtfs.org/documentation/schedule/schedule-best-practices/). Ver https://github.com/datosbolivia/gtfs/issues/25.

Añadí `service_name`, aunque no está en el estándar, pero es recomendado en https://gtfs.org/documentation/schedule/schedule-best-practices/. Se muestra como info en el validador de GTFS https://gtfs-validator-results.mobilitydata.org/, pero está bien. Es útil para que los desarrolladores puedan entender mejor a qué se refiere la excepción de servicio, por ejemplo: `Día de la Patría (feriado nacional)`.

### campos no incluidos

Todos los campos están incluidos, no hay campos vacíos.

## fare_attributes.txt

## fare_rules.txt

## timeframes.txt

## rider_categories.txt

## fare_media.txt

## fare_products.txt

## fare_leg_rules.txt

## fare_leg_join_rules.txt

## fare_transfer_rules.txt

## areas.txt

## stop_areas.txt

## networks.txt

## route_networks.txt

## shapes.txt

## frequencies.txt

[Referencia](https://gtfs.org/documentation/schedule/reference/#frequenciestxt), [Buenas prácticas](https://gtfs.org/documentation/schedule/schedule-best-practices/#frequenciestxt).

### código

No se definen códigos en este archivo.

### justificaciones

Utilicé este archivo para indicar el tiempo de espera entre dos cabinas sucesivas, y los horarios de servicio de cada línea. De esta forma, el archivo `stop_times.txt` es más simple, y solo sirve para indicar la duración de viaje entre estaciones.

Medí `headway_secs` a 20 segundos entre dos cabinas. Escuché que el tiempo entre cabinas cambia según la hora del día o el día de la semana (al igual que el tiempo de recorrida entre estaciones, obviamente), porque adaptan la velocidad al flujo de pasajeros. Podremos adecuar eso más adelante si el cambio es significativo. Ver https://github.com/datosbolivia/gtfs/issues/24.

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

## feed_info.txt

Puse "Datos Bolivia" como "feed_publisher_name".

Puse default_lang a es, porque solo tenemos el español. Si traducimos, se puede poner otro idioma (en?).

Para feed_lang y default_lang, puse "es", pero podría ser "es-BO" para especificar el español de Bolivia.

Puse feed_start_date y feed_end_date a las mismas fechas que en calendar.txt, es importante que sea el mismo porque sino implica que no hay servicio en las fechas que faltan.

Para feed_version, inicie con 1. Sería bueno incrementarlo para cada cambio, o por lo menos para cada cambio importante. Nota: solo es para información de los desarrolladores.

Para simplificar, no incluí el campo vacío: feed_contact_email.

## attributions.txt

Di la atribución a Datos Bolivia, porque entiendo que es una referencia hacia la organización que genera los datos (data producer), segun https://gtfs.org/documentation/schedule/examples/attributions/. Hay algo de redundancia con feed_info.txt.

Puse "datos_bolivia" como "attribution_id". Está bien?

Para simplificar, no incluí los campos vacíos: agency_id, route_id, trip_id, attribution_email y attribution_phone.
