# Guion de narración · Desiertos de recarga bip!

El guion sigue los cortes del [video de cinco minutos](Presentacion_Final_BIP.mp4). Las indicaciones en cursiva sirven para sincronizar la grabación. Lea en voz alta el párrafo bajo cada indicación. Las notas en bloques de cita son para preparar la exposición o responder preguntas del curso y quedan fuera de los cinco minutos.

### 00:00–00:18 · Apertura

*En pantalla, portada y mapa de Santiago.*

Imaginen que llegan al paradero con poco saldo en la bip!, la tarjeta que se usa para pagar el transporte público de Santiago. ¿Dónde se juntan muchos viajes y pocas oportunidades de cargarla cerca? Buscamos paraderos donde valdría la pena evaluar una instalación.

> **Para quien presenta.** «Desierto de recarga» describe un sector donde llegar a una recarga física puede ser difícil. Los datos registran viajes, subidas y ubicaciones. Saber cuántas personas se quedaron sin saldo o dejaron de pagar requeriría otra medición.

### 00:18–00:39 · Unidad de análisis

*Muestre el mapa y señale los límites entre zonas.*

Una comuna puede tener varios puntos de recarga en su centro y pocos en los sectores más alejados. Por eso comparamos zonas de transporte más pequeñas. Dentro de esas zonas revisamos paraderos para encontrar sitios concretos que podrían beneficiarse de una recarga cercana.

> **Para quien presenta.** Una zona permite comparar sectores dentro de una comuna. El paradero permite proponer un lugar concreto para visitar. «Zona 777» es el nombre de la cartografía usada. El archivo contiene 803 códigos distintos y en 793 se pudieron comparar viajes de origen y subidas de bus.

### 00:39–01:01 · Fuentes

*Muestre el período y las tres cifras de la lámina.*

Procesamos más de quince millones de viajes iniciados entre el once y el diecisiete de abril de dos mil veintiséis. Cruzamos las subidas laborales de casi doce mil paraderos con el catastro de puntos de recarga. Para las estaciones de Metro usamos sus ubicaciones del registro de transporte de abril.

> **Para quien presenta.** Un viaje comienza cuando alguien inicia su desplazamiento. Una subida ocurre cada vez que aborda un bus. Quien toma dos buses para ir al trabajo puede aportar un viaje y dos subidas. Para medir demanda por zona contamos inicios de viaje. Para medir a cuánta actividad afecta una brecha usamos las subidas promedio de un día laboral de abril.

### 01:01–01:21 · Cruce de datos

*Señale la proporción de subidas ubicadas y las recargas de Metro y la Intermodal Aeropuerto.*

Con el registro de transporte, llamado GTFS, ubicamos casi todas las subidas de bus. El DTPM confirma recarga en todas las estaciones de Metro y usamos el mismo registro para ubicarlas. También incorporamos la recarga confirmada en la Intermodal Aeropuerto.

> **Para quien presenta.** GTFS es el archivo que publica las rutas y ubicaciones del transporte. El código público permitió situar 11.929 paraderos. El catastro de Metro ya incluía recarga, pero 12 de sus 143 filas estaban a más de 500 m de la estación correspondiente. Al reunir las combinaciones contamos 126 ubicaciones de Metro entre 1.900 puntos. En Del Sol, corregir la ubicación redujo la distancia estimada desde el paradero de 778 a 89 m.

### 01:21–01:43 · Accesibilidad

*Muestre los radios de 300 y 500 metros.*

Usamos un árbol espacial, llamado cKDTree, para encontrar el punto de recarga más cercano a cada paradero. Medimos en línea recta. A trescientos metros queda fuera de cobertura el veinte coma uno por ciento de las subidas de bus. A quinientos metros, baja al siete coma uno por ciento.

> **Para quien presenta.** El árbol espacial acelera la búsqueda entre los 1.900 puntos. Un local al otro lado del límite de una zona también cuenta. Al ampliar el radio a 500 m quedan fuera 2.089 paraderos. El 7,1 % usa como denominador todas las subidas de bus enlazadas. Una avenida sin cruce cercano puede alargar la caminata aunque el mapa muestre poca distancia.

