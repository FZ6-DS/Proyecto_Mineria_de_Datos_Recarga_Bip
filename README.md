# Desiertos de recarga bip! en Santiago

Entrega final de Minería de Datos IIC2433. El estudio diagnostica la accesibilidad a recarga por Zona 777 y prioriza paraderos donde conviene evaluar nuevos puntos.

## Entregables

- [Notebook integral](Notebook_Integral_Recarga_BIP.ipynb). Reúne la EDA histórica, el código del proyecto y el análisis actualizado.
- [Mapa para el live demo](Live_Demo_BIP.html). Ábralo directamente en un navegador. Los datos y la cartografía están incorporados en el HTML.
- [Video de cinco minutos](Presentacion_Final_BIP.mp4). La versión entregada usa texto en pantalla y gráficos, sin narración.
- [Guion de narración](Guion_Video_BIP.md), sincronizado con las 14 escenas del video.
- Informe del proyecto en [PDF](Informe_Proyecto_BIP.pdf).
- Guía para preparar la defensa en [PDF](Preguntas_Defensa_BIP.pdf).
- [Cambios, inventario y limpieza del repositorio](Guia_Repositorio.md).
- [Diagnóstico por Zona 777](resultados_integral/diagnostico_zona777.csv), [ranking de paraderos](resultados_integral/ranking_candidatos_bip.csv) y [simulación de cobertura](resultados_integral/comparacion_cobertura_500m.csv).

## Resultados

- Se procesaron **15.191.070 inicios de viaje** del 11 al 17 de abril de 2026. En la cartografía hay 803 códigos distintos. De 793 zonas con demanda y acceso comparables, **26** cruzan los cortes de alta demanda y alta brecha a 500 m.
- El cálculo incluye **1.900 puntos de recarga**, entre ellos las **126 estaciones de Metro** del GTFS. En el Excel de Metro, 12 de 143 registros por línea y estación estaban a más de 500 m de su ubicación GTFS. El paradero **PI1788** del Intermodal Del Sol pasó de **778 m a 89 m** del punto de carga más cercano y salió de la lista de candidatos. [Auditoría de la conciliación Metro](resultados_integral/auditoria_recarga_metro.csv)
- Se enlazaron 11.929 paraderos de bus con el GTFS del 18 de abril. Representan el 99,94% de las subidas laborales DTPM. A 500 m, **2.089 paraderos** quedan fuera de cobertura, equivalentes al **7,08%** de las subidas enlazadas.
- K-Means eligió **k=2** con silueta de 0,474. El perfil con mayor brecha incluye 110 zonas y una mediana de 70,7% de subidas fuera de cobertura a 500 m. Las medianas de cada clúster quedan por debajo de alguno de los dos cortes críticos.
- Los dos componentes del PCA recogen el 75,4% de la variación. En el primero predominan la distancia ponderada y la proporción de subidas fuera del radio de 500 m. En el segundo predomina la proporción de viajes en hora punta.
- Para estimar subidas/día por paradero en comunas retenidas, Ridge con atributos de recarga obtuvo un MAE de 175,8 frente a 180,6 de Random Forest y 222,7 de la media de entrenamiento. Para pronosticar viajes/hora, la referencia de la misma hora del día anterior obtuvo el menor MAE medio, 5.847, frente a 7.127 de SARIMA. Las dos comparaciones usan objetivos y particiones propios.
- Con 20 sitios simulados, la estrategia de cobertura marginal deja **42.784 subidas laborales/día** al alcance de un punto nuevo, frente a **23.748** con el orden del índice del avance. Se contabilizan subidas ya observadas y los radios se miden en línea recta.

## Live demo

1. Abra el HTML. En **Resaltar zonas**, elija **Prioridad crítica** y haga clic en un polígono rojo. Muestre viajes laborales, puntos dentro de la zona, y el porcentaje de subidas sin recarga a 300 y 500 m.
2. Active **Puntos bip!**. Con **Índice del avance**, seleccione **PC907** y active **Radio del sitio activo**. En Rotonda Pie Andino, Lo Barnechea, se observan 695 subidas diarias y el punto de recarga más cercano está a 2.041 m en línea recta.
3. Alterne entre **Índice del avance** y **Cobertura marginal**. Compare el total en la tarjeta y abra un sitio de cada estrategia. El escenario mantiene fijo el número de emplazamientos.
4. Active **Bus**, **Metro** o **Tren** para ver cada modo. Los candidatos de ambas estrategias son paraderos de bus. La capa **Puntos bip!** incluye las estaciones de Metro usadas como puntos de recarga. La capa **Tren** sirve de referencia territorial.

## Reproducir el análisis

Instale las dependencias en el entorno del kernel con `python -m pip install -r requirements.txt`. Abra el notebook en Jupyter desde esta carpeta y use **Ejecutar todo**. Se requieren los archivos bajo `datos_originales/` (incluido el GTFS). El notebook recorre los CSV diarios por bloques, genera las tablas, figuras y el mapa en resultados_integral/. La plantilla está incluida en el notebook. Para actualizar la demo publicada, copie el HTML generado a la raíz.

Las fuentes principales son la matriz ADATRAP y las subidas DTPM de abril de 2026, los polígonos Zona 777 de 2014, el GTFS que entró en vigencia el 18 de abril de 2026 y el catastro bip! local de septiembre de 2024. Red Movilidad indica que se puede cargar en todas las boleterías del Metro. El catastro Excel ya incluía puntos Metro. Al contrastar sus coordenadas con las del GTFS se detectaron desplazamientos. El cruce por nombre une los registros que documentan la recarga con una ubicación GTFS por estación. Esa coordenada aproxima la ubicación de la recarga dentro de la estación. La capa de tren aporta contexto territorial. Para evaluar una instalación se requiere confirmar el acceso peatonal, los horarios y la disponibilidad de locales. El análisis de propensión describe una asociación observacional. [Matrices de viaje y subidas DTPM](https://www.dtpm.cl/index.php/documentos/matrices-de-viaje) · [GTFS oficial](https://www.dtpm.cl/descargas/gtfs/GTFS_20260418.zip) · [Dónde recargar según Red Movilidad](https://www.red.cl/tarifas-y-recargas/tarjeta-bip/) · [Recurso Metro del catastro abierto](https://datos.gob.cl/dataset/33355/resource/3d54e961-d81b-4507-aeee-7a433e00a9bf)
