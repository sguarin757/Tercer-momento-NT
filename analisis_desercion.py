import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

BASE = Path(__file__).parent
RAW = BASE / "Data" / "raw" / "datos_estudiantes.csv"
PROCESSED = BASE / "Data" / "processed"
GRAFICOS = PROCESSED / "graficos"
WEB = BASE / "web"

VALIDOS = {
    "programa": ["Administración de Empresas", "Contaduría Pública", "Derecho", "Psicología",
                 "Ingeniería de Sistemas", "Ingeniería Industrial", "Enfermería", "Diseño Gráfico"],
    "jornada": ["Diurna", "Nocturna", "Fin de semana"],
    "genero": ["Femenino", "Masculino"],
    "ciudad_procedencia": ["Bogotá", "Medellín", "Cali", "Bucaramanga", "Rionegro",
                           "Barranquilla", "Otra ciudad"],
}

EDAD_MIN, EDAD_MAX = 15, 60
PROMEDIO_MIN, PROMEDIO_MAX = 0, 5
HORAS_MAX = 100

DECISIONES = []
AUDITORIA = {}
RESPUESTAS = {}


def registrar(paso, columna, accion, filas, justificacion):
    DECISIONES.append({
        "paso": paso, "columna": columna, "accion": accion,
        "filas_afectadas": int(filas), "justificacion": justificacion,
    })


def titulo(texto):
    print("\n" + "=" * 80)
    print(texto)
    print("=" * 80)


def explorar(df):
    titulo("PASO 1. EXPLORACIÓN")
    print(f"Forma: {df.shape[0]} filas x {df.shape[1]} columnas\n")
    df.info()
    print("\nEstadísticas numéricas:")
    print(df.describe().round(2))
    for col in ["programa", "jornada", "genero", "estado"]:
        print(f"\nValores de {col}:")
        print(df[col].value_counts(dropna=False))


def auditar(df):
    titulo("PASO 2. AUDITORÍA DE CALIDAD")

    nulos = df.isnull().sum()
    print("Nulos por columna:")
    print(nulos[nulos > 0])

    asistencia = df["asistencia_pct"].astype(str)
    horas = df["horas_trabajo_semana"].astype(str)
    fecha = df["fecha_matricula"].astype(str)
    edad = pd.to_numeric(df["edad"], errors="coerce")
    promedio = pd.to_numeric(df["promedio_acumulado"], errors="coerce")
    horas_num = pd.to_numeric(horas, errors="coerce")

    AUDITORIA.update({
        "filas_originales": int(df.shape[0]),
        "columnas": int(df.shape[1]),
        "asistencia_guion": int((asistencia == "-").sum()),
        "asistencia_con_pct": int(asistencia.str.contains("%").sum()),
        "horas_guion": int((horas == "-").sum()),
        "distancia_999": int((df["distancia_km"] == 999).sum()),
        "edad_imposible": int(((edad < EDAD_MIN) | (edad > EDAD_MAX)).sum()),
        "promedio_fuera_escala": int(((promedio < PROMEDIO_MIN) | (promedio > PROMEDIO_MAX)).sum()),
        "horas_imposibles": int((horas_num > HORAS_MAX).sum()),
        "no_trabaja_con_guion": int(((df["trabaja"] == "no") & (horas == "-")).sum()),
        "duplicados": int(df.duplicated().sum()),
        "ids_repetidos": int(df["id_estudiante"].duplicated().sum()),
        "fecha_iso": int(fecha.str.match(r"^\d{4}-\d{2}-\d{2}$").sum()),
        "fecha_dmy": int(fecha.str.match(r"^\d{2}/\d{2}/\d{4}$").sum()),
        "nulos_promedio": int(nulos["promedio_acumulado"]),
        "nulos_ciudad": int(nulos["ciudad_procedencia"]),
        "nulos_colegio": int(nulos["tipo_colegio"]),
        "nulos_motivo": int(nulos["motivo_retiro"]),
    })

    for col, validos in VALIDOS.items():
        malos = df[col].dropna()
        malos = malos[~malos.isin(validos)]
        AUDITORIA[f"variantes_{col}"] = int(len(malos))
        print(f"\n{col}: {len(malos)} filas mal escritas")
        print(malos.value_counts())

    print("\nFaltantes disfrazados:")
    print(f"  asistencia_pct con '-': {AUDITORIA['asistencia_guion']}")
    print(f"  asistencia_pct con %: {AUDITORIA['asistencia_con_pct']}")
    print(f"  horas_trabajo_semana con '-': {AUDITORIA['horas_guion']} "
          f"({AUDITORIA['no_trabaja_con_guion']} no trabajan)")
    print(f"  distancia_km con 999: {AUDITORIA['distancia_999']}")
    print("\nValores imposibles:")
    print(f"  edad fuera de {EDAD_MIN}-{EDAD_MAX}: {AUDITORIA['edad_imposible']} -> "
          f"{sorted(edad[(edad < EDAD_MIN) | (edad > EDAD_MAX)].unique().tolist())}")
    print(f"  promedio fuera de 0-5: {AUDITORIA['promedio_fuera_escala']} -> "
          f"{sorted(promedio[promedio > PROMEDIO_MAX].unique().tolist())}")
    print(f"  horas de trabajo > {HORAS_MAX}: {AUDITORIA['horas_imposibles']}")
    print(f"\nDuplicados: {AUDITORIA['duplicados']}")
    print(f"id_estudiante repetidos: {AUDITORIA['ids_repetidos']}")
    print(f"\nFechas AAAA-MM-DD: {AUDITORIA['fecha_iso']} | DD/MM/AAAA: {AUDITORIA['fecha_dmy']}")


