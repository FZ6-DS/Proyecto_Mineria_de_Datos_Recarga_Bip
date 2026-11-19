"""Lectura de fuentes y cruce territorial para la entrega IIC2433."""

import json
import re
import unicodedata
from zipfile import ZipFile

import numpy as np
import openpyxl
import pandas as pd
from scipy.spatial import cKDTree


def normalizar(valor):
    if pd.isna(valor):
        return ""
    texto = unicodedata.normalize("NFKD", str(valor))
    return "".join(c for c in texto if not unicodedata.combining(c)).strip().upper()


def agregar_viajes(carpeta, resultados):
    """Acumula conteos horarios y zonales, sin cargar identificadores personales."""
    archivos = {}
    for ruta in carpeta.rglob("*.viajes.csv"):
        coincidencia = re.fullmatch(r"(\d{4}-\d\d-\d\d)\.viajes\.csv", ruta.name)
        if ruta.is_file() and coincidencia:
            fecha = pd.Timestamp(coincidencia[1])
            if fecha in archivos:
                raise ValueError(f"Dos archivos de viajes para {fecha.date()}")
            archivos[fecha] = ruta
    fechas = pd.date_range("2026-04-11", "2026-04-17", freq="D")
    if set(archivos) != set(fechas):
        raise ValueError("Se esperan los siete CSV diarios del 11 al 17 de abril de 2026")

    horarios, zonas, control = [], [], []
    columnas = ["tiempo_inicio_viaje", "zona_inicio_viaje"]
    for fecha in fechas:
        total_hora = np.zeros(24, dtype="int64")
        parciales = []
        n_leidas = 0
        for bloque in pd.read_csv(archivos[fecha], sep="|", encoding="latin1",
                                 usecols=columnas, dtype="str", chunksize=300_000):
            n_leidas += len(bloque)
            tiempo = pd.to_datetime(bloque.tiempo_inicio_viaje, format="%Y-%m-%d %H:%M:%S",
                                    errors="coerce")
            validos = tiempo.ge(fecha) & tiempo.lt(fecha + pd.Timedelta(days=1))
            hora = tiempo[validos].dt.hour.to_numpy(dtype=int)
            total_hora += np.bincount(hora, minlength=24)
            codigo = pd.to_numeric(bloque.loc[validos, "zona_inicio_viaje"], errors="coerce")
            codigo = codigo.where(codigo.between(0, 9999) & codigo.mod(1).eq(0), -1).astype(int)
            punta = ((hora >= 7) & (hora < 9)) | ((hora >= 17) & (hora < 20))
            datos = pd.DataFrame({"zona_777": codigo.to_numpy(), "viajes": 1, "punta": punta})
            parciales.append(datos.groupby("zona_777")[["viajes", "punta"]].sum())
        if not parciales or not total_hora.sum():
            raise ValueError(f"Sin viajes válidos el {fecha.date()}")
        zona_dia = pd.concat(parciales).groupby(level=0).sum().reset_index()
        zonas.append(zona_dia.assign(fecha=fecha))
        horarios.append(pd.DataFrame({"fecha_hora": pd.date_range(fecha, periods=24, freq="h"),
                                     "viajes_totales": total_hora}))
        control.append({"fecha": fecha.date().isoformat(), "filas": n_leidas,
                        "viajes_validos": int(total_hora.sum()),
                        "fecha_invalida_o_fuera_del_dia": n_leidas - int(total_hora.sum())})
        print(f"{fecha.date()} · {int(total_hora.sum()):,} viajes con fecha válida", flush=True)

    horario = pd.concat(horarios, ignore_index=True)
    zonal_dia = pd.concat(zonas, ignore_index=True)
    assert horario.viajes_totales.sum() == zonal_dia.viajes.sum()
    horario.to_csv(resultados / "serie_temporal_viajes_horarios.csv", index=False)
    zonal_dia.to_csv(resultados / "viajes_por_zona_y_dia.csv", index=False)
    pd.DataFrame(control).to_csv(resultados / "auditoria_viajes.csv", index=False)
    return horario, zonal_dia, pd.DataFrame(control)


