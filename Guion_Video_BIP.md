# Guion de narración · Desiertos de recarga bip!

El guion sigue los cortes del [video de cinco minutos](Presentacion_Final_BIP.mp4). Las indicaciones en cursiva sirven para sincronizar la grabación. Deje una pausa breve al final de cada bloque.

### 00:00–00:18 · Apertura

*En pantalla, portada y mapa de Santiago.*

¿En qué barrios de Santiago es más difícil encontrar un punto de recarga bip!, pese al volumen de viajes? Cruzamos la demanda de transporte con la ubicación de los puntos de carga para identificar esas zonas y proponer paraderos donde conviene evaluar nuevas ubicaciones.

### 00:18–00:39 · Unidad de análisis

*Muestre el mapa y señale los límites entre zonas.*

Una comuna puede tener muchos puntos de recarga concentrados en su centro, mientras otros barrios quedan lejos. Por eso usamos la zonificación de transporte Zona 777 para el diagnóstico. Después bajamos a la escala de paradero para identificar sitios concretos.

### 00:39–01:01 · Fuentes

*Muestre el período y las tres cifras de la lámina.*

Procesamos más de quince millones de inicios de viaje registrados entre el once y el diecisiete de abril de dos mil veintiséis. Para los paraderos, usamos el promedio de subidas laborales de buses. Para la oferta, consolidamos mil novecientos cinco ubicaciones del catastro de septiembre de dos mil veinticuatro.

### 01:01–01:21 · Cruce de datos

*Señale el contraste entre 58,0 % y 99,94 %.*

El diccionario histórico, cruzado por código interno, ubicaba apenas el cincuenta y ocho por ciento de las subidas. Con el código público y el GTFS del dieciocho de abril recuperamos casi todas. Esa versión del GTFS empieza un día después del período analizado.

### 01:21–01:43 · Accesibilidad

*Muestre los radios de 300 y 500 metros.*

Con un árbol espacial medimos la distancia en línea recta desde cada paradero al bip! más cercano. A trescientos metros queda fuera de cobertura el veintiuno coma cinco por ciento de las subidas de bus analizadas. A quinientos metros, la proporción baja al siete coma siete por ciento.

### 01:43–02:06 · Cuadrantes

*Señale la nube roja del gráfico de zonas.*

La matriz cruza los viajes laborales por zona con la proporción de subidas en paraderos sin recarga a quinientos metros. Usamos el percentil setenta y cinco como corte en ambos ejes. De setecientas noventa y tres zonas comparables, veintisiete tienen simultáneamente alta demanda y alta brecha.

### 02:06–02:27 · PCA y segmentación

*Señale el máximo de silueta en dos grupos y la proyección PCA.*

El PCA resume los atributos en dos componentes que explican casi el setenta y cinco por ciento de la variación. K-Means elige dos grupos por silueta. Las medianas de cada grupo quedan debajo de al menos uno de los cortes críticos. Los cuadrantes permiten señalar las zonas específicas.

### 02:27–02:52 · Regresión

*Muestre el gráfico de error espacial.*

Ridge y Random Forest se usan como regresores. Ambos estiman cuántas subidas laborales registra un paradero, usando atributos como ubicación, oferta de buses y acceso a recarga. Evaluamos en comunas retenidas. Ridge con recarga obtuvo un error absoluto medio cercano a ciento setenta y seis subidas por día. El ranking se construye con subidas observadas.

### 02:52–03:14 · Pronóstico

*Señale las curvas del viernes y destaque el baseline.*

El pronóstico responde otra pregunta. ¿Cuántos viajes empiezan por hora en toda la red? Comparamos ARIMA, SARIMA y la misma hora del día anterior en tres fechas. La referencia del día anterior obtuvo el menor error medio, cinco mil ochocientos cuarenta y siete viajes por hora.

### 03:14–03:35 · Emparejamiento

*Deje visible el indicador de balance.*

También comparamos paraderos con y sin recarga a trescientos metros, emparejándolos según sus características geográficas. La diferencia ajustada fue de unas ciento sesenta y dos subidas laborales al día. Este resultado describe una asociación. El comercio, la conectividad y la frecuencia de buses pueden influir en ella.

### 03:35–03:59 · Sitios priorizados

*Señale el primer candidato en el mapa.*

Para el ranking filtramos paraderos críticos que quedan sin recarga a quinientos metros. Luego ordenamos por subidas multiplicadas por distancia y exigimos doscientos metros entre los sitios elegidos. El primer candidato es el paradero del Intermodal Del Sol, en Maipú, con más de ocho mil subidas laborales diarias.

### 03:59–04:23 · Simulación

*Compare las dos líneas en el punto de 20 sitios.*

Con veinte sitios, el ranking del avance cubre cerca de treinta y seis mil subidas diarias en la simulación. Si elegimos cada punto por la cobertura nueva que aporta, llegamos a unas cincuenta y cuatro mil. Son subidas que ya existen y quedarían dentro de un radio de recarga.

### 04:23–04:41 · Transición al live demo

*Muestre el mapa y el orden de las tres acciones.*

En la demostración vamos a resaltar las zonas críticas, abrir el detalle de un paradero y encender el radio de quinientos metros. Luego cambiaremos la estrategia para comparar cuántas subidas quedarían al alcance de los sitios propuestos.

### 04:41–05:00 · Cierre

*Mantenga la lámina de conclusiones.*

El proyecto entrega un diagnóstico por barrio y una lista de sitios para revisar. Antes de decidir una instalación, queda verificar si los puntos del catastro siguen activos, cómo se llega a pie y qué locales pueden ofrecer el servicio. Gracias.