def convertir_numericos(df):
    titulo("PASO 3. CONVERSIÓN A NÚMERO")

    asistencia = df["asistencia_pct"].astype(str)
    con_pct = asistencia.str.contains("%").sum()
    guiones = (asistencia == "-").sum()
    asistencia = asistencia.str.replace("%", "", regex=False).replace("-", np.nan)
    df["asistencia_pct"] = pd.to_numeric(asistencia, errors="coerce")
    registrar(3, "asistencia_pct", "Quitar % y convertir a número", con_pct,
              "Con el % la columna se lee como texto; el valor no cambia.")
    registrar(3, "asistencia_pct", "'-' a nulo", guiones,
              "El guion es un dato faltante, no un 0%.")

    horas = df["horas_trabajo_semana"].astype(str)
    guiones_h = (horas == "-").sum()
    df["horas_trabajo_semana"] = pd.to_numeric(horas.replace("-", np.nan), errors="coerce")
    registrar(3, "horas_trabajo_semana", "'-' a nulo y convertir a número", guiones_h,
              "Se deja nulo por ahora; en el paso 8 se revisa si el estudiante trabaja.")

    df["distancia_km"] = pd.to_numeric(df["distancia_km"], errors="coerce")
    n999 = (df["distancia_km"] == 999).sum()
    df["distancia_km"] = df["distancia_km"].replace(999, np.nan)
    registrar(3, "distancia_km", "999 a nulo", n999,
              "999 significa sin dato y subiría la distancia promedio.")

    print(df[["asistencia_pct", "horas_trabajo_semana", "distancia_km"]].describe().round(2))
    return df


def unificar_categorias(df):
    titulo("PASO 4. UNIFICACIÓN DE CATEGORÍAS")

    extras = {
        "programa": {"ingenieria de sistemas": "Ingeniería de Sistemas", "psicologia": "Psicología"},
        "jornada": {},
        "genero": {"m": "Masculino", "f": "Femenino"},
        "ciudad_procedencia": {"bogota": "Bogotá", "medellin": "Medellín"},
    }
    for col, validos in VALIDOS.items():
        mapa = {v.lower(): v for v in validos}
        mapa.update(extras[col])
        antes = df[col].copy()
        df[col] = df[col].str.strip().str.lower().replace(mapa)
        cambiadas = (antes.notna() & (antes != df[col])).sum()
        registrar(4, col, "strip, minúscula y mapear al valor correcto", cambiadas,
                  "Era el mismo valor escrito distinto (tildes, mayúsculas, espacios, "
                  "abreviaturas); sin unificar, un grupo se parte en varios.")
        print(f"{col}: {cambiadas} filas corregidas")
        print(df[col].value_counts(dropna=False), "\n")
    return df