def leer_demanda_bus(ruta):
    """DTPM informa subidas promedio por media hora, tipo de día y modo."""
    libro = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    try:
        filas = libro["SUBIDAS_2026_04"].values
        columnas = tuple(next(filas))
        esperadas = ("Tipo_dia", "Modo", "Paradero", "Paradero Usuario", "Comuna",
                     "Media_hora", "Subidas_Promedio")
        if columnas != esperadas:
            raise ValueError(f"Esquema de subidas DTPM inesperado: {columnas}")
        registros = [(str(codigo).strip().upper(), str(publico or "").strip().upper(),
                      str(comuna or ""), media.hour, float(subidas))
                     for dia, modo, codigo, publico, comuna, media, subidas in filas
                     if dia == "LABORAL" and modo == "BUS" and codigo and media is not None
                     and subidas is not None and float(subidas) >= 0]
    finally:
        libro.close()
    datos = pd.DataFrame(registros, columns=["PARADA", "CODIGO_PUBLICO", "COMUNA_DTPM",
                                            "HORA", "SUBIDAS_LABORAL"])
    datos["subidas_punta"] = datos.SUBIDAS_LABORAL.where(
        datos.HORA.between(7, 8) | datos.HORA.between(17, 19), 0)
    return datos.groupby("PARADA", as_index=False).agg(
        CODIGO_PUBLICO=("CODIGO_PUBLICO", "first"), COMUNA_DTPM=("COMUNA_DTPM", "first"),
        SUBIDAS_LABORAL=("SUBIDAS_LABORAL", "sum"), subidas_punta=("subidas_punta", "sum"))


def leer_paraderos_gtfs(ruta):
    """stop_id contiene los códigos públicos de la red. Conserva solo rutas de bus."""
    from pyproj import Transformer

    with ZipFile(ruta) as gtfs:
        def tabla(nombre, columnas):
            with gtfs.open(nombre + ".txt") as archivo:
                return pd.read_csv(archivo, usecols=columnas, dtype="str")

        version = tabla("feed_info", ["feed_start_date", "feed_version"])
        if version.feed_start_date.tolist() != ["20260418"]:
            raise ValueError("Se espera el GTFS de DTPM del 18 de abril de 2026")
        paradas = tabla("stops", ["stop_id", "stop_name", "stop_lat", "stop_lon"])
        rutas = tabla("routes", ["route_id", "route_type"])
        buses = rutas.loc[rutas.route_type.eq("3"), "route_id"]
        viajes = tabla("trips", ["trip_id", "route_id"])
        viajes_bus = viajes.loc[viajes.route_id.isin(buses)]
        horarios = tabla("stop_times", ["trip_id", "stop_id"])
        rutas_por_parada = (horarios.merge(viajes_bus, on="trip_id", validate="m:1")
                            .groupby("stop_id").route_id.nunique().rename("rutas_bus_gtfs"))
    paradas = paradas.join(rutas_por_parada, on="stop_id", how="inner")
    lat = pd.to_numeric(paradas.stop_lat, errors="coerce")
    lon = pd.to_numeric(paradas.stop_lon, errors="coerce")
    paradas = paradas.loc[lat.between(-35, -32) & lon.between(-72, -69)].copy()
    convertir = Transformer.from_crs(4326, 32719, always_xy=True)
    paradas["X_UTM"], paradas["Y_UTM"] = convertir.transform(
        lon.loc[paradas.index].to_numpy(), lat.loc[paradas.index].to_numpy())
    paradas = paradas.rename(columns={"stop_id": "CODIGO_PUBLICO", "stop_name": "REFERENCIA"})
    paradas["REFERENCIA"] = paradas.REFERENCIA.str.replace(r"^[A-Z0-9]+-", "", regex=True)
    return paradas[["CODIGO_PUBLICO", "REFERENCIA", "X_UTM", "Y_UTM", "rutas_bus_gtfs"]]


