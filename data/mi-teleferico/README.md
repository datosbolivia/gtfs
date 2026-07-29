# Mi Teleférico

Para Mi Teleférico, publicamos un GTFS de tipo "Schedule". Ver https://gtfs.org/documentation/schedule/reference/ para los detalles de los archivos y de los campos, así como las buenas prácticas: https://gtfs.org/documentation/schedule/schedule-best-practices/.

Creo que no tiene sentido generar un GTFS de tipo "Realtime", porque no hay información de tiempo real, y además las cabinas de teleférico llegan de manera continua, no son como los buses o trenes.

Para todos los archivos:
- no incluí los campos vacíos para todas las líneas,
- ordene los campos poniendo los campos de identificacióna a la izquierda, y los campos menos importantes a la derecha,
- para los códigos (***_id), establecí un tamaño constante para facilitar el alineamiento vertical. También traté de que el código sea auto-explicativo cuando se pueda.

## feed_info.txt

Puse "Datos Bolivia" como "feed_publisher_name".

## agency.txt

Puse "mi_teleferico" como "agency_id". Tal vez retomar un código existente, si hay (OSM?).

No puse agency_fare_url porque no hay página oficial con los precios, o para comprar boletos en línea.

Para agency_lang, puse "es", pero podría ser "es-BO" para especificar el español de Bolivia.

Para simplificar, no incluí el campo vacío: agency_fare_url.

## stops.txt