def convertir_fechas(df):
    titulo("PASO 5. FECHAS")
    iso = pd.to_datetime(df["fecha_matricula"], format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(df["fecha_matricula"], format="%d/%m/%Y", errors="coerce")
    otro_formato = (iso.isna() & dmy.notna()).sum()
    df["fecha_matricula"] = iso.fillna(dmy)
    registrar(5, "fecha_matricula", "Convertir a fecha (AAAA-MM-DD y DD/MM/AAAA)", otro_formato,
              "Había dos formatos. Se indica cada uno para no confundir día y mes.")
    print(f"Fechas DD/MM/AAAA: {otro_formato}")
    print(f"Sin convertir: {df['fecha_matricula'].isna().sum()}")
    print(f"Rango: {df['fecha_matricula'].min().date()} a {df['fecha_matricula'].max().date()}")
    return df


def eliminar_duplicados(df):
    titulo("PASO 6. DUPLICADOS")
    n = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    registrar(6, "todas", "Eliminar filas duplicadas", n,
              "Mismo id_estudiante y mismos datos: es el mismo estudiante dos veces.")
    print(f"Duplicados eliminados: {n}. Quedan {df.shape[0]} filas")
    print(f"id repetidos: {df['id_estudiante'].duplicated().sum()}")
    return df


def tratar_faltantes(df):
    titulo("PASO 7. FALTANTES")

    registrar(7, "promedio_acumulado", "Dejar nulo", df["promedio_acumulado"].isna().sum(),
              "No se inventa una nota; mean() ignora los nulos.")

    for col in ["ciudad_procedencia", "tipo_colegio"]:
        n = df[col].isna().sum()
        df[col] = df[col].fillna("Sin dato")
        registrar(7, col, "Nulo a 'Sin dato'", n,
                  "No se puede deducir y borrar la fila haría perder el resto de datos.")

    registrar(7, "asistencia_pct", "Dejar nulo", df["asistencia_pct"].isna().sum(),
              "Inventarla cambiaría el cuartil del estudiante; quedan fuera de la pregunta 5.")
    registrar(7, "distancia_km", "Dejar nulo (incluye los 999)", df["distancia_km"].isna().sum(),
              "No se usa en las preguntas y no hay cómo deducirla.")

    no_desertor = df["estado"] != "desertor"
    n_motivo = (no_desertor & df["motivo_retiro"].isna()).sum()
    sin_motivo = (~no_desertor & df["motivo_retiro"].isna()).sum()
    df.loc[no_desertor, "motivo_retiro"] = df.loc[no_desertor, "motivo_retiro"].fillna("No aplica")
    registrar(7, "motivo_retiro", "'No aplica' para activos y graduados", n_motivo,
              f"Solo aplica a quien se retiró. Desertores sin motivo: {sin_motivo}.")

    nulos = df.isnull().sum()
    print(nulos[nulos > 0])
    return df


def tratar_imposibles(df):
    titulo("PASO 8. VALORES IMPOSIBLES")

    fuera = (df["promedio_acumulado"] < PROMEDIO_MIN) | (df["promedio_acumulado"] > PROMEDIO_MAX)
    print(f"Promedios fuera de escala: {sorted(df.loc[fuera, 'promedio_acumulado'].unique().tolist())}")
    df.loc[fuera, "promedio_acumulado"] = np.nan
    registrar(8, "promedio_acumulado", "Mayores que 5 a nulo", fuera.sum(),
              "45, 62 y 78 no se pueden corregir con seguridad (62/10 sigue fuera de escala).")

    edad_mala = (df["edad"] < EDAD_MIN) | (df["edad"] > EDAD_MAX)
    mediana = df.loc[~edad_mala, "edad"].median()
    print(f"Edades imposibles: {sorted(df.loc[edad_mala, 'edad'].unique().tolist())} -> {mediana}")
    df.loc[edad_mala, "edad"] = mediana
    df["edad"] = df["edad"].astype(int)
    registrar(8, "edad", f"Fuera de {EDAD_MIN}-{EDAD_MAX} a la mediana ({mediana:.0f})", edad_mala.sum(),
              "12 y 150 años son errores. La mediana no se mueve por los extremos.")

    no_trabaja = df["trabaja"] == "no"
    a_cero = (no_trabaja & (df["horas_trabajo_semana"] != 0)).sum()
    df.loc[no_trabaja, "horas_trabajo_semana"] = 0
    registrar(8, "horas_trabajo_semana", "Horas = 0 si no trabaja", a_cero,
              "Si no trabaja, sus horas son 0.")

    imposibles = df["horas_trabajo_semana"] > HORAS_MAX
    df.loc[imposibles, "horas_trabajo_semana"] = np.nan
    mediana_horas = df.loc[df["trabaja"] == "sí", "horas_trabajo_semana"].median()
    df.loc[imposibles, "horas_trabajo_semana"] = mediana_horas
    registrar(8, "horas_trabajo_semana",
              f"Más de {HORAS_MAX} h a la mediana de quienes trabajan ({mediana_horas:.0f})",
              imposibles.sum(),
              "200 h/semana no es posible (la semana tiene 168) y poner 0 sería falso.")

    print(df[["edad", "promedio_acumulado", "horas_trabajo_semana"]].describe().round(2))
    return df


def crear_variables(df):
    titulo("PASO 9. VARIABLES NUEVAS")
    df["desertor"] = df["estado"] == "desertor"
    df["cuartil_asistencia"] = pd.qcut(df["asistencia_pct"], q=4,
                                       labels=["Q1 (más baja)", "Q2", "Q3", "Q4 (más alta)"])
    registrar(9, "desertor", "estado == 'desertor'", df.shape[0],
              "Su promedio es la tasa de deserción.")
    registrar(9, "cuartil_asistencia", "Cuartiles de asistencia con qcut",
              df["cuartil_asistencia"].notna().sum(),
              "Cuatro grupos de tamaño parecido para comparar tasas.")
    print(df["desertor"].value_counts())
    print(df.groupby("cuartil_asistencia", observed=True)["asistencia_pct"].agg(["min", "max", "size"]))
    return df


def guardar_grafico(nombre):
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(GRAFICOS / nombre, dpi=120)
    plt.show()
    plt.close()


def grafico_faltantes(df):
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="viridis")
    plt.title("Mapa de faltantes del dataset original (amarillo = nulo)")
    plt.xlabel("Columna")
    plt.ylabel(f"Filas ({df.shape[0]})")
    guardar_grafico("mapa_faltantes.png")


