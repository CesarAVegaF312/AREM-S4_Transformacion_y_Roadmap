# AREM S4 — Transformación y Roadmap

Material de la **Sesión 4** del curso *Arquitectura Empresarial* (AREM), Unidad 4:
**Transformación Empresarial y Roadmaps Arquitectónicos**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

Es la unidad que cierra el curso. Va de la arquitectura que se tiene a la que se necesita, **con la plata,
la gente y el tiempo que de verdad hay**: AS-IS, TO-BE, brechas por dominio, un roadmap T+0/T+1/T+2
priorizado por valor, riesgo y costo, y la gestión del cambio. Marcos de referencia: **TOGAF® Standard,
10th Edition** (fases E y F del ADM) y **ArchiMate® 3.2**.

Las actividades de la unidad, tal como están en la plataforma:

- **Actividad 4.1 — Presentación del reto** · grupal, de 3 a 4 integrantes · formativa, sin calificación · 4 horas.
  - **Entregable:** una ficha de contexto sectorial de **1 a 2 páginas**: tendencias de transformación
    digital del sector y **al menos dos casos reales** de referencia, en APA 7.
  - La retroalimentación se da en la sesión sincrónica con el **F-36**.
- **Actividad 4.2 — Proyecto integrador de transformación empresarial** · grupal, de **3 a 4
  integrantes** · 20 % · 20 horas.
  - **Entregable:** una propuesta de transformación arquitectónica en PDF, de **máximo 20 páginas más
    anexos**, en **norma APA 7**: resumen ejecutivo de 2 páginas, AS-IS, TO-BE, análisis de brechas,
    roadmap T+0/T+1/T+2, gestión del cambio y referencias. Y una **presentación en vivo de máximo 10
    minutos** ante un grupo que hace de comité de dirección.
  - Se califica con la rúbrica de la actividad, de cuatro criterios: arquitecturas AS-IS y TO-BE (1,5),
    análisis de brechas y roadmap (2,0), gestión del cambio y casos sectoriales (1,0) y calidad ejecutiva
    del documento (0,5).
  - **Los formatos F-30 a F-35 no se suben:** son el borrador de la propuesta y de la presentación.

---

## Empiecen aquí

**Todo el material se abre desde aquí, sin descargar nada:**
<https://cesaravegaf312.github.io/AREM-S4_Transformacion_y_Roadmap/>

