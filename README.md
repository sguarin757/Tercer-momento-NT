# Taller práctico proyecto integrador: calidad de datos para la retención estudiantil

Una institución de educación superior quiere entender qué factores están asociados a la deserción, para diseñar estrategias de retención tempranas. Antes de responder preguntas de análisis, el equipo de datos debe garantizar que la información sea confiable. Este taller trabaja justo ese paso: auditar, limpiar y documentar los datos, y después responder cinco preguntas con esos datos limpios.

Los datos son sintéticos. Fueron generados para el taller y no corresponden a estudiantes reales.

## Requisitos

- Python 3.10 o superior
- Git
- Lo visto en los talleres de Pandas y de limpieza de datos

## Cómo empezar

1. Clona el repositorio y entra a la carpeta del proyecto:

   ```
   git clone <URL-DEL-REPOSITORIO>
   cd <NOMBRE-DE-LA-CARPETA>
   ```

2. Crea y activa un ambiente virtual. Las instrucciones para Windows y Mac/Linux están en `LEEME_ambiente.txt`.

3. Instala las librerías:

   ```
   pip install -r requirements.txt
   ```

4. Ejecuta el script:

   ```
   python analisis_desercion.py
   ```

Ejecuta el comando desde la carpeta del proyecto.

## Estructura del proyecto

```
proyecto/
├── analisis_desercion.py   Script principal. Tiene un TODO por cada paso.
├── requirements.txt        Versiones de las librerías.
├── LEEME_ambiente.txt      Pasos para crear el ambiente virtual.
├── README.md               Este archivo.
├── .gitignore              Archivos que Git no debe subir.
└── Data/
    ├── raw/
    │   └── datos_estudiantes.csv   Dataset original. No lo modifiques.
    └── processed/
        ├── .gitkeep                Mantiene la carpeta en el repositorio.
        ├── dataset_limpio.csv      Lo genera el script. No se sube (está en .gitignore).
        ├── decisiones.csv          Lo genera el script. Sí se sube.
        └── graficos/               Lo genera el script. Sí se sube.
```

Lo que genera el script (`dataset_limpio.csv`, `decisiones.csv` y `graficos/`) aparece en `Data/processed/` al ejecutarlo. Los dos últimos se suben al repositorio, porque son parte de la entrega.

## Qué debes hacer

Completa los TODO de `analisis_desercion.py` en orden. Cada función tiene un docstring con preguntas: respóndelas antes de escribir el código. Cada decisión que tomes debe quedar registrada con `registrar()`.

Cuando termines, el script debe producir:

- `Data/processed/dataset_limpio.csv`: el dataset limpio.
- `Data/processed/decisiones.csv`: la tabla de decisiones.
- `Data/processed/graficos/`: los cuatro gráficos.

La guía del taller (`Taller_Retencion_Estudiantil.docx`) explica cada método antes de usarlo, con ejemplos y errores frecuentes.

## Entrega

Sube tu código completo al repositorio y envía el enlace por el formulario de entrega. La entrega es individual.

El repositorio debe incluir:

- `analisis_desercion.py` con todos los TODO completados.
- `Data/processed/decisiones.csv` y la carpeta `Data/processed/graficos/`.
- Un `README.md` al final de este archivo, con una sección titulada **Mis decisiones y respuestas**. Debe incluir:
  0. El diccionario de datos: la tabla de las 23 columnas con tipo, descripción y rol, completada según el paso 1 de la guía.
  1. Tu diagnóstico de calidad: qué problemas encontraste y en qué columnas.
  2. Tus decisiones de limpieza, con su justificación.
  3. Las respuestas a las cinco preguntas, cada una con el número de estudiantes por grupo.
  4. Tu respuesta a la reflexión sobre asociación y causalidad.
  5. Tu respuesta a la reflexión sobre `motivo_retiro` y la predicción.
  6. Tu respuesta a la reflexión sobre el uso de variables sensibles.

El script debe ejecutarse sin errores desde cero. Cada decisión necesita una justificación, y cada conclusión debe apoyarse en un número del análisis.

---

# Mis decisiones y respuestas

## Cómo ejecutar el proyecto y ver los resultados