def grafico_distribuciones(antes, despues):
    fig, ejes = plt.subplots(2, 2, figsize=(12, 8))
    for i, (col, nombre) in enumerate([("promedio_acumulado", "Promedio acumulado"), ("edad", "Edad")]):
        sns.boxplot(x=pd.to_numeric(antes[col], errors="coerce"), ax=ejes[i, 0], color="#e07a5f")
        ejes[i, 0].set_title(f"{nombre}: antes")
        sns.boxplot(x=despues[col], ax=ejes[i, 1], color="#3d85c6")
        ejes[i, 1].set_title(f"{nombre}: después")
    fig.suptitle("Distribuciones antes y después de la limpieza")
    guardar_grafico("distribuciones_antes_despues.png")


def grafico_tasa_programa(df):
    tasa = df.groupby("programa")["desertor"].mean().sort_values() * 100
    plt.figure(figsize=(10, 6))
    barras = plt.barh(tasa.index, tasa.values, color="#3d85c6")
    plt.bar_label(barras, fmt="%.1f%%", padding=3)
    plt.axvline(df["desertor"].mean() * 100, color="gray", ls="--", label="Promedio general")
    plt.xlabel("Tasa de deserción (%)")
    plt.title("Tasa de deserción por programa")
    plt.legend(loc="lower right")
    plt.xlim(0, tasa.max() * 1.15)
    guardar_grafico("tasa_desercion_por_programa.png")


def grafico_tasa_asistencia(df):
    tasa = df.groupby("cuartil_asistencia", observed=True)["desertor"].mean() * 100
    plt.figure(figsize=(9, 6))
    barras = plt.bar(tasa.index.astype(str), tasa.values, color="#3d85c6")
    plt.bar_label(barras, fmt="%.1f%%", padding=3)
    plt.ylabel("Tasa de deserción (%)")
    plt.xlabel("Cuartil de asistencia")
    plt.title("Tasa de deserción por cuartil de asistencia")
    plt.ylim(0, tasa.max() * 1.15)
    guardar_grafico("tasa_desercion_por_asistencia.png")


def a_registros(tabla):
    t = tabla.reset_index().rename(columns={tabla.index.name: "grupo"})
    t["grupo"] = t["grupo"].astype(str)
    return json.loads(t.to_json(orient="records", force_ascii=False))


