# Inventario de la entrega

El notebook integral contiene el código y la plantilla del mapa. La raíz reúne el notebook ejecutado, las dependencias, la documentación, el mapa autónomo, los dos PDF, el guion y el video final.

## Resultados publicados

Se conservan las tablas utilizadas para consultar el diagnóstico, comparar estrategias y verificar las cifras de la presentación.

- diagnostico_zona777.csv
- ranking_candidatos_bip.csv
- comparacion_cobertura_500m.csv
- auditoria_recarga_metro.csv
- metricas_sensibilidad_espacial.csv
- sensibilidad_radios.csv
- resumen_auditoria.json

El notebook regenera también los gráficos y tablas intermedias. Sus copias locales y el segundo HTML pueden archivarse. El notebook portable, su módulo, su plantilla y la antigua carpeta de resultados pertenecen a la versión anterior. Los fuentes LaTeX pueden guardarse con el material de edición.

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
| `datos_originales/GTFS_20260418.zip` | Fuente oficial de paraderos, estaciones de Metro y tren, rutas y correspondencias del 18 de abril de 2026. | Requerido localmente. Puede descargarse desde DTPM y guardarse en esta ruta. [GTFS oficial](https://www.dtpm.cl/descargas/gtfs/GTFS_20260418.zip) |

Para reproducir desde un clon, cree `datos_originales/` con la estructura indicada. Consiga los datos en las fuentes institucionales o en la copia local del equipo. El repositorio puede incluir los resultados agregados para que se puedan consultar sin tener las fuentes crudas.