1. Crear y activar el ambiente virtual (Windows, PowerShell), desde la carpeta del proyecto:

   ```
   python -m venv venv
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   En Mac/Linux: `python3 -m venv venv` y `source venv/bin/activate`.

2. Ejecutar el análisis:

   ```
   python analisis_desercion.py
   ```

   El script imprime cada paso en la terminal y abre los cuatro gráficos uno por uno (cierra cada ventana para continuar). Al terminar genera:

   | Archivo | Contenido |
   |---|---|
   | `Data/processed/dataset_limpio.csv` | Dataset limpio (10.000 filas, 25 columnas). No se sube al repositorio. |
   | `Data/processed/decisiones.csv` | Tabla con las 22 decisiones de limpieza. |
   | `Data/processed/graficos/*.png` | Los cuatro gráficos. |
   | `web/datos.js` | Resultados en formato JSON para la página web. |

3. Ver los resultados en el navegador: abrir **`web/index.html`** con doble clic (o clic derecho → *Abrir con* → navegador). No necesita servidor ni internet. La página muestra:
   - Indicadores generales (filas antes y después, decisiones, tasa de deserción).
   - El diagnóstico de calidad con el conteo de cada problema.
   - La tabla de decisiones con un buscador.
   - Los cuatro gráficos (clic para ampliar).
   - Las cinco preguntas con barras y el número de estudiantes por grupo.
   - Las tres reflexiones.

   Si la página muestra el aviso "No se encontró web/datos.js", ejecuta primero el paso 2.

Estructura de la visualización (HTML independiente):

```
web/
├── index.html   Estructura de la página
├── estilos.css  Estilos (modo claro y oscuro, adaptable a celular)
├── app.js       Lee window.RESULTADOS y dibuja tarjetas, tabla y barras
└── datos.js     Lo genera analisis_desercion.py
```

## 0. Diccionario de datos

| Columna | Tipo | Descripción | Rol |
|---|---|---|---|
| id_estudiante | texto | Código único del estudiante (EST00001) | identificación |
| programa | categórica | Programa académico que cursa (8 programas) | explicativa |
| facultad | categórica | Facultad a la que pertenece el programa | explicativa |
| jornada | categórica | Diurna, Nocturna o Fin de semana | explicativa |
| semestre | numérica | Semestre que cursa (1 a 10) | explicativa |
| promedio_acumulado | numérica | Promedio de notas en escala de 0 a 5. Llega con valores en otra escala (45, 62, 78) | explicativa |
| creditos_aprobados | numérica | Créditos aprobados hasta la fecha | explicativa |
| materias_reprobadas | numérica | Número de materias perdidas | explicativa |
| asistencia_pct | numérica | Porcentaje de asistencia a clases. Llega como texto por el símbolo % y los guiones | explicativa |
| sesiones_tutoria | numérica | Número de tutorías académicas a las que asistió | explicativa |
| cambios_programa | numérica | Veces que se cambió de programa | explicativa |
| estrato | categórica (ordinal) | Estrato socioeconómico de la vivienda (1 a 6). Variable sensible | explicativa |
| beca | categórica | Si recibe beca (sí / no) | explicativa |
| trabaja | categórica | Si trabaja además de estudiar (sí / no) | explicativa |
| horas_trabajo_semana | numérica | Horas de trabajo por semana. Llega como texto por los guiones | explicativa |
| distancia_km | numérica | Distancia de la vivienda a la sede en km. 999 = sin dato | explicativa |
| edad | numérica | Edad en años | explicativa |
| genero | categórica | Femenino o Masculino. Variable sensible | explicativa |
| ciudad_procedencia | categórica | Ciudad de origen del estudiante. Variable sensible | explicativa |
| tipo_colegio | categórica | Colegio de bachillerato Público o Privado | explicativa |
| fecha_matricula | fecha | Fecha de la matrícula. Llega en dos formatos | explicativa |
| estado | categórica | Situación del estudiante: activo, graduado o desertor | resultado |
| motivo_retiro | categórica | Razón del retiro (Económico, Académico, Personal…). Solo existe para desertores y se conoce después del retiro | resultado (no sirve para predecir) |

Columnas creadas en el paso 9: `desertor` (booleana, resultado) y `cuartil_asistencia` (categórica ordinal, explicativa).

## 1. Diagnóstico de calidad

El archivo original tiene **10.150 filas y 23 columnas**. Problemas encontrados:

| Tipo de problema | Columna | Cantidad |
|---|---|---|
| Nulo real | promedio_acumulado | 304 |
| Nulo real | distancia_km | 199 |
| Nulo real | ciudad_procedencia | 103 |
| Nulo real | tipo_colegio | 152 |
| Nulo esperado (no es error) | motivo_retiro | 6.877 (todos los no desertores) |
| Faltante disfrazado `-` | asistencia_pct | 202 |
| Faltante disfrazado `-` | horas_trabajo_semana | 2.822 (todos de estudiantes con `trabaja = no`) |
| Faltante disfrazado `999` | distancia_km | 152 |
| Formato: número con `%` | asistencia_pct | 300 |
| Valor imposible (> 5) | promedio_acumulado | 17 (valores 45, 62 y 78) |
| Valor imposible (fuera de 15-60) | edad | 12 (valores 12 y 150) |
| Valor imposible (> 100 h) | horas_trabajo_semana | 30 (valor 200) |
| Duplicados completos | todas | 150 (mismo id_estudiante) |
| Error tipográfico | programa | 260 (`Ingenieria de Sistemas`, `Psicologia`) |
| Error tipográfico | jornada | 485 (`diurna`, `nocturna`, `NOCTURNA `) |
| Error tipográfico | genero | 559 (`M`, `F`, `femenino`) |
| Error tipográfico | ciudad_procedencia | 542 (`BOGOTÁ`, `Bogota`, `bogota `, `medellin`, `Medellin `) |
| Fechas en dos formatos | fecha_matricula | 7.098 AAAA-MM-DD y 3.052 DD/MM/AAAA |

Por los `%` y los `-`, `asistencia_pct` y `horas_trabajo_semana` aparecen como texto en `info()`: basta un valor no numérico para que Pandas lea toda la columna como texto.

**¿Qué problema afecta más el análisis?** Los errores tipográficos y los duplicados, porque cambian directamente los grupos de las cinco preguntas. Sin unificar, "Psicologia" y "Psicología" serían dos programas, y "M" sería un tercer género. Los duplicados cuentan dos veces a 150 estudiantes. Los promedios de 45 a 78 subirían el promedio de cualquier jornada donde caigan.

**Mapa de faltantes:** los huecos más visibles están en `motivo_retiro` (casi toda la columna, porque solo aplica a desertores), y después en `promedio_acumulado`, `distancia_km`, `tipo_colegio` y `ciudad_procedencia`. Coinciden con el conteo de `isnull()`. Los faltantes disfrazados (`-`, `999`) **no** aparecen en el mapa porque Pandas no los ve como nulos.

## 2. Decisiones de limpieza

La tabla completa está en [`Data/processed/decisiones.csv`](Data/processed/decisiones.csv).

| Paso | Columna | Decisión | Filas | Justificación |
|---|---|---|---|---|
| 3 | asistencia_pct | Quitar `%` y convertir a número | 300 | El valor es el mismo sin el símbolo |
| 3 | asistencia_pct | `-` → nulo | 202 | Es un faltante disfrazado, no un 0 % |
| 3 | horas_trabajo_semana | `-` → nulo y convertir | 2.822 | Se resuelve en el paso 8 según `trabaja` |
| 3 | distancia_km | 999 → nulo | 152 | Es un código de "sin dato" que inflaría la media |
| 4 | programa, jornada, genero, ciudad_procedencia | `strip()`, `lower()` y diccionario al valor válido | 260 / 485 / 559 / 542 | Es el mismo valor escrito distinto. No se unificó "Otra ciudad" con ninguna ciudad ni se rellenaron los nulos en este paso |
| 5 | fecha_matricula | Dos `to_datetime` con formato explícito + `fillna` | 3.052 | Evita confundir día y mes; quedan 0 fechas sin convertir |
| 6 | todas | `drop_duplicates()` + `reset_index(drop=True)` | 150 | Mismo id y mismos datos: es el mismo estudiante dos veces. Quedan 10.000 filas |
| 7 | promedio_acumulado | Dejar nulo | 298 | No se inventa una nota; imputar la media acerca a todos al centro y oculta a los estudiantes en riesgo |
| 7 | ciudad_procedencia / tipo_colegio | Nulo → `"Sin dato"` | 100 / 150 | No se puede deducir; borrar la fila perdería el resto de su información |
| 7 | asistencia_pct | Dejar nulo | 200 | Inventarla movería estudiantes de cuartil; quedan fuera de la pregunta 5 |
| 7 | distancia_km | Dejar nulo | 347 | No se usa en las preguntas |
| 7 | motivo_retiro | `"No aplica"` para activos y graduados | 6.764 | No es un error: solo aplica a desertores (los 3.236 desertores tienen motivo) |
| 8 | promedio_acumulado | > 5 → nulo | 15 | 45 podría ser 4,5, pero 62 y 78 divididos entre 10 siguen fuera de escala; no hay forma segura de recuperarlos |
| 8 | edad | Fuera de 15-60 → mediana (22) | 12 | 12 y 150 son errores de registro; la mediana no se afecta por los extremos |
| 8 | horas_trabajo_semana | `trabaja = no` → 0 | 2.781 | Si no trabaja, sus horas son 0. La regla depende de otra columna |
| 8 | horas_trabajo_semana | > 100 → mediana de quienes trabajan (24) | 30 | 200 h/semana es imposible (una semana tiene 168); poner 0 sería falso porque sí trabajan |
| 9 | desertor | `estado == "desertor"` | 10.000 | Su media es la tasa de deserción |
| 9 | cuartil_asistencia | `pd.qcut(asistencia_pct, 4)` | 9.800 | Cuatro grupos de unos 2.450 estudiantes |

**Boxplots antes y después:** antes, los promedios de 45, 62 y 78 estiran el eje hasta 80 y la caja real (entre 3 y 4) queda aplastada. Lo mismo pasa con la edad de 150. Después, el promedio queda entre 1,17 y 5,0 y la edad entre 17 y 29. Siguen apareciendo puntos sueltos (promedios menores que 1,9 y edades de 28 y 29). Se dejaron porque son valores **posibles**, de estudiantes reales con bajo rendimiento o con más edad que la mayoría, no errores.

**¿Por qué cuartiles y no valores exactos?** Con valores exactos habría cientos de grupos con muy pocos estudiantes, y una tasa de 1 de 2 se vería como 50 %. Los cuartiles crean cuatro grupos de tamaño parecido (de 2.431 a 2.466) y la tendencia se lee con claridad.

## 3. Respuestas a las cinco preguntas

Tasa de deserción general: **32,4 %** (3.236 de 10.000 estudiantes).

### Pregunta 1. ¿Qué programa presenta la tasa de deserción más alta?

**Ingeniería Industrial, con 40,2 %** (531 de 1.322 estudiantes).

| Programa | Tasa | Desertores | Estudiantes |
|---|---|---|---|
| Ingeniería Industrial | 40,2 % | 531 | 1.322 |
| Ingeniería de Sistemas | 38,3 % | 548 | 1.432 |
| Diseño Gráfico | 35,7 % | 311 | 870 |
| Enfermería | 31,3 % | 365 | 1.167 |
| Derecho | 30,6 % | 460 | 1.501 |
| Administración de Empresas | 29,4 % | 395 | 1.343 |
| Contaduría Pública | 26,8 % | 321 | 1.196 |
| Psicología | 26,1 % | 305 | 1.169 |

El programa más pequeño es Diseño Gráfico (870 estudiantes). Es menor que los demás, pero sigue siendo un grupo grande, así que su tasa es confiable. Sin la unificación del paso 4, Ingeniería de Sistemas habría perdido 144 filas y Psicología 116.

### Pregunta 2. ¿Hay diferencia en la deserción entre becados y no becados?

**Sí.** Sin beca: **36,3 %** (2.631 de 7.243). Con beca: **21,9 %** (605 de 2.757). Diferencia: **14,4 puntos porcentuales**.

Esa diferencia no prueba que la beca cause la permanencia (ver la reflexión 1).

### Pregunta 3. ¿Qué jornada tiene el menor promedio acumulado?

**Nocturna, con 3,46.**

| Jornada | Promedio | Estudiantes con promedio | Estudiantes |
|---|---|---|---|
| Nocturna | 3,46 | 2.666 | 2.754 |
| Fin de semana | 3,70 | 949 | 984 |
| Diurna | 3,73 | 6.072 | 6.262 |

Todos los grupos son grandes; Fin de semana es el más pequeño (984).

### Pregunta 4. ¿Cuántas materias reprobadas tienen en promedio los desertores frente a los activos?

| Estado | Materias reprobadas (promedio) | Estudiantes |
|---|---|---|
| Desertor | **3,07** | 3.236 |
| Activo | **0,62** | 5.878 |

Los desertores reprueban en promedio unas **5 veces más** materias que los activos. Se excluyó a los 886 graduados porque la pregunta compara a quienes se fueron con quienes siguen estudiando. Los graduados ya terminaron (llevan más semestres cursados, 8,2 en promedio), y mezclarlos con los activos cambiaría el grupo de comparación.

### Pregunta 5. ¿La deserción aumenta conforme baja la asistencia?

**Sí, de forma clara y constante.**

| Cuartil | Rango de asistencia | Asistencia promedio | Tasa de deserción | Estudiantes |
|---|---|---|---|---|
| Q1 (más baja) | 48,0 - 80,5 % | 73,9 % | **61,8 %** | 2.456 |
| Q2 | 80,6 - 87,8 % | 84,4 % | 37,0 % | 2.466 |
| Q3 | 87,9 - 95,0 % | 91,3 % | 20,7 % | 2.431 |
| Q4 (más alta) | 95,1 - 100 % | 98,7 % | **9,3 %** | 2.447 |

En el cuartil de menor asistencia deserta más de 6 de cada 10 estudiantes; en el de mayor asistencia, menos de 1 de cada 10. Los 200 estudiantes sin dato de asistencia quedan fuera. El patrón no es una prueba de causa: faltar a clase y desertar pueden ser consecuencias de un mismo problema (trabajo, dinero, salud). Tampoco sabemos el orden en el tiempo: es posible que el estudiante deje de asistir porque **ya** decidió retirarse.

## 4. Reflexión 1: asociación y causalidad

No. Los becados desertan menos (21,9 % frente a 36,3 %), pero eso es una **asociación**. Hay otras razones por las que un estudiante puede recibir la beca y también permanecer:

- Las becas suelen darse por mérito. Un estudiante disciplinado o con buen rendimiento tiene más probabilidad de recibirla **y** de terminar. En los datos, los becados tienen un promedio algo mayor (3,71 frente a 3,63) y más asistencia (87,7 % frente a 86,8 %).
- Para conservar la beca hay que mantener un promedio mínimo. Quien no lo logra la pierde y pasa al grupo "sin beca", lo que infla la deserción de ese grupo.
- Factores que no están en el dataset (apoyo familiar, motivación) pueden influir en ambas cosas.

Para distinguir causa de asociación habría que comparar estudiantes **iguales en todo menos en la beca**. Por ejemplo: sortear becas entre aspirantes parecidos, comparar a quienes quedaron justo por encima y justo por debajo del puntaje de corte, o al menos controlar por promedio, estrato y trabajo.

## 5. Reflexión 2: `motivo_retiro` y la predicción

No. `motivo_retiro` solo se llena **después** de que el estudiante deserta, y solo existe para los desertores. Si se usa para predecir, el modelo aprende que "tener motivo = desertor" y acierta casi al 100 % con los datos históricos. Pero con un estudiante activo la columna siempre está vacía y el modelo no sirve. Esto se llama **fuga de información**: se usa información del futuro para predecir.

Otras columnas con el mismo riesgo:

- **`estado`** y **`desertor`**: son el resultado mismo.
- **`creditos_aprobados`** y **`semestre`**: se detienen cuando el estudiante se retira, mientras los activos siguen sumando. Los desertores tienen 19,0 créditos frente a 23,7 de los activos; parte de esa diferencia puede deberse a que dejaron de estudiar.
- **`materias_reprobadas`** y **`asistencia_pct`**, si se midieron al final: un estudiante que ya decidió irse deja de asistir y pierde las materias que abandonó. Solo sirven para predecir si se toman **antes** del retiro (por ejemplo, en la semana 8 del semestre).

## 6. Reflexión 3: uso de variables sensibles

Género, estrato y ciudad de procedencia pueden reflejar desigualdades sociales. En estos datos, las diferencias por estas variables son pequeñas: por estrato van de 30,8 % a 37,5 % (y el estrato 6 tiene solo 419 estudiantes); por género, 31,6 % frente a 33,3 %. Son mucho menores que las diferencias por asistencia o por materias reprobadas.

La institución **no** debería usarlas para decidir quién recibe apoyo, por estos riesgos:

- **Discriminación y estigma:** se trataría a la persona según su grupo y no según su situación. Un estudiante de estrato 1 con 95 % de asistencia quedaría marcado como "en riesgo", y uno de estrato 5 con problemas reales quedaría por fuera.
- **Profecía autocumplida:** si se etiqueta a un grupo como "propenso a desertar", puede recibir menos expectativas o un trato distinto.
- **Reproducir la desigualdad:** si un modelo aprende de datos con sesgos históricos, los repite.
- **Legal:** en Colombia, la Ley 1581 de 2012 protege los datos personales y exige usarlos con una finalidad clara y autorizada.

Un uso responsable es emplearlas para **revisar la equidad** (por ejemplo, comprobar que los apoyos llegan por igual a todos los estratos) y basar las alertas en **conductas que la institución puede ayudar a cambiar**: asistencia, materias reprobadas y tutorías. Por ejemplo, un estudiante del cuartil Q1 de asistencia (61,8 % de deserción) debería recibir acompañamiento sin importar su género o su estrato, y siempre con la revisión de una persona antes de tomar una decisión.