def responder_preguntas(df):
    titulo("PASO 10. RESPUESTAS")

    p1 = (df.groupby("programa")
            .agg(tasa_desercion=("desertor", "mean"), estudiantes=("desertor", "size"),
                 desertores=("desertor", "sum"))
            .sort_values("tasa_desercion", ascending=False))
    print("\nP1. Deserción por programa:")
    print(p1.assign(tasa_desercion=(p1["tasa_desercion"] * 100).round(1)))
    print(f"-> Mayor: {p1.index[0]} ({p1['tasa_desercion'].iloc[0]:.1%}, "
          f"{p1['estudiantes'].iloc[0]} estudiantes)")

    p2 = df.groupby("beca").agg(tasa_desercion=("desertor", "mean"), estudiantes=("desertor", "size"),
                                desertores=("desertor", "sum"))
    print("\nP2. Deserción por beca:")
    print(p2.assign(tasa_desercion=(p2["tasa_desercion"] * 100).round(1)))
    dif = (p2.loc["no", "tasa_desercion"] - p2.loc["sí", "tasa_desercion"]) * 100
    print(f"-> Diferencia: {dif:.1f} puntos")

    p3 = (df.groupby("jornada")
            .agg(promedio=("promedio_acumulado", "mean"),
                 estudiantes_con_dato=("promedio_acumulado", "count"),
                 estudiantes=("promedio_acumulado", "size"))
            .sort_values("promedio"))
    print("\nP3. Promedio por jornada:")
    print(p3.round(3))
    print(f"-> Menor: {p3.index[0]} ({p3['promedio'].iloc[0]:.2f})")

    p4 = (df[df["estado"] != "graduado"].groupby("estado")
            .agg(materias_reprobadas=("materias_reprobadas", "mean"),
                 estudiantes=("materias_reprobadas", "size")))
    print("\nP4. Materias reprobadas (sin graduados):")
    print(p4.round(2))

    p5 = df.groupby("cuartil_asistencia", observed=True).agg(
        asistencia_min=("asistencia_pct", "min"), asistencia_max=("asistencia_pct", "max"),
        asistencia_promedio=("asistencia_pct", "mean"),
        tasa_desercion=("desertor", "mean"), estudiantes=("desertor", "size"))
    print("\nP5. Deserción por cuartil de asistencia:")
    print(p5.assign(tasa_desercion=(p5["tasa_desercion"] * 100)).round(1))
    sin_asistencia = df["cuartil_asistencia"].isna().sum()
    print(f"Sin dato de asistencia: {sin_asistencia}")

    RESPUESTAS.update({
        "p1": a_registros(p1), "p2": a_registros(p2), "p3": a_registros(p3),
        "p4": a_registros(p4), "p5": a_registros(p5),
        "sin_asistencia": int(sin_asistencia),
        "tasa_general": float(df["desertor"].mean()),
        "estado": {k: int(v) for k, v in df["estado"].value_counts().items()},
    })


def guardar(df):
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "dataset_limpio.csv", index=False)
    pd.DataFrame(DECISIONES).to_csv(PROCESSED / "decisiones.csv", index=False)
    print(f"\nDataset limpio: {df.shape[0]} filas, {df.shape[1]} columnas.")


def exportar_web(df):
    WEB.mkdir(exist_ok=True)
    datos = {
        "auditoria": AUDITORIA,
        "decisiones": DECISIONES,
        "respuestas": RESPUESTAS,
        "filas_limpias": int(df.shape[0]),
        "columnas_limpias": int(df.shape[1]),
    }
    texto = json.dumps(datos, ensure_ascii=False, indent=2, default=lambda o: o.item())
    (WEB / "datos.js").write_text(f"window.RESULTADOS = {texto};\n", encoding="utf-8")
    print(f"Datos para la web en {WEB / 'datos.js'}")


def main():
    original = pd.read_csv(RAW)
    df = original.copy()

    explorar(df)
    auditar(df)
    grafico_faltantes(df)

    df = convertir_numericos(df)
    df = unificar_categorias(df)
    df = convertir_fechas(df)
    df = eliminar_duplicados(df)
    df = tratar_faltantes(df)
    df = tratar_imposibles(df)
    df = crear_variables(df)

    grafico_distribuciones(original, df)
    grafico_tasa_programa(df)
    grafico_tasa_asistencia(df)

    responder_preguntas(df)
    print("\nDecisiones:")
    print(pd.DataFrame(DECISIONES))
    guardar(df)
    exportar_web(df)


if __name__ == "__main__":
    main()