def leer_poligonos(ruta):
    import shapefile
    import shapely
    from pyproj import Transformer
    from shapely.ops import transform

    # El archivo no trae .prj. Sus coordenadas corresponden a longitudes y latitudes de Santiago.
    proyectar = Transformer.from_crs(4326, 32719, always_xy=True).transform
    componentes, comunas = {}, {}
    with shapefile.Reader(str(ruta), encoding="latin1") as lector:
        if not (-72 < lector.bbox[0] < lector.bbox[2] < -69 and
                -35 < lector.bbox[1] < lector.bbox[3] < -32):
            raise ValueError("La extensión del shapefile no es compatible con Santiago en grados")
        for registro in lector.iterShapeRecords():
            zona = int(registro.record["ZONA777"])
            forma = shapely.make_valid(shapely.geometry.shape(registro.shape.__geo_interface__))
            poligonos = [p for p in shapely.get_parts(forma) if p.geom_type in {"Polygon", "MultiPolygon"}]
            if poligonos:
                componentes.setdefault(zona, []).extend(transform(proyectar, p) for p in poligonos)
                comunas[zona] = registro.record["COMUNA"].strip().title()
    geometrias = {zona: shapely.union_all(componentes[zona]) for zona in sorted(componentes)}
    return geometrias, comunas


def asignar_poligonos(geometrias, x, y):
    import shapely

    codigos = np.array(list(geometrias))
    formas = list(geometrias.values())
    arbol = shapely.STRtree(formas)
    puntos, figuras = arbol.query(shapely.points(x, y), predicate="covered_by")
    coincidencias = pd.DataFrame({"fila": puntos, "zona": codigos[figuras],
                                  "area": shapely.area(formas)[figuras]})
    # En bordes o solapamientos, el polígono menor tiene precedencia. Luego, el código menor.
    asignadas = (coincidencias.sort_values(["area", "zona"]).drop_duplicates("fila")
                 .set_index("fila").zona.reindex(range(len(x))).astype("Int64"))
    return asignadas, int(coincidencias.fila.duplicated().sum())


def construir_zonas(geometrias, comunas, viajes_diarios, maestro, df_bip):
    universo = pd.DataFrame({"zona_777": list(geometrias), "comuna_cartografica": list(comunas[z] for z in geometrias)})
    laborales = viajes_diarios.loc[viajes_diarios.fecha.dt.dayofweek < 5]
    acumulado = laborales.groupby("zona_777", as_index=False)[["viajes", "punta"]].sum()
    zonas = universo.merge(acumulado, on="zona_777", how="left", validate="1:1")
    zonas[["viajes", "punta"]] = zonas[["viajes", "punta"]].fillna(0).astype(int)
    dias = laborales.fecha.nunique()
    zonas["viajes_laborales_dia"] = zonas.viajes / dias
    zonas["pct_viajes_punta"] = 100 * zonas.punta.div(zonas.viajes.where(zonas.viajes.gt(0)))
    oferta = df_bip.groupby("zona_777").size().rename("puntos_bip_internos")
    zonas = zonas.join(oferta, on="zona_777")
    zonas["puntos_bip_internos"] = zonas.puntos_bip_internos.fillna(0).astype(int)

    acceso = maestro.assign(distancia_ponderada=maestro.SUBIDAS_LABORAL * maestro.distancia_min_bip_m)
    for radio in (300, 500):
        acceso[f"subidas_sin_{radio}m"] = acceso.SUBIDAS_LABORAL.where(acceso[f"bip_en_{radio}m"].eq(0), 0)
    paradas = acceso.groupby("zona_777").agg(
        paraderos_bus=("PARADA", "size"), subidas_bus_dia=("SUBIDAS_LABORAL", "sum"),
        distancia_ponderada=("distancia_ponderada", "sum"),
        subidas_sin_300m=("subidas_sin_300m", "sum"), subidas_sin_500m=("subidas_sin_500m", "sum"))
    zonas = zonas.join(paradas, on="zona_777")
    zonas["paraderos_bus"] = zonas.paraderos_bus.fillna(0).astype(int)
    zonas["distancia_media_ponderada_m"] = zonas.distancia_ponderada / zonas.subidas_bus_dia
    for radio in (300, 500):
        zonas[f"pct_subidas_sin_{radio}m"] = 100 * zonas[f"subidas_sin_{radio}m"] / zonas.subidas_bus_dia
    return zonas.drop(columns="distancia_ponderada")


