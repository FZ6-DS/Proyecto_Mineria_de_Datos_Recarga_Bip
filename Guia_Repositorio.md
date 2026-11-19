# Cambios, inventario y preparación del repositorio

## Qué cambió desde el avance

1. **Zona 777 pasó a ser la unidad principal.** El avance mapeaba la accesibilidad por paradero. La entrega final agrega los CSV de ADATRAP por `zona_inicio_viaje` y cruza los puntos bip! con los polígonos. La capa contiene 803 códigos distintos y 793 zonas con datos comparables. La matriz se calcula tanto para zonas como para paraderos.
2. **La demanda de bus se actualizó a abril de 2026.** El diccionario histórico enlazaba solo el 58,03 % de las subidas de 2026 por código interno. La unión del código público de DTPM con `stop_id` del GTFS del 18 de abril ubicó el 99,94 %. El diccionario histórico sirve como control de concordancia cartográfica. El GTFS empieza un día después del período de demanda.
3. **La accesibilidad incorpora cruces de límites.** `cKDTree` calcula la distancia al punto de recarga más cercano y los conteos a 300 y 500 m con todo el catastro. Por zona se informa además la oferta contenida en el polígono. Así se puede reconocer acceso dentro del radio aun cuando una zona tenga cero puntos en su interior.
4. **PCA y K-Means se aplican a zonas.** Se estandarizan cinco variables, se muestran las cargas del PCA y se prueban siete valores de `k` con inercia y silueta. El mejor valor fue `k=2`. Las medianas de los dos clústeres no cruzan ambos cortes críticos y la matriz conserva la identificación individual de 27 zonas. El tiempo de espera se omitió porque su equivalencia con el diccionario disponible era incierta.
5. **Cada modelo tiene una pregunta y una validación.** Ridge y Random Forest estiman subidas/día en comunas retenidas y se comparan con la media de entrenamiento. Ridge se evalúa con y sin atributos de recarga. ARIMA y SARIMA pronostican viajes/hora en tres fechas y se comparan con la misma hora del día anterior. El emparejamiento de propensión se interpreta como asociación observacional.
6. **La cobertura simulada agrega una comparación de ubicaciones.** Se mantiene el índice de priorización del avance y se agrega la selección por ganancia marginal. Ambas estrategias usan los mismos candidatos, presupuesto y separación mínima. El mapa sin conexión permite verlas, comparar la cobertura y abrir los detalles.
7. **Los resultados se recalcularon.** El notebook ejecutado contiene tablas, gráficos y verificaciones. El video, el guion y el informe usan los resultados de esa ejecución.

## Archivos de la raíz

| Archivo | Para qué sirve | Tratamiento recomendado |
|---|---|---|
| `README.md` | Resumen, accesos rápidos y pasos de reproducción. | Publicar. |
| `Guia_Repositorio.md` | Inventario, cambios y criterios de limpieza. | Publicar. |
| `Entrega_Final_BIP_Portable_Mapa_OK.ipynb` | Entrada principal. Limpia, analiza, entrena, grafica y exporta. Incluye resultados ejecutados. | Publicar. |
| `proyecto_bip.py` | Funciones de lectura, unión espacial, agregación, simulación y exportación del mapa. El notebook lo importa. | Publicar. |
| `requirements.txt` | Dependencias de Python para reproducir el notebook. | Publicar. |
| `mapa_bip_plantilla.html` | Plantilla de interfaz que recibe los resultados desde Python. | Publicar. |
| `Live_Demo_BIP.html` | Mapa final precalculado que abre en navegador y funciona sin conexión. | Publicar para mostrar el resultado sin ejecutar el notebook. Es regenerable. |
| `Presentacion_Final_BIP.mp4` | Video de cinco minutos con gráficos y texto, sin narración. | Publicar o adjuntar a la entrega. |
| `Guion_Video_BIP.md` | Narración y señales visuales alineadas con los cortes del video. | Publicar. |
| `Informe_Proyecto_BIP.tex` | Fuente editable del informe. Lee gráficos de `resultados/`. | Publicar. |
| `Informe_Proyecto_BIP.pdf` | Versión compilada del informe. | Publicar para lectura directa. |
| `Proyecto DM 2026-2.pdf` | Pauta del curso y antecedentes académicos. | Guardar fuera del repositorio público, salvo que el curso permita redistribuirla. |