Desde esa portada salen los documentos, las cuatro herramientas y la
[presentación de la sesión](https://cesaravegaf312.github.io/AREM-S4_Transformacion_y_Roadmap/presentacion.html).

1. **Lean el [mapa de la Actividad 4.2](documentos/1_actividad_4_2/AREM_S4_Mapa_Actividad_4_2.pdf).** Tres páginas: qué pide la actividad,
   con qué criterio se califica, en qué sección de la propuesta va cada cosa y qué formato y qué herramienta la prepara.
2. **Miren la [propuesta de ejemplo](documentos/1_actividad_4_2/AREM_S4_Informe_Ejemplo_Actividad_4_2.pdf).** Así se ve la 4.2 terminada, con
   Red Salud Andina. Cada sección abre con un recuadro que explica qué hay que hacer en ella.
3. **Relean las secciones 3, 8, 9, 12 y 13 del [dossier](documentos/2_caso/AREM_Caso_Red_Salud_Andina.pdf)** —o lo equivalente de su caso—:
   la ambición, la infraestructura, los datos, los episodios y las restricciones. El roadmap se escribe con la
   restricción real, no con la que les gustaría tener.

Para trabajar sin conexión, descarguen el repositorio (botón verde **`Code` → `Download ZIP`**),
descomprímanlo y hagan doble clic en `index.html`: la portada abre todos los documentos y
herramientas.

---

## Paso a paso de la unidad

Esta unidad **no empieza de cero**: casi todo lo que pide la 4.2 ya lo produjeron. El diagnóstico y las
brechas de la Unidad 1 (F-05 a F-12), las vistas, la decisión y la deuda de la Unidad 2 (F-13 a F-18) y el
gobierno de la Unidad 3 (F-22 a F-26) son los insumos. Los formatos están en los
[Instrumentos F-29 a F-37](documentos/3_como_se_hace/AREM_S4_Instrumentos.pdf), y cómo llenarlos con las
herramientas, en la [guía de herramientas y formatos](documentos/3_como_se_hace/AREM_S4_Guia_Herramientas_e_Instrumentos.pdf).

**El error más caro es dibujar el TO-BE antes de decidir el modelo operativo objetivo.** Sin esa
decisión —qué se comparte y qué no—, el TO-BE se vuelve la lista de deseos de TI.

### Paso 0 · La ficha sectorial (Actividad 4.1)

- **Cuándo:** antes de la sesión y durante la semana siguiente, en grupo.
- **Con qué:** la [guía de la Actividad 4.1](documentos/3_como_se_hace/AREM_S4_Guia_Actividad_4_1.pdf).
- **Produce:** **F-29** — tendencias con evidencia, dos casos reales verificados y la normativa que fija el calendario.
- **La regla:** abran la fuente. Un caso que solo aparece en el resumen de un buscador o en una respuesta
  de una IA no está verificado. Cada caso tiene que sostener una decisión del roadmap.

### Paso 1 · AS-IS y TO-BE

- **Cuándo:** antes de la sesión (el modelo operativo objetivo) y fuera de clase.
- **Produce:** **F-30** (AS-IS: modelo operativo, capacidades, portafolio, plataforma) y **F-31** (TO-BE,
  con al menos **dos vistas ArchiMate**). Las mismas capacidades en los dos, para que se puedan comparar.
- **Va a la propuesta en:** secciones 2 y 3.
- **Se califica en:** *Arquitecturas AS-IS y TO-BE* (1,5).

### Paso 2 · La matriz de brechas

- **Cuándo:** en el **taller de la sesión**.
- **Con qué:** [Matriz de brechas](interactivos/matriz_brechas_interactivo.html). Marca las brechas sin
  iniciativa y avisa cuando el TO-BE está escrito en tecnologías.
- **Produce:** **F-32** — brechas en los cuatro dominios, con su tipo (nuevo, transformar, eliminar) y la
  iniciativa que las cierra.
- **Va a la propuesta en:** sección 4 y anexo.
- **Se califica en:** *Análisis de brechas y roadmap* (2,0).

### Paso 3 · Priorizar y hacer que quepa

- **Cuándo:** en el **taller de la sesión** (primer borrador) y fuera de clase.
- **Con qué:** [Priorizador de portafolio](interactivos/priorizador_portafolio_interactivo.html). La barra del
  año 1 se pone roja si se pasan del presupuesto.
- **Produce:** **F-33, partes A y B** — valor, riesgo y costo en UC para **cada** iniciativa, y lo que no
  cabe en el año 1, diferido con su razón.
- **Va a la propuesta en:** secciones 5.1 a 5.3.
- **Se califica en:** *Análisis de brechas y roadmap* (2,0). Sin los tres números no hay nota máxima.

### Paso 4 · El roadmap en el tiempo

- **Cuándo:** fuera de clase, en grupo.
- **Con qué:** [Constructor de roadmap](interactivos/roadmap_interactivo.html). Comparte el portafolio con el
  Priorizador; marca las dependencias al revés y las iniciativas que chocan con una fecha ajena.
- **Produce:** **F-33, partes C y D** — T+0 (meses 0 a 6), T+1 (6 a 18) y T+2 (18 a 36), un resultado
  visible cada seis meses y, si la hay, la decisión que se deja abierta.
- **Va a la propuesta en:** secciones 5.4 a 5.6.

### Paso 5 · La gestión del cambio

- **Cuándo:** fuera de clase, en grupo.
- **Con qué:** [Mapa del cambio](interactivos/mapa_cambio_interactivo.html).
- **Produce:** **F-34** — grupos, lo que pierde cada uno, su resistencia y acciones de **comunicación y
  capacitación** con fecha y responsable.
- **Va a la propuesta en:** secciones 6 y 7 (con los casos de la 4.1).
- **Se califica en:** *Gestión del cambio y casos sectoriales* (1,0).

### Paso 6 · Resumen ejecutivo, presentación y verificación

- **Cuándo:** cuando los pasos 1 a 5 estén listos.
- **Produce:** **F-35** — el resumen ejecutivo de 2 páginas, sin siglas técnicas, y el guion de la
  presentación en vivo: 10 minutos, 10 diapositivas y una decisión pedida al comité.
- **Antes de subir y de presentar:** la lista del **F-37**, condición por condición.
- **Se califica en:** *Calidad ejecutiva del documento* (0,5).

**No copien el caso: cópienle la estructura.** El ejemplo es de una IPS de salud; su organización es otra.

---

## Qué hay en el repositorio

```text
AREM-S4_Transformacion_y_Roadmap/
├── index.html          ← portada: desde aquí se abre todo lo demás
├── presentacion.html   ← la sesión como presentación web, con los ejemplos animados
├── README.md
├── LICENSE
├── documentos/                 ← PDF, en el orden en que se usan
│   ├── 1_actividad_4_2/        ← qué se entrega y cómo se ve: mapa, propuesta de ejemplo, enunciado
│   ├── 2_caso/                 ← dossier de Red Salud Andina
│   ├── 3_como_se_hace/         ← instrumentos F-29 a F-37 y guías
│   └── 4_clase/                ← deck de la sesión
├── interactivos/               ← las cuatro herramientas HTML
└── fuentes/                    ← los mismos documentos en Word, y el deck en PowerPoint
```

### `documentos/` — PDF

| Carpeta | Archivo | Descripción |
|---|---|---|
| `1_actividad_4_2` | [`AREM_S4_Mapa_Actividad_4_2.pdf`](documentos/1_actividad_4_2/AREM_S4_Mapa_Actividad_4_2.pdf) | Lo que pide la 4.2, su rúbrica y, para cada requisito, la sección, el formato, cuándo se trabaja y la herramienta. |
| | [`AREM_S4_Informe_Ejemplo_Actividad_4_2.pdf`](documentos/1_actividad_4_2/AREM_S4_Informe_Ejemplo_Actividad_4_2.pdf) | Propuesta de transformación terminada de Red Salud Andina (20 páginas y dos anexos), con un recuadro por sección. |
| | [`AREM_S4_Enunciado_Actividad_4_2.pdf`](documentos/1_actividad_4_2/AREM_S4_Enunciado_Actividad_4_2.pdf) | El taller de la sesión: la idea que lo organiza, los cuatro pasos, el ejemplo resuelto y los conceptos. |
| `2_caso` | [`AREM_Caso_Red_Salud_Andina.pdf`](documentos/2_caso/AREM_Caso_Red_Salud_Andina.pdf) | El dossier del caso de respaldo, el mismo de las unidades anteriores. |
| `3_como_se_hace` | [`AREM_S4_Instrumentos.pdf`](documentos/3_como_se_hace/AREM_S4_Instrumentos.pdf) | Los nueve formatos F-29 a F-37. |
| | [`AREM_S4_Guia_Actividad_4_1.pdf`](documentos/3_como_se_hace/AREM_S4_Guia_Actividad_4_1.pdf) | Cómo hacer la ficha sectorial: fuentes, verificación de casos y normativa de salud verificada. |
| | [`AREM_S4_Guia_Herramientas_e_Instrumentos.pdf`](documentos/3_como_se_hace/AREM_S4_Guia_Herramientas_e_Instrumentos.pdf) | Las cuatro herramientas recorridas con el caso y los formatos campo por campo. |
| `4_clase` | [`AREM_S4_Deck_Reto_U4.pdf`](documentos/4_clase/AREM_S4_Deck_Reto_U4.pdf) | Las 21 diapositivas del encuentro sincrónico, con cada ejemplo en su estado final. |
| raíz | [`presentacion.html`](presentacion.html) | La misma sesión como presentación web: los ejemplos avanzan paso a paso con → (A los reproduce solos); índice (I), glosario de códigos (G) y cronómetro del taller (T). |
| `fuentes` | Los seis documentos en `.docx` y el deck en `.pptx` | Para adaptarlos: cambien lo que necesiten y expórtenlos a PDF. |

### `interactivos/` — herramientas HTML

Son **autocontenidas**: todo el HTML, CSS y JavaScript va dentro de un solo archivo. No requieren
instalación, ni servidor, ni conexión a internet. Lo que se escribe en ellas se guarda solo en el
navegador de quien las usa.

| Archivo | Para qué sirve | Paso |
|---|---|---|
| [`matriz_brechas_interactivo.html`](interactivos/matriz_brechas_interactivo.html) | Brechas por dominio con su tipo e iniciativa; lleva las iniciativas al Priorizador. | 2 |
| [`priorizador_portafolio_interactivo.html`](interactivos/priorizador_portafolio_interactivo.html) | Valor, riesgo y costo; el año 1 contra el presupuesto; lo que se difiere. | 3 |
| [`roadmap_interactivo.html`](interactivos/roadmap_interactivo.html) | Gantt de 36 meses con barras que se arrastran, fechas ajenas, resultados visibles y decisión abierta. | 4 |
| [`mapa_cambio_interactivo.html`](interactivos/mapa_cambio_interactivo.html) | Grupos en la rejilla de poder e interés, con resistencias y acciones. | 5 |

Las cuatro abren con **Red Salud Andina**, tienen el botón **«Empezar con el caso del grupo»** y un
**«Recorrido animado del caso»** que construye el ejemplo paso a paso, comete un error típico y lo corrige;
al salir, la herramienta vuelve a lo que tenían en pantalla. Para abrirlas directamente en blanco, agreguen
`?caso=grupo` al final de la dirección. El Priorizador y el Constructor de roadmap trabajan sobre el mismo
portafolio.

> Las Sesiones 1, 2 y 3 están en sus propios repositorios:
> [AREM-S1_Marcos_y_Capacidades](https://github.com/CesarAVegaF312/AREM-S1_Marcos_y_Capacidades-repositorio),
> [AREM-S2_Modelado_y_Decision](https://github.com/CesarAVegaF312/AREM-S2_Modelado_y_Decision) y
> [AREM-S3_Gobierno_y_Control](https://github.com/CesarAVegaF312/AREM-S3_Gobierno_y_Control).
> El roadmap de esta unidad lo gobierna el ARB de la Unidad 3.

---

## Problemas frecuentes

**Al hacer clic en un `.html` dentro de GitHub se ve código, no la herramienta.**
GitHub muestra el código fuente, no lo ejecuta. Usen el enlace publicado de arriba, o descarguen el
repositorio y ábranlo desde su computador.

**El doble clic sobre un `.html` abre un editor de texto.**
Clic derecho → **Abrir con** → Chrome, Edge o Firefox.

**El Priorizador muestra iniciativas que no escribí.**
El Priorizador y el Constructor de roadmap comparten el portafolio, y la Matriz de brechas le pasa sus
iniciativas. Para volver al ejemplo, pulsen **«Caso Red Salud Andina»**; para empezar en blanco,
**«Empezar con el caso del grupo»**.

**En el teléfono, los ejemplos de la presentación se ven pequeños.**
Giren el teléfono en horizontal, o usen el botón **Lectura** para ver todas las diapositivas de corrido.

---

## Referencias

- Kotter, J. P. (1996). *Leading change*. Harvard Business School Press.
- Lankhorst, M. (2017). *Enterprise architecture at work: Modelling, communication and analysis* (4.ª ed.).
  Springer. https://doi.org/10.1007/978-3-662-53933-0
- Pham, T., Pham, D. K., & Pham, A. T. (2013). *From business strategy to information technology roadmap: A
  practical guide for executives and board members*. Productivity Press. https://doi.org/10.4324/9781315373195
- Ross, J. W., Weill, P., & Robertson, D. C. (2006). *Enterprise architecture as strategy: Creating a
  foundation for business execution*. Harvard Business School Press.
- The Open Group. (2022). *The TOGAF® Standard, 10th Edition*. https://www.opengroup.org/togaf
- The Open Group. (2022). *ArchiMate® 3.2 specification*. https://pubs.opengroup.org/architecture/archimate32-doc/
- Weill, P., & Woerner, S. L. (2018). *What's your digital business model? Six questions to help you build
  the next-generation enterprise*. Harvard Business Review Press.

La normativa colombiana de salud y los casos del sector, con su verificación de septiembre de 2026, están en
la [guía de la Actividad 4.1](documentos/3_como_se_hace/AREM_S4_Guia_Actividad_4_1.pdf).

---

## Licencia

Este material se distribuye bajo la licencia [Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es) — ver [`LICENSE`](LICENSE).

Pueden **usar, adaptar o compartir** este contenido, incluido el código de los interactivos, con fines educativos, siempre que:

1. Se reconozca la autoría del profesor **César Augusto Vega Fernández**.
2. No se utilice con fines comerciales.
3. Las obras derivadas se distribuyan bajo la misma licencia.

*Nota: TOGAF® y ArchiMate® son marcas registradas de The Open Group. Este repositorio contiene material
docente que los explica; la licencia aplica a estos materiales, no a los marcos originales. Red Salud
Andina es una organización simulada con fines pedagógicos.*
