(function () {
  const R = window.RESULTADOS;
  if (!R) {
    document.getElementById("aviso").hidden = false;
    return;
  }

  const fmt = (n, d = 0) => Number(n).toLocaleString("es-CO", { minimumFractionDigits: d, maximumFractionDigits: d });
  const pct = (x, d = 1) => fmt(x * 100, d) + " %";
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const A = R.auditoria;
  const P = R.respuestas;

  const kpis = [
    [fmt(A.filas_originales), "filas originales"],
    [fmt(R.filas_limpias), "filas limpias"],
    [fmt(R.decisiones.length), "decisiones registradas"],
    [pct(P.tasa_general), "tasa de deserción general"],
  ];
  document.getElementById("kpis").innerHTML = kpis
    .map(([v, e]) => `<div class="kpi"><span class="valor">${v}</span><span class="etiqueta">${e}</span></div>`)
    .join("");

  const problemas = [
    [A.duplicados, "Filas duplicadas", "Mismo id_estudiante y todos los datos iguales"],
    [A.variantes_programa, "programa mal escrito", "Psicologia, Ingenieria de Sistemas (sin tilde)"],
    [A.variantes_jornada, "jornada mal escrita", "diurna, nocturna, “NOCTURNA ” con espacio"],
    [A.variantes_genero, "genero mal escrito", "M, F, femenino"],
    [A.variantes_ciudad_procedencia, "ciudad mal escrita", "BOGOTÁ, Bogota, bogota, medellin…"],
    [A.asistencia_con_pct, "asistencia con %", "Valores como “85%” que vuelven texto la columna"],
    [A.asistencia_guion, "asistencia con “-”", "Faltante disfrazado"],
    [A.horas_guion, "horas de trabajo con “-”", `Todos de estudiantes que no trabajan (${fmt(A.no_trabaja_con_guion)})`],
    [A.horas_imposibles, "horas de trabajo > 100", "200 h/semana: más de las 168 que tiene una semana"],
    [A.distancia_999, "distancia = 999", "Código de “sin dato”"],
    [A.promedio_fuera_escala, "promedio fuera de 0-5", "45, 62 y 78"],
    [A.edad_imposible, "edad imposible", "12 y 150 años"],
    [A.fecha_dmy, "fechas DD/MM/AAAA", `Mezcladas con ${fmt(A.fecha_iso)} en AAAA-MM-DD`],
    [A.nulos_promedio, "promedio nulo", "Nulos reales"],
    [A.nulos_ciudad, "ciudad nula", "Nulos reales"],
    [A.nulos_colegio, "tipo de colegio nulo", "Nulos reales"],
    [A.nulos_motivo, "motivo_retiro nulo", "Esperado: solo aplica a desertores"],
  ];
  document.getElementById("problemas").innerHTML = problemas
    .map(([n, t, d]) => `<div class="problema"><span class="n">${fmt(n)}</span><span class="t">${esc(t)}</span><span class="d">${esc(d)}</span></div>`)
    .join("");

  const tbody = document.querySelector("#tabla-decisiones tbody");
  function pintarDecisiones(filtro) {
    const f = filtro.trim().toLowerCase();
    tbody.innerHTML = R.decisiones
      .filter((d) => !f || [d.columna, d.accion, d.justificacion].join(" ").toLowerCase().includes(f))
      .map((d) => `<tr><td><span class="paso">${d.paso}</span></td><td class="col">${esc(d.columna)}</td>
        <td>${esc(d.accion)}</td><td class="num">${fmt(d.filas_afectadas)}</td><td>${esc(d.justificacion)}</td></tr>`)
      .join("") || `<tr><td colspan="5">Sin resultados.</td></tr>`;
  }
  document.getElementById("buscar").addEventListener("input", (e) => pintarDecisiones(e.target.value));
  pintarDecisiones("");

  function barras(filas, valor, formato, destacar, max) {
    const tope = max ?? Math.max(...filas.map((f) => f[valor]));
    return `<div class="barras">${filas
      .map((f) => `<div class="barra ${f.grupo === destacar ? "destacada" : ""}">
          <span class="nombre">${esc(f.grupo)}</span>
          <span class="pista"><span class="relleno" style="width:${(f[valor] / tope) * 100}%"></span></span>
          <span class="valor"><b>${formato(f[valor])}</b> · ${fmt(f.estudiantes)} est.</span>
        </div>`)
      .join("")}</div>`;
  }

  const p1 = P.p1, p2 = P.p2, p3 = P.p3, p4 = P.p4, p5 = P.p5;
  const beca = (k) => p2.find((f) => f.grupo === k);
  const est = (k) => p4.find((f) => f.grupo === k);
  const dif = (beca("no").tasa_desercion - beca("sí").tasa_desercion) * 100;
  const sube = p5.every((f, i) => i === 0 || f.tasa_desercion <= p5[i - 1].tasa_desercion);
  const nombresBeca = p2.map((f) => ({ ...f, grupo: f.grupo === "sí" ? "Con beca" : "Sin beca" }));

  const preguntas = [
    {
      t: "¿Qué programa presenta la tasa de deserción más alta?",
      r: `<b>${esc(p1[0].grupo)}</b>, con ${pct(p1[0].tasa_desercion)} (${fmt(p1[0].desertores)} de ${fmt(p1[0].estudiantes)} estudiantes). La más baja es ${esc(p1.at(-1).grupo)} con ${pct(p1.at(-1).tasa_desercion)}.`,
      g: barras(p1, "tasa_desercion", (v) => pct(v), p1[0].grupo),
    },
    {
      t: "¿Hay diferencia en la deserción entre becados y no becados?",
      r: `Sí. Sin beca: <b>${pct(beca("no").tasa_desercion)}</b> (${fmt(beca("no").estudiantes)} est.). Con beca: <b>${pct(beca("sí").tasa_desercion)}</b> (${fmt(beca("sí").estudiantes)} est.). Diferencia de ${fmt(dif, 1)} puntos porcentuales.`,
      g: barras(nombresBeca, "tasa_desercion", (v) => pct(v), dif > 0 ? "Sin beca" : "Con beca"),
    },
    {
      t: "¿Qué jornada tiene el menor promedio acumulado?",
      r: `<b>${esc(p3[0].grupo)}</b>, con ${fmt(p3[0].promedio, 2)} (${fmt(p3[0].estudiantes_con_dato)} estudiantes con promedio de ${fmt(p3[0].estudiantes)}).`,
      g: barras(p3, "promedio", (v) => fmt(v, 2), p3[0].grupo, 5),
    },
    {
      t: "¿Cuántas materias reprobadas tienen en promedio los desertores frente a los activos?",
      r: `Desertores: <b>${fmt(est("desertor").materias_reprobadas, 2)}</b> (${fmt(est("desertor").estudiantes)} est.). Activos: <b>${fmt(est("activo").materias_reprobadas, 2)}</b> (${fmt(est("activo").estudiantes)} est.). Se excluyen los graduados.`,
      g: barras(p4, "materias_reprobadas", (v) => fmt(v, 2), "desertor"),
    },
    {
      t: "¿La deserción aumenta conforme baja la asistencia?",
      r: `${sube ? "<b>Sí.</b>" : "<b>No de forma constante.</b>"} En el cuartil de menor asistencia (${fmt(p5[0].asistencia_min, 1)}-${fmt(p5[0].asistencia_max, 1)} %) la tasa es ${pct(p5[0].tasa_desercion)}; en el de mayor asistencia, ${pct(p5.at(-1).tasa_desercion)}. ${fmt(P.sin_asistencia)} estudiantes sin dato de asistencia quedan fuera.`,
      g: barras(p5, "tasa_desercion", (v) => pct(v), p5[0].grupo),
    },
  ];
  document.getElementById("lista-preguntas").innerHTML = preguntas
    .map((p, i) => `<article class="pregunta"><h3><span class="np">P${i + 1}.</span>${p.t}</h3><div class="respuesta">${p.r}</div>${p.g}</article>`)
    .join("");

  const visor = document.getElementById("visor");
  document.querySelectorAll(".galeria img").forEach((img) =>
    img.addEventListener("click", () => {
      visor.querySelector("img").src = img.src;
      visor.showModal();
    })
  );
  visor.addEventListener("click", () => visor.close());
})();