## Fuentes locales

| Ruta o grupo | Para qué sirve | Tratamiento recomendado |
|---|---|---|
| `datos_originales/Viajes_2026-04/Tabla de Viajes/` | Siete CSV del 11 al 17 de abril. El notebook lee fecha y zona, pero los archivos crudos también contienen identificadores de tarjeta y de viaje. | **Excluir de Git y conservar una copia local protegida.** Son necesarios para regenerar los resultados. Los siete suman 6,64 GB y cada uno supera 100 MiB. [Límite de archivos de GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github) |
| `datos_originales/Subidas_Paradero_Estacion_2026.04_v3.xlsx` | Fuente de subidas promedio que se filtra a buses en días laborales. | Conservar localmente para ejecutar. [Fuente DTPM](https://www.dtpm.cl/index.php/documentos/matrices-de-viaje) |
| `datos_originales/Lugares de carga/` | Cinco catálogos Excel de puntos de recarga. `metro` corresponde a estaciones, `retail` a comercios y `pcma` y `pcmav` a puntos y centros de recarga. | Conservar los cinco para ejecutar. [Catastros de recarga](https://datos.gob.cl/es/group/transporte) |
| `datos_originales/Zona777_ADATRAP/DIC_777.xlsx` | Diccionario histórico de paradas. Permite auditar la cobertura del cruce por código interno y la concordancia de zonificación. | Conservar localmente para ejecutar. |
| `datos_originales/Zona777_ADATRAP/Zonas777-04-04-2014/Shape/` | Geometrías y atributos de Zona 777. El `.shp` contiene los polígonos, el `.shx` su índice y el `.DBF` los códigos y atributos. | Conservar los tres juntos, con sus nombres originales. |
| Otros archivos `Zonas777-V07-04-2014.*` fuera de `Shape/` | Archivos del paquete cartográfico original. El notebook no los abre. | Opcionales en una copia mínima. Conservarlos en el archivo de fuentes si interesa mantener la descarga completa. |
| `datos_originales/diccionario_campos.csv` y `Diccionario_campos_tabla_viajes_y_etapas(transparencia).xlsx` | Documentación de campos y unidades. | Conservar como referencia. El notebook se ejecuta sin ellos. |
| `datos_originales/GTFS_20260418.zip` | Fuente oficial de paraderos, rutas y correspondencias del 18 de abril de 2026. | Requerido localmente. Puede descargarse desde DTPM y guardarse en esta ruta. [GTFS oficial](https://www.dtpm.cl/descargas/gtfs/GTFS_20260418.zip) |

Para reproducir desde un clon, cree `datos_originales/` con la estructura indicada. Consiga los datos en las fuentes institucionales o en la copia local del equipo. El repositorio puede incluir los resultados agregados para que se puedan consultar sin tener las fuentes crudas.

## Archivos de `resultados/`

Todos estos archivos son regenerables con el notebook. Conservar los cuatro gráficos indicados permite compilar el informe inmediatamente desde el repositorio. El resto de los resultados agrega evidencia y facilita revisar la entrega.

| Archivo | Contenido |
|---|---|
| `auditoria_viajes.csv` | Filas leídas, viajes válidos y descartes, por fecha. |
| `viajes_por_zona_y_dia.csv` | Viajes y conteos de punta agregados por código y fecha. |
| `serie_temporal_viajes_horarios.csv` | Serie de 168 horas usada para el pronóstico. |
| `puntos_bip_consolidados.csv` | Catastro limpio, coordenadas y Zona 777 asignada. |
| `paraderos_sin_enlace_gtfs.csv` | Tres registros DTPM que quedaron fuera del cruce de paraderos. |
| `matriz_paraderos_modelado.csv` | Subidas, ubicación, distancias, oferta dentro de los radios y cuadrante de cada paradero. |
| `diagnostico_zona777.csv` | Demanda, oferta interna, brecha, cuadrante, PCA y clúster por código de zona. |
| `sensibilidad_radios.csv` | Paraderos y subidas fuera de los radios de 300 y 500 m. |
| `cargas_pca_zona777.csv` | Contribuciones de las variables a los dos componentes. |
| `evaluacion_kmeans_zona777.csv` | Inercia y silueta para `k` de 2 a 8. |
| `perfiles_zona777.csv` | Tamaños, medianas y zonas críticas de los clústeres. |
| `metricas_modelos_espaciales.csv` | MAE, RMSE y R² en comunas retenidas. |
| `metricas_modelos_temporales.csv` | Errores por modelo y fecha de prueba, con estado de convergencia. |
| `balance_emparejamiento_psm.csv` | Diferencias estandarizadas de las covariables antes y después del emparejamiento. |
| `ranking_candidatos_bip.csv` | Veinte sitios seleccionados por el índice del avance. |
| `comparacion_cobertura_500m.csv` | Sitios seleccionados, aporte marginal y cobertura acumulada para ambas estrategias. |
| `resumen_auditoria.json` | Indicadores y conteos de la ejecución, métricas y rutas relativas de fuentes. |
| `03_matriz_prioridad.png` | Cuadrantes para paraderos y zonas. **Lo usa el informe.** |
| `04_modelos_espaciales.png` | Comparación de MAE por regresor. |
| `05_pca_clustering.png` | Codo, silueta y proyección PCA. **Lo usa el informe.** |
| `06_pronostico_temporal.png` | Observado y pronosticado para el viernes 17. |
| `08_ranking_candidatos.png` | Curvas de cobertura acumulada de ambas estrategias. **Lo usa el informe.** |
| `09_mapa_zona777.png` | Mapa estático de cuadrantes y candidatos. **Lo usa el informe.** |

## Qué se puede limpiar

- **Eliminar de la copia de trabajo:** `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/` y los temporales de compilación de LaTeX (`.aux`, `.log`, `.out`, `.toc`, `.synctex.gz`), si aparecen. Se regeneran automáticamente.
- **Excluir de Git o eliminar después de guardar la entrega:** `.venv/` completa. Python y sus dependencias pueden reinstalarse. Aquí también quedaron pruebas y scripts auxiliares usados para producir y verificar el video y el PDF. Guarde `.venv/generar_video.py` y sus imágenes de escena en otra carpeta solo si quiere conservar ese proceso auxiliar de edición de video.
- **Archivar fuera del repositorio:** `Codigos pasados, errores y base/`. Incluye `EDA.ipynb` (exploración inicial), `avance_final.ipynb` (avance), `final.ipynb` y `Entrega_Final.ipynb` (iteraciones previas), `Entrega_Final_BIP_Portable_Mapa_OK_anterior.ipynb` (respaldo del notebook intervenido) y `resultados_anteriores/` (mapa y gráficos de versiones previas). El flujo final no depende de esos archivos.
- **Mantener fuera de Git y conservar localmente:** `datos_originales/` y el ZIP GTFS. El `.tex` y la demo publicada se pueden revisar sin estos datos. La reproducción completa los requiere.
- **Eliminar solo si va a regenerar:** `resultados/` y `Live_Demo_BIP.html`. Conviene subirlos para que el proyecto se pueda evaluar directamente y se pueda compilar el informe con sus figuras.

Ejemplo de reglas para un `.gitignore` si se publica el código, las figuras y los entregables:

```gitignore
/.venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
/datos_originales/
/Codigos pasados, errores y base/
/Proyecto DM 2026-2.pdf
*.aux
*.log
*.out
*.toc
*.synctex.gz
```

Antes del primer commit, revise `git status --short` y `git diff --cached --name-only` para confirmar que se seleccionaron los entregables y quedaron fuera las fuentes locales.