def simular_cobertura(maestro, candidatos, ranking, radio, limite, separacion):
    """Compara el ranking original y una selección por cobertura marginal de subidas."""
    sin_cobertura = maestro.loc[maestro[f"bip_en_{radio}m"].eq(0)]
    xy_objetivo = sin_cobertura[["X_UTM", "Y_UTM"]].to_numpy()
    xy_candidatos = candidatos[["X_UTM", "Y_UTM"]].to_numpy()
    pesos = sin_cobertura.SUBIDAS_LABORAL.to_numpy()
    vecinos = [np.asarray(i, dtype=int) for i in cKDTree(xy_objetivo).query_ball_point(xy_candidatos, radio)]
    cercanos = cKDTree(xy_candidatos).query_ball_point(xy_candidatos, separacion)
    posiciones = {codigo: pos for pos, codigo in enumerate(candidatos.PARADA)}
    por_indice = [posiciones[codigo] for codigo in ranking.PARADA]
    salidas = []
    for metodo in ("Índice del avance", "Cobertura marginal"):
        cubiertos = np.zeros(len(pesos), dtype=bool)
        disponibles = np.ones(len(vecinos), dtype=bool)
        for paso in range(min(limite, len(por_indice))):
            if metodo == "Índice del avance":
                elegido = por_indice[paso]
            else:
                ganancias = np.full(len(vecinos), -1.0)
                for pos in np.flatnonzero(disponibles):
                    vec = vecinos[pos]
                    ganancias[pos] = pesos[vec[~cubiertos[vec]]].sum()
                elegido = int(np.argmax(ganancias))
                if ganancias[elegido] < 0:
                    break
                disponibles[elegido] = False
                for pos in cercanos[elegido]:
                    if np.linalg.norm(xy_candidatos[pos] - xy_candidatos[elegido]) < separacion:
                        disponibles[pos] = False
            vec = vecinos[elegido]
            ganancia = float(pesos[vec[~cubiertos[vec]]].sum())
            cubiertos[vec] = True
            salidas.append({"metodo": metodo, "sitios": paso + 1, "paradero": candidatos.PARADA.iloc[elegido],
                            "subidas_adicionales_con_cobertura": ganancia,
                            "subidas_acumuladas_con_cobertura": float(pesos[cubiertos].sum()),
                            "paraderos_cubiertos": int(cubiertos.sum())})
    return pd.DataFrame(salidas)


def exportar_mapa(ruta, plantilla, geometrias, zonas, df_bip, candidatos, cobertura):
    import shapely

    def registros(tabla, columnas):
        return json.loads(tabla[columnas].round(2).to_json(orient="records", force_ascii=False))

    zonas_mapa = registros(zonas, ["zona_777", "comuna_cartografica", "cuadrante", "perfil",
                                  "puntos_bip_internos", "viajes_laborales_dia", "subidas_bus_dia",
                                  "pct_subidas_sin_300m", "pct_subidas_sin_500m",
                                  "distancia_media_ponderada_m"])
    for zona in zonas_mapa:
        geom = geometrias[zona["zona_777"]].simplify(5, preserve_topology=True)
        zona["poligonos"] = [[[[round(x), round(y)] for x, y in anillo.coords]
                              for anillo in (parte.exterior, *parte.interiors)]
                             for parte in shapely.get_parts(geom)]
    datos = {
        "zonas": zonas_mapa,
        "bip": registros(df_bip, ["ESTE", "NORTE", "ENTIDAD"]),
        "sitios": registros(candidatos.loc[candidatos.PARADA.isin(cobertura.paradero)],
                            ["PARADA", "CODIGO_PUBLICO", "COMUNA", "REFERENCIA", "X_UTM", "Y_UTM",
                             "SUBIDAS_LABORAL", "distancia_min_bip_m", "zona_777"]),
        "cobertura": registros(cobertura, ["metodo", "sitios", "paradero", "subidas_acumuladas_con_cobertura"]),
    }
    contenido = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    ruta.write_text(plantilla.read_text(encoding="utf-8").replace("__DATOS_PROYECTO__", contenido), encoding="utf-8")
