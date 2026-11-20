window.RESULTADOS = {
  "auditoria": {
    "filas_originales": 10150,
    "columnas": 23,
    "asistencia_guion": 202,
    "asistencia_con_pct": 300,
    "horas_guion": 2822,
    "distancia_999": 152,
    "edad_imposible": 12,
    "promedio_fuera_escala": 17,
    "horas_imposibles": 30,
    "no_trabaja_con_guion": 2822,
    "duplicados": 150,
    "ids_repetidos": 150,
    "fecha_iso": 7098,
    "fecha_dmy": 3052,
    "nulos_promedio": 304,
    "nulos_ciudad": 103,
    "nulos_colegio": 152,
    "nulos_motivo": 6877,
    "variantes_programa": 260,
    "variantes_jornada": 485,
    "variantes_genero": 559,
    "variantes_ciudad_procedencia": 542
  },
  "decisiones": [
    {
      "paso": 3,
      "columna": "asistencia_pct",
      "accion": "Quitar % y convertir a número",
      "filas_afectadas": 300,
      "justificacion": "Con el % la columna se lee como texto; el valor no cambia."
    },
    {
      "paso": 3,
      "columna": "asistencia_pct",
      "accion": "'-' a nulo",
      "filas_afectadas": 202,
      "justificacion": "El guion es un dato faltante, no un 0%."
    },
    {
      "paso": 3,
      "columna": "horas_trabajo_semana",
      "accion": "'-' a nulo y convertir a número",
      "filas_afectadas": 2822,
      "justificacion": "Se deja nulo por ahora; en el paso 8 se revisa si el estudiante trabaja."
    },
    {
      "paso": 3,
      "columna": "distancia_km",
      "accion": "999 a nulo",
      "filas_afectadas": 152,
      "justificacion": "999 significa sin dato y subiría la distancia promedio."
    },
    {
      "paso": 4,
      "columna": "programa",
      "accion": "strip, minúscula y mapear al valor correcto",
      "filas_afectadas": 260,
      "justificacion": "Era el mismo valor escrito distinto (tildes, mayúsculas, espacios, abreviaturas); sin unificar, un grupo se parte en varios."
    },
    {
      "paso": 4,
      "columna": "jornada",
      "accion": "strip, minúscula y mapear al valor correcto",
      "filas_afectadas": 485,
      "justificacion": "Era el mismo valor escrito distinto (tildes, mayúsculas, espacios, abreviaturas); sin unificar, un grupo se parte en varios."
    },
    {
      "paso": 4,
      "columna": "genero",
      "accion": "strip, minúscula y mapear al valor correcto",
      "filas_afectadas": 559,
      "justificacion": "Era el mismo valor escrito distinto (tildes, mayúsculas, espacios, abreviaturas); sin unificar, un grupo se parte en varios."
    },
    {
      "paso": 4,
      "columna": "ciudad_procedencia",
      "accion": "strip, minúscula y mapear al valor correcto",
      "filas_afectadas": 542,
      "justificacion": "Era el mismo valor escrito distinto (tildes, mayúsculas, espacios, abreviaturas); sin unificar, un grupo se parte en varios."
    },
    {
      "paso": 5,
      "columna": "fecha_matricula",
      "accion": "Convertir a fecha (AAAA-MM-DD y DD/MM/AAAA)",
      "filas_afectadas": 3052,
      "justificacion": "Había dos formatos. Se indica cada uno para no confundir día y mes."
    },
    {
      "paso": 6,
      "columna": "todas",
      "accion": "Eliminar filas duplicadas",
      "filas_afectadas": 150,
      "justificacion": "Mismo id_estudiante y mismos datos: es el mismo estudiante dos veces."
    },
    {
      "paso": 7,
      "columna": "promedio_acumulado",
      "accion": "Dejar nulo",
      "filas_afectadas": 298,
      "justificacion": "No se inventa una nota; mean() ignora los nulos."
    },
    {
      "paso": 7,
      "columna": "ciudad_procedencia",
      "accion": "Nulo a 'Sin dato'",
      "filas_afectadas": 100,
      "justificacion": "No se puede deducir y borrar la fila haría perder el resto de datos."
    },
    {
      "paso": 7,
      "columna": "tipo_colegio",
      "accion": "Nulo a 'Sin dato'",
      "filas_afectadas": 150,
      "justificacion": "No se puede deducir y borrar la fila haría perder el resto de datos."
    },
    {
      "paso": 7,
      "columna": "asistencia_pct",
      "accion": "Dejar nulo",
      "filas_afectadas": 200,
      "justificacion": "Inventarla cambiaría el cuartil del estudiante; quedan fuera de la pregunta 5."
    },
    {
      "paso": 7,
      "columna": "distancia_km",
      "accion": "Dejar nulo (incluye los 999)",
      "filas_afectadas": 347,
      "justificacion": "No se usa en las preguntas y no hay cómo deducirla."
    },
    {
      "paso": 7,
      "columna": "motivo_retiro",
      "accion": "'No aplica' para activos y graduados",
      "filas_afectadas": 6764,
      "justificacion": "Solo aplica a quien se retiró. Desertores sin motivo: 0."
    },
    {
      "paso": 8,
      "columna": "promedio_acumulado",
      "accion": "Mayores que 5 a nulo",
      "filas_afectadas": 15,
      "justificacion": "45, 62 y 78 no se pueden corregir con seguridad (62/10 sigue fuera de escala)."
    },
    {
      "paso": 8,
      "columna": "edad",
      "accion": "Fuera de 15-60 a la mediana (22)",
      "filas_afectadas": 12,
      "justificacion": "12 y 150 años son errores. La mediana no se mueve por los extremos."
    },
    {
      "paso": 8,
      "columna": "horas_trabajo_semana",
      "accion": "Horas = 0 si no trabaja",
      "filas_afectadas": 2781,
      "justificacion": "Si no trabaja, sus horas son 0."
    },
    {
      "paso": 8,
      "columna": "horas_trabajo_semana",
      "accion": "Más de 100 h a la mediana de quienes trabajan (24)",
      "filas_afectadas": 30,
      "justificacion": "200 h/semana no es posible (la semana tiene 168) y poner 0 sería falso."
    },
    {
      "paso": 9,
      "columna": "desertor",
      "accion": "estado == 'desertor'",
      "filas_afectadas": 10000,
      "justificacion": "Su promedio es la tasa de deserción."
    },
    {
      "paso": 9,
      "columna": "cuartil_asistencia",
      "accion": "Cuartiles de asistencia con qcut",
      "filas_afectadas": 9800,
      "justificacion": "Cuatro grupos de tamaño parecido para comparar tasas."
    }
  ],
  "respuestas": {
    "p1": [
      {
        "grupo": "Ingeniería Industrial",
        "tasa_desercion": 0.4016641452,
        "estudiantes": 1322,
        "desertores": 531
      },
      {
        "grupo": "Ingeniería de Sistemas",
        "tasa_desercion": 0.3826815642,
        "estudiantes": 1432,
        "desertores": 548
      },
      {
        "grupo": "Diseño Gráfico",
        "tasa_desercion": 0.3574712644,
        "estudiantes": 870,
        "desertores": 311
      },
      {
        "grupo": "Enfermería",
        "tasa_desercion": 0.3127677806,
        "estudiantes": 1167,
        "desertores": 365
      },
      {
        "grupo": "Derecho",
        "tasa_desercion": 0.3064623584,
        "estudiantes": 1501,
        "desertores": 460
      },
      {
        "grupo": "Administración de Empresas",
        "tasa_desercion": 0.2941176471,
        "estudiantes": 1343,
        "desertores": 395
      },
      {
        "grupo": "Contaduría Pública",
        "tasa_desercion": 0.2683946488,
        "estudiantes": 1196,
        "desertores": 321
      },
      {
        "grupo": "Psicología",
        "tasa_desercion": 0.2609067579,
        "estudiantes": 1169,
        "desertores": 305
      }
    ],
    "p2": [
      {
        "grupo": "no",
        "tasa_desercion": 0.3632472732,
        "estudiantes": 7243,
        "desertores": 2631
      },
      {
        "grupo": "sí",
        "tasa_desercion": 0.2194414218,
        "estudiantes": 2757,
        "desertores": 605
      }
    ],
    "p3": [
      {
        "grupo": "Nocturna",
        "promedio": 3.4644448612,
        "estudiantes_con_dato": 2666,
        "estudiantes": 2754
      },
      {
        "grupo": "Fin de semana",
        "promedio": 3.7044573235,
        "estudiantes_con_dato": 949,
        "estudiantes": 984
      },
      {
        "grupo": "Diurna",
        "promedio": 3.7249440053,
        "estudiantes_con_dato": 6072,
        "estudiantes": 6262
      }
    ],
    "p4": [
      {
        "grupo": "activo",
        "materias_reprobadas": 0.6218101395,
        "estudiantes": 5878
      },
      {
        "grupo": "desertor",
        "materias_reprobadas": 3.066131026,
        "estudiantes": 3236
      }
    ],
    "p5": [
      {
        "grupo": "Q1 (más baja)",
        "asistencia_min": 48.0,
        "asistencia_max": 80.5,
        "asistencia_promedio": 73.8915309446,
        "tasa_desercion": 0.6180781759,
        "estudiantes": 2456
      },
      {
        "grupo": "Q2",
        "asistencia_min": 80.6,
        "asistencia_max": 87.8,
        "asistencia_promedio": 84.3851175994,
        "tasa_desercion": 0.3698296837,
        "estudiantes": 2466
      },
      {
        "grupo": "Q3",
        "asistencia_min": 87.9,
        "asistencia_max": 95.0,
        "asistencia_promedio": 91.3246400658,
        "tasa_desercion": 0.2069107363,
        "estudiantes": 2431
      },
      {
        "grupo": "Q4 (más alta)",
        "asistencia_min": 95.1,
        "asistencia_max": 100.0,
        "asistencia_promedio": 98.6654270535,
        "tasa_desercion": 0.092766653,
        "estudiantes": 2447
      }
    ],
    "sin_asistencia": 200,
    "tasa_general": 0.3236,
    "estado": {
      "activo": 5878,
      "desertor": 3236,
      "graduado": 886
    }
  },
  "filas_limpias": 10000,
  "columnas_limpias": 25
};