Solo puse un stop por estación en la línea Roja, o sea 3 stops, de tipo "stop" (porque solo se permite usar de tipo 'stop' en stop_times.txt). Para las coordenadas, copie desde OSM (por ejemplo, https://www.openstreetmap.org/node/2838067901 para la Estación Central).

Para la estación Libertador, donde llegan la línea Verde y la línea Amarilla, puse un stop por cada línea, porque no están exactamente en el mismo lugar (https://www.openstreetmap.org/node/3088943775 vs https://www.openstreetmap.org/node/6648434407).

Se podría poner más detalles:

- añadir 4 stops por parada (dos direcciones, anden de subida y anden de bajada en cada dirección), de tipo "stop", precisamente ubicados con algunos metros de precisión
- añadir un stop para la estación como tal (tipo "station"), y colocar este valor en parent_station de los stops de cada anden
- agregar stops para las entradas del edificio de la estación (ver "platforms.txt")

Para el código (stop_id), el formato es `estacion_c/stop/001` para el primer punto de tipo "stop" en la Estación Central: primero el nombre de la estación en minusculas, con espacios remplazados por guiones bajos, y truncando a 10 caracteres. Luego, el tipo de "stop" (ver location_type, codificada con 4 caracteres: "stop", "stat", "entr", "gene", "boar"), y luego el número de punto (001, 002, 003, ...) de forma iterativa. Los tres subcampos están separados por "/".

Para los nombres, evité poner "Estación" al inicio, como recomendado en https://gtfs.org/documentation/schedule/best-practices/#stopstxt. Excepción: "Estación Central", porque se refiere a la estación central de trenes.

No puse stop_url porque hay una página oficial para la línea Roja: https://www.miteleferico.bo/lineas/linea-roja, y haciendo clic en una estación, se actualiza el estado interno de la página para mostrar los detalles de esa estación, pero no hay una URL directa hacia esta página.

En stop_desc, copie la información en https://www.miteleferico.bo/lineas/linea-roja.

No puse parent_station, pero si creamos un stop por anden, entonces sí habrá que ponerlo.

No puse stop_timezone, se utiliza la zona horaria de la agencia (America/La_Paz) por defecto.

No puse los campos de ubicación de los stops como "level_id" o "stop_access". Se podrá hacer luego.

Para simplificar, no incluí los campos vacíos: stop_code, tts_stop_name, zone_id, stop_url, parent_station, stop_timezone, level_id, platform_code y stop_access.

## routes.txt

Solo la línea Roja por el momento.

Puse "roja" como "route_id". Usar las cuatro primeras letras del color, en minúsculas (amarilla -> amar). Tal vez retomar un código existente, si hay (OSM?). Para la línea Morada, como está discontinuida en la estación Faro Murillo, puse dos route_id: mor1 y mor2.

No puse route_desc. Se podría añadir si hay una descripción larga y con información adicional en comparación con route_long_name.

No puse network_id todavía, no sé si es necesario.

Para los colores, busqué un plano del teleférico. Ver https://github.com/datosbolivia/gtfs/issues/2#issuecomment-5096536344.

Para simplificar, no incluí los campos vacíos: route_desc, continuous_pickup, continuous_drop_off, network_id y cemv_support.

## trips.txt

Solo pusé para la línea Roja. Son 4 trayectos (trips): dos direcciones, y uno para la semana y otro para fin de semana.

Para el código (trip_id), el formato es `roja/16_de_julio/semana` para el trayecto de la línea roja hacia la estación 16 de Julio en días de la semana: primero el código de la línea, luego el nombre de la estación destino, y luego el código del servicio (semana o fin_de). Los tres subcampos están separados por "/".

Hay que verificar "trip_headsign" en los paneles en las estaciones.

Creo que block_id no es necesario, a verificar.

Habrá que agregar shape_id una vez se tenga el archivo de shapes.txt.

Para simplificar, no incluí los campos vacíos: trip_short_name, block_id, shape_id, safe_duration_factor y safe_duration_offset.

## stop_times.txt

Como incluímos el archivo frequencies.txt, no es necesario poner los horarios de llegada y salida de cada cabina en cada estación en cada momento del día. Como recomendado en https://gtfs.org/documentation/schedule/schedule-best-practices/#frequenciestxt, puse unicamente una entrada para el horario ficticio 00:00:00 en la primera estación, y en las siguientes estaciones, para definir el tiempo de recorrido.

Para los tiempos de recorrida entre estaciones, use los valores en https://www.miteleferico.bo/lineas/linea-roja: estación central -> cementerio: 5 min 09 s, cementerio -> 16 de julio: 5 min 38 s.

No puse stop_headsign, lo que implica que se usa el valor de stop_headsign del "trip". Hay que verificar si el panel de destino cambia según la parada, en tal caso, habría que poner el valor de stop_headsign en cada parada.

Puse pickup_type y drop_off_type como 1 (no permitido), porque no se puede subir ni bajar en el medio del trayecto, solo en las estaciones.

No puse shape_dist_traveled, porque no tenemos shapes.txt todavía. Se podría poner un valor una vez se tenga shapes.txt, para indicar la distancia recorrida desde el inicio del trayecto. No estoy seguro si es necesario, sin embargo.

Puse timepoint como 0, porque el tiempo de recorrida entre estaciones solo es aproximado. Depende de la velocidad del cable, que puede variar según la fecha, la hora, el flujo de pasajeros.

Para simplificar, no incluí los campos vacíos: location_group_id, location_id, stop_headsign,start_pickup_drop_off_window, end_pickup_drop_off_window, pickup_type, drop_off_type, continuous_pickup, continuous_drop_off, shape_dist_traveled, pickup_booking_rule_id and drop_off_booking_rule_id.

## calendar.txt

Cree dos service_id: semana y fin_de (mismo tamaño), porque los horarios son diferentes en días de la semana y en la semana. Tal vez retomar un código existente, si hay (OSM?). O usar otro código (1, 2, 3, 4, ...).

Puse "20260801" como start_date y "20261231" como end_date. Significa que habrá que ampliar end_date antes del fin del año, y regularmente. Otra opción es poner un rango más amplio, por ejemplo 20260801-20301231.

Añadí service_name, aunque no esta en estandar, pero es recomendado en https://gtfs.org/documentation/schedule/schedule-best-practices/. Se muestra como info en el validador de GTFS https://gtfs-validator-results.mobilitydata.org/, pero está bien.

## calendar_dates.txt

Aquí puse los próximos feriados en 2026 en La Paz, según https://www.feriados.com.bo/: 6 de agosto, 7 de agosto, 2 de noviembre y 25 de diciembre. Para estos cuatro días, di de baja el servicio "semana" y di de alta el servicio "fin_de".

Abrá que actualizar este archivo, porque el estandar recomiendo no incluir datos del pasado (https://gtfs.org/documentation/schedule/schedule-best-practices/).

Añadí service_name, aunque no esta en estandar, pero es recomendado en https://gtfs.org/documentation/schedule/schedule-best-practices/. Se muestra como info en el validador de GTFS https://gtfs-validator-results.mobilitydata.org/, pero está bien.

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

Utilicé este archivo para indicar el tiempo entre las cabinas, y el tiempo de apertura de la línea Roja. De esta forma, el archivo stop_times.txt es más simple, y solo sirve para indicar la duración de viaje entre estaciones.

Medí headway_secs a 20s entre dos cabinas. Escuché que el tiempo entre cabinas cambia según la hora del día o el día de la semana (al igual que el tiempo de recorrida entre estaciones, obviamente), porque adaptan la velocidad al flujo de pasajeros. Podremos adecuar eso más adelante si el cambio es significativo.

## transfers.txt

## pathways.txt

## levels.txt

## location_groups.txt

## location_group_stops.txt

## locations.geojson

## booking_rules.txt

## translations.txt

## feed_info.txt

Puse default_lang a es, porque solo tenemos el español. Si traducimos, se puede poner otro idioma (en?).

Para feed_lang y default_lang, puse "es", pero podría ser "es-BO" para especificar el español de Bolivia.

Puse feed_start_date y feed_end_date a las mismas fechas que en calendar.txt, es importante que sea el mismo porque sino implica que no hay servicio en las fechas que faltan.

Para feed_version, inicie con 1. Sería bueno incrementarlo para cada cambio, o por lo menos para cada cambio importante. Nota: solo es para información de los desarrolladores.

Para simplificar, no incluí el campo vacío: feed_contact_email.

## attributions.txt

Di la atribución a Datos Bolivia, porque entiendo que es una referencia hacia la organización que genera los datos (data producer), segun https://gtfs.org/documentation/schedule/examples/attributions/. Hay algo de redundancia con feed_info.txt.

Puse "datos_bolivia" como "attribution_id". Está bien?

Para simplificar, no incluí los campos vacíos: agency_id, route_id, trip_id, attribution_email y attribution_phone.