### 01:43–02:06 · Cuadrantes

*Señale los puntos rojos del gráfico de zonas.*

Cada punto del gráfico representa una zona. Hacia la derecha aumentan los viajes. Hacia arriba aumenta la proporción de subidas sin recarga cerca. Las líneas marcan dónde empieza el cuarto superior de cada indicador. De setecientas noventa y tres zonas comparables, veintiséis quedan arriba a la derecha y son prioritarias.

> **Para quien presenta.** Para leer el gráfico, elijan un punto y háganle dos preguntas. ¿En esa zona empiezan al menos 2.406 viajes por día laboral? ¿Al menos un 13,37 % de sus subidas ocurre en paraderos sin recarga a 500 m? Si cumple ambos cortes, entra en las 26 zonas críticas. El corte de brecha se muestra redondeado. Estos umbrales se calcularon con las zonas de la muestra.

### 02:06–02:27 · PCA y segmentación

*Señale los dos perfiles que muestra el gráfico.*

PCA resume cinco medidas en dos ejes y conserva algo más del setenta y cinco por ciento de su variación. K-Means reúne zonas parecidas y usamos la silueta para elegir dos grupos. Agrupar ayuda a describir patrones. Los cuadrantes señalan cuáles zonas requieren más atención.

> **Para quien presenta.** Las cinco medidas son viajes, porcentaje en hora punta, puntos de recarga dentro de la zona, distancia promedio ponderada por subidas y porcentaje de subidas fuera de 500 m. PCA combina esas medidas para dibujarlas en dos ejes. K-Means agrupa usando las cinco medidas transformadas y estandarizadas. La silueta compara cuánto se parece cada zona a su propio grupo frente al grupo vecino. El mejor valor entre dos y ocho grupos se obtuvo con dos.

### 02:27–02:52 · Regresión

*Señale las dos cifras de error.*

Ridge y Random Forest estiman cuántas subidas tiene un paradero. Probamos ambos en comunas que quedaron fuera del entrenamiento. La variante logarítmica de Random Forest se equivocó en promedio por unas ciento cuarenta y una subidas al día. Ridge obtuvo menor RMSE, una medida que penaliza más los errores grandes.

> **Para quien presenta.** Ridge es una regresión lineal regularizada. Random Forest promedia las estimaciones de muchos árboles. Los probamos en comunas reservadas para ver cómo estiman demanda en otros territorios. MAE significa error absoluto medio y se lee en subidas por día. RMSE da más peso a los errores grandes. Para decidir qué sitios evaluar usamos las subidas observadas y la distancia a la recarga.

### 02:52–03:14 · Pronóstico

*Señale las curvas del viernes y destaque el resultado de la referencia.*

El pronóstico responde otra pregunta. ¿Cuántos viajes empiezan por hora en toda la red? Comparamos ARIMA, SARIMA y la misma hora del día anterior en tres fechas. La referencia del día anterior obtuvo el menor error medio, cinco mil ochocientos cuarenta y siete viajes por hora.

> **Para quien presenta.** Para pronosticar las ocho de la mañana del viernes, la referencia usa los viajes del jueves a las ocho. ARIMA aprovecha la evolución reciente y SARIMA incorpora además un ciclo diario. Se evaluaron tres períodos de 24 horas. El error se expresa en viajes por hora para toda la red. Esta pregunta temporal es distinta de estimar subidas por paradero.

### 03:14–03:35 · Emparejamiento

*Señale la diferencia observada tras emparejar.*

También comparamos paraderos con y sin recarga a trescientos metros, emparejándolos según sus características geográficas. Los paraderos con recarga cercana registraron, en promedio, unas ciento setenta y cuatro subidas más por día laboral. Este resultado describe una asociación. El comercio, la conectividad y la frecuencia de buses pueden influir en ella.

