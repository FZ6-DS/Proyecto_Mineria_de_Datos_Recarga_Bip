# Desiertos de recarga bip! en Santiago

Entrega final de Minería de Datos IIC2433. El estudio diagnostica la accesibilidad a recarga por Zona 777 y prioriza paraderos donde conviene evaluar nuevos puntos.

## Entregables

- [Notebook ejecutado](Entrega_Final_BIP_Portable_Mapa_OK.ipynb). Incluye fuentes, limpieza, evaluación de modelos, resultados y controles de integridad.
- [Mapa para el live demo](Live_Demo_BIP.html). Ábralo directamente en un navegador. Los datos y la cartografía están incorporados en el HTML.
- [Video de cinco minutos](Presentacion_Final_BIP.mp4). La versión entregada usa texto en pantalla y gráficos, sin narración.
- [Guion de narración](Guion_Video_BIP.md), sincronizado con las 14 escenas del video.
- Informe del proyecto en [LaTeX](Informe_Proyecto_BIP.tex) y [PDF](Informe_Proyecto_BIP.pdf).
- [Cambios, inventario y limpieza del repositorio](Guia_Repositorio.md).
- [Diagnóstico por Zona 777](resultados/diagnostico_zona777.csv), [ranking de paraderos](resultados/ranking_candidatos_bip.csv) y [simulación de cobertura](resultados/comparacion_cobertura_500m.csv).

## Resultados

- Se procesaron **15.191.070 inicios de viaje** del 11 al 17 de abril de 2026. En la cartografía hay 803 códigos distintos. De 793 zonas con demanda y acceso comparables, **27** cruzan los cortes de alta demanda y alta brecha a 500 m.
- Se enlazaron 11.929 paraderos de bus con el GTFS del 18 de abril. Representan el 99,94% de las subidas laborales DTPM. A 500 m, 2.108 paraderos quedan fuera de cobertura, equivalentes al 7,73% de las subidas enlazadas.
- K-Means eligió **k=2** con silueta de 0,469. El perfil con mayor brecha incluye 113 zonas y una mediana de 71,5% de subidas fuera de cobertura a 500 m. Las medianas de cada clúster quedan por debajo de alguno de los dos cortes críticos. La matriz conserva la identificación de las 27 zonas individuales.
- Los dos componentes del PCA recogen el 74,7% de la variación. En el primero predominan la distancia ponderada y la proporción de subidas fuera del radio de 500 m. En el segundo predomina la proporción de viajes en hora punta.
- Para estimar subidas/día por paradero en comunas retenidas, Ridge con atributos de recarga obtuvo un MAE de 175,6 frente a 189,2 de Random Forest y 222,7 de la media de entrenamiento. Para pronosticar viajes/hora, el baseline de la misma hora del día anterior obtuvo el menor MAE medio, 5.847, frente a 7.127 de SARIMA. Las dos comparaciones usan objetivos y particiones propios.
- Con 20 sitios simulados, la estrategia de cobertura marginal deja **54.091 subidas laborales/día** al alcance de un punto nuevo, frente a **35.877** con el orden del índice del avance. Se contabilizan subidas ya observadas y los radios se miden en línea recta.

## Live demo

1. Abra el HTML. En **Resaltar zonas**, elija **Prioridad crítica** y haga clic en un polígono rojo. Muestre viajes laborales, puntos dentro de la zona, y el porcentaje de subidas sin recarga a 300 y 500 m.
2. Active **Puntos bip!**. Seleccione **PI1788** en el ranking y active **Radio del sitio activo**. El paradero del Intermodal Del Sol registra 8.021 subidas laborales diarias. El catastro ubica el punto más cercano a 778 m en línea recta.
3. Alterne entre **Índice del avance** y **Cobertura marginal**. Compare el total en la tarjeta y abra un sitio de cada estrategia. El escenario mantiene fijo el número de emplazamientos.

## Reproducir el análisis

Instale las dependencias en el entorno del kernel con `python -m pip install -r requirements.txt`. Abra el notebook en Jupyter desde esta carpeta y use **Ejecutar todo**. Se requieren los archivos bajo `datos_originales/` (incluido el GTFS). El notebook recorre los CSV diarios por bloques, regenera los archivos de `resultados/` y reconstruye el HTML con `mapa_bip_plantilla.html`.

Para compilar el informe desde la raíz, ejecute `tectonic Informe_Proyecto_BIP.tex`. Mantenga las cuatro figuras que el informe lee desde `resultados/`.

Las fuentes principales son la matriz ADATRAP y las subidas DTPM de abril de 2026, los polígonos Zona 777 de 2014, el GTFS que entró en vigencia el 18 de abril de 2026 y el catastro bip! local de septiembre de 2024. Para verificar sitios se requiere un catastro vigente, la red peatonal efectiva y la disponibilidad de locales. El análisis de propensión describe una asociación observacional. [Matrices de viaje y subidas DTPM](https://www.dtpm.cl/index.php/documentos/matrices-de-viaje) · [GTFS oficial](https://www.dtpm.cl/descargas/gtfs/GTFS_20260418.zip) · [Portal de Datos Abiertos](https://datos.gob.cl/es/group/transporte)
