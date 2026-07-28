# Mi Teleférico

Ver https://gtfs.org/documentation/schedule/reference/ para los detalles de los archivos y de los campos.

## agency.txt

Puse "mi_teleferico" como "agency_id". Tal vez retomar un código existente, si hay (OSM?).

No puse agency_fare_url porque no hay página oficial con los precios, o para comprar boletos en línea.

Para agency_lang, puse "es", pero podría ser "es-BO" para especificar el español de Bolivia.

## stops.txt

Solo puse un stop por estación en la línea Roja, o sea 3 stops, de tipo "stop". Para las coordenadas, copie desde OSM: https://www.openstreetmap.org/node/2838067901 para la Estación Central.

Se podría poner más detalles:

- pasar a 4 stops por estación (dos direcciones, anden de subida y anden de bajada en cada dirección), de tipo "stop", precisamente ubicados con algunos metros de precisión, más un stop para la estación como tal (tipo "station").
- agregar stops para las entradas del edificio de la estación (ver "platforms.txt")

Puse números enteros (1, 2, 3) como "stop_id". Está bien? Tal vez retomar un código existente, si hay (OSM?).

No puse stop_url porque hay una página oficial para la línea Roja: https://www.miteleferico.bo/lineas/linea-roja, y haciendo clic en una estación, se actualiza el estado interno de la página para mostrar los detalles de esa estación, pero no hay una URL directa hacia esta página.

No puse parent_station, pero si creamos un stop por anden, entonces sí habrá que ponerlo.

No puse stop_timezone, se utiliza la zona horaria de la agencia (America/La_Paz) por defecto.

No puse los campos de ubicación de los stops como "level_id" o "stop_access". Se podrá hacer luego.

## routes.txt

Solo la línea Roja por el momento.

Puse "roja" como "route_id". Tal vez retomar un código existente, si hay (OSM?).

No puse network_id todavía, no sé si es necesario.

## trips.txt

Solo pusé para la línea Roja. Son 4 trayectos (trips): dos direcciones, y uno para la semana y otro para fin de semana.

Puse números enteros (1, 2, 3, 4) como "trip_id". Está bien?

Hay que verificar "trip_headsign" en los paneles en las estaciones.

Creo que block_id no es necesario, a verificar.

Habrá que agregar shape_id una vez se tenga el archivo de shapes.txt.

## stop_times.txt

## calendar.txt

## calendar_dates.txt

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

No puse feed_start_date y feed_end_date, creo que no es necesario en nuestro caso, ya que no tenemos autoridad ni conocimiento sobre los horarios previstos.

Para feed_version, inicie con 1. Sería bueno incrementarlo para cada cambio, o por lo menos para cada cambio importante. Nota: solo es para información de los desarrolladores.

## attributions.txt

Di la atribución a Datos Bolivia, porque entiendo que es una referencia hacia la organización que genera los datos (data producer), segun https://gtfs.org/documentation/schedule/examples/attributions/. Hay algo de redundancia con feed_info.txt.

Puse "datos_bolivia" como "attribution_id". Está bien?