> **Para quien presenta.** El emparejamiento busca paraderos con ubicación y distancia al centro similares, uno con recarga cercana y otro sin ella. Así se reduce parte de la diferencia geográfica. Un sector comercial también puede atraer más pasajeros y más locales de recarga. Por eso las 174 subidas adicionales observadas no permiten predecir qué ocurriría al abrir un local.

### 03:35–03:59 · Sitios priorizados

*Muestre dónde se concentran los candidatos en el mapa y lea el primer candidato de la lámina.*

Para el ranking filtramos paraderos críticos que quedan sin recarga a quinientos metros. Luego ordenamos por subidas multiplicadas por distancia y exigimos doscientos metros entre los sitios elegidos. El primer candidato es Rotonda Pie Andino, en Lo Barnechea, con seiscientas noventa y cinco subidas laborales diarias.

> **Para quien presenta.** El filtro se calcula para cada paradero de bus. De 422 paraderos con demanda y distancia altas, 266 además carecen de recarga a 500 m. En Rotonda Pie Andino, código PC907, las 695 subidas diarias coinciden con una distancia de 2.041 m al punto registrado más cercano. Ese paradero encabeza la lista ordenada por subidas multiplicadas por distancia.

### 03:59–04:23 · Simulación

*Compare las dos líneas en el punto de 20 sitios.*

Con veinte sitios, el ranking del avance cubre cerca de veinticuatro mil subidas diarias en la simulación. Si elegimos cada punto por la cobertura nueva que aporta, llegamos a unas cuarenta y tres mil. Son subidas que ya existen y quedarían dentro de un radio de recarga.

> **Para quien presenta.** Si dos candidatos cubren el mismo paradero, sus subidas se cuentan una sola vez. Por eso la estrategia marginal vuelve a calcular qué sitio aporta más cobertura después de cada elección. Con 20 sitios, el índice alcanza unas 23.748 subidas diarias y la selección marginal 42.784. La diferencia es de unas 19.036 subidas existentes que quedarían cerca de una recarga.

### 04:23–04:41 · Transición al live demo

*Muestre el mapa y el orden de las tres acciones.*

En el mapa resaltamos las zonas críticas y abrimos el detalle de una. Las capas permiten ver buses, Metro, tren y puntos de recarga. Después cambiamos de estrategia para comparar la cobertura estimada.

> **Para quien presenta.** En el mapa, seleccionen PC907 con la estrategia «Índice del avance» y activen el radio del sitio. El círculo representa el alcance simulado de instalar allí una recarga. Los candidatos son paraderos de bus. Metro también integra la oferta de recarga y la capa Tren sirve de referencia territorial.

### 04:41–05:00 · Cierre

*Mantenga la lámina de conclusiones.*

El proyecto muestra qué sectores conviene investigar y qué paraderos merece la pena visitar primero. Antes de decidir dónde instalar una recarga, hay que confirmar si los puntos del listado siguen activos, cómo se llega a pie y qué locales pueden ofrecer el servicio. Gracias.

> **Para quien presenta.** En terreno conviene recorrer el trayecto desde el paradero al local, comprobar sus horarios y consultar si podría ofrecer recarga. Esa visita permite pasar de una prioridad calculada con datos de abril a una decisión de instalación.

### Fuentes para la presentación

- Recarga física bip! en estaciones de Metro. [Red Movilidad](https://www.red.cl/tarifas-y-recargas/tarjeta-bip/)
- Dos máquinas de recarga física en la Intermodal Aeropuerto desde septiembre de 2025. La ubicación que usamos es la del paradero dentro de la Intermodal. [Red Movilidad](https://www.red.cl/red-comunica/buses-red-al-aeropuerto-reportan-mas-de-2-millones-y-medio-de-transacciones-y-suman-maquinas-de-venta-de-tarjetas-bip/)

Las cifras del diagnóstico, los modelos y los escenarios se pueden consultar en el [resumen de la ejecución](resultados_integral/resumen_auditoria.json), la [comparación de regresores](resultados_integral/metricas_sensibilidad_espacial.csv) y el [ranking de sitios](resultados_integral/ranking_candidatos_bip.csv).
