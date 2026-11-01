# AREM S4 — Laboratorio: la consolidación, ensayada

Laboratorio de la **Sesión 4** del curso *Arquitectura Empresarial* (AREM), Unidad 4:
**Transformación Empresarial y Roadmaps Arquitectónicos**. Maestría en Ingeniería de Software,
Universidad de La Sabana.

Un roadmap dice qué se hace en T+0, T+1 y T+2. Lo difícil es justificar el orden: por qué una
iniciativa va antes que otra, qué se mide para decidir que se avanza y qué pasa si algo sale mal a
mitad de camino. En este laboratorio esa transición **se ejecuta**: las seis sedes adquiridas a
Centro Médico del Norte pasan de HIS-NORTE a HIS-CORE, sede por sede, detrás de una fachada. Es
el patrón *Strangler Fig*, el mismo que en la Unidad 2 aparece frente a la reescritura de una vez.

Es la rama B del [documento de ejemplo](../documentos/1_actividad_4_2/AREM_S4_Informe_Ejemplo_Actividad_4_2.pdf)
de la Actividad 4.2: consolidar las seis sedes en HIS-CORE y apagar HIS-NORTE, una decisión que
el roadmap deja para el mes 18 con cinco criterios medidos. El laboratorio permite medir uno de
ellos, el C3 (procedimientos de HIS-NORTE con código homologado, umbral ≥ 95 %), y ensayar el
camino antes de decidir. No hay que programar.

---

## La situación

- Las seis sedes registran sus admisiones en HIS-NORTE. HIS-CORE, el sistema de las otras 18 sedes
  y la clínica, no conoce a esos pacientes.
- Los dos sistemas codifican los procedimientos de forma distinta, y la homologación no está
  completa (dossier, sección 9).
- FACT-SALUD saca datos de HIS-NORTE por su cuenta, sin pasar por ninguna interfaz formal
  (dossier, sección 7).
- El contrato de HIS-NORTE vence en 2027.

| Servicio | Qué es |
|---|---|
| `fachada` | El punto único por el que las sedes registran admisiones. Decide, sede por sede, a qué HIS va cada una. En <http://localhost:8080>. |
| `his-norte` | Simulador de HIS-NORTE. Lleva la cuenta de quién lo usa. |
| `his-core` | Simulador de HIS-CORE. Solo conoce a los pacientes de una sede cuando se migran sus datos, y solo entiende los procedimientos homologados. |
| `fact-salud` | FACT-SALUD extrayendo datos de HIS-NORTE cada 15 segundos, por fuera de la fachada. |
| `migracion` | La herramienta del laboratorio. |

La fachada tiene cuatro modos por sede:

| Modo | Qué pasa |
|---|---|
| `norte` | Todo va a HIS-NORTE. Es el estado inicial. |
| `sombra` | Responde HIS-NORTE y, por detrás, la misma admisión se manda a HIS-CORE para comparar las respuestas. El usuario no ve a HIS-CORE. |
| `canario` | Un porcentaje de las admisiones lo atiende HIS-CORE; el resto, HIS-NORTE. |
| `core` | Todo va a HIS-CORE. |

---

## Requisitos

- **Docker Desktop** (Windows o Mac) o Docker Engine con el plugin Compose (Linux). Verifiquen con
  `docker compose version`.
- **Sin Docker en su equipo:** abran el repositorio en **GitHub Codespaces** (botón verde
  **`Code` → `Codespaces`**) y elijan la configuración **«AREM S4 · Laboratorio de la
  consolidación»**. En la terminal, entren a la carpeta con `cd laboratorio`.

---

## Levantar el laboratorio

```bash
git clone https://github.com/CesarAVegaF312/AREM-S4_Transformacion_y_Roadmap.git
cd AREM-S4_Transformacion_y_Roadmap/laboratorio
docker compose up -d --build
docker compose run --rm migracion estado
```

Todos los comandos de esta guía se ejecutan dentro de la carpeta `laboratorio/`. Si el último
muestra las seis sedes en `norte`, el laboratorio está listo.

Los comandos del laboratorio:

```bash
docker compose run --rm migracion admisiones                  # las sedes registran admisiones
docker compose run --rm migracion ruta --sede N1 --modo sombra # cambia a qué HIS va una sede
docker compose run --rm migracion migrar-datos --sede N1       # lleva los pacientes de una sede a HIS-CORE
docker compose run --rm migracion homologar                    # completa la homologación de procedimientos
docker compose run --rm migracion estado                       # rutas, datos, comparación y quién usa HIS-NORTE
docker compose run --rm migracion apagar-norte                 # verifica si HIS-NORTE se puede apagar
docker compose run --rm migracion reiniciar                    # vuelve al estado inicial
```

En `ruta` y `migrar-datos`, `--sede todas` aplica a las seis sedes. Cada corrida de `admisiones`
guarda su resumen en `resultados/` con las rutas vigentes.

---

## Experimentos

Hagan los seis en orden, **sin reiniciar entre uno y otro**: cada uno parte de donde quedó el
anterior, como en una transición real. Empiecen con `reiniciar`. Antes de cada paso, escriban qué
esperan que pase. Tiempo estimado: dos horas.

### Experimento 1 — T+0: la fachada, sin cambiar nada

```bash
docker compose run --rm migracion reiniciar
docker compose run --rm migracion admisiones --etiqueta e1
```

Las seis sedes ya pasan por la fachada, pero todo sigue yendo a HIS-NORTE.

**Registren:** el éxito y el tiempo de respuesta (p95) por sede.

**Para pensar:** este paso no le da nada visible a nadie: las sedes trabajan igual que antes. ¿Por
qué va primero en el roadmap? ¿Cómo se le explica a un comité de dirección una iniciativa cuyo
valor es habilitar las siguientes?

### Experimento 2 — El atajo

Alguien propone pasar la Sede Norte 1 a HIS-CORE de una vez.

```bash
docker compose run --rm migracion ruta --sede N1 --modo core
docker compose run --rm migracion admisiones --sede N1 --peticiones 50
```

Cuando vean el resultado, deshagan el cambio y comprueben que la sede vuelve a funcionar:

```bash
docker compose run --rm migracion ruta --sede N1 --modo norte
docker compose run --rm migracion admisiones --sede N1 --peticiones 50
```

**Registren:** el éxito de la sede con el atajo, el error que ven las admisiones y cuánto tomó
volver atrás.

**Para pensar:** ¿qué iniciativa tenía que ir antes? En su roadmap, ¿esa dependencia está escrita?
Volver atrás tomó un comando porque la fachada existe: ¿cuánto habría costado sin ella?

### Experimento 3 — Migrar los datos y comparar en sombra

```bash
docker compose run --rm migracion migrar-datos --sede N1
docker compose run --rm migracion ruta --sede N1 --modo sombra
docker compose run --rm migracion admisiones --sede N1 --peticiones 200
docker compose run --rm migracion estado
```

En sombra, la sede sigue trabajando con HIS-NORTE y nadie nota nada, pero cada admisión también se
manda a HIS-CORE y se comparan las dos respuestas.

**Registren:** el porcentaje de admisiones iguales, las diferencias por tipo y el porcentaje de
códigos homologados.

**Para pensar:** compárenlo con el criterio C3 del documento de ejemplo (≥ 95 % de procedimientos
homologados). ¿La rama B está lista? Una admisión con «tarifa distinta», si pasara a producción,
¿en qué se convierte en el área financiera?

### Experimento 4 — El canario, antes de tiempo

Alguien propone no esperar y mandar ya el 20 % de las admisiones de la Sede Norte 1 a HIS-CORE.

```bash
docker compose run --rm migracion ruta --sede N1 --modo canario --porcentaje 20
docker compose run --rm migracion admisiones --sede N1 --peticiones 200
```

**Registren:** cuántas admisiones atendió HIS-CORE y cuántas fallaron.

**Para pensar:** en sombra, las mismas diferencias no le llegaban a nadie; ahora le llegan a un
paciente en la ventanilla. ¿Cuál debería ser el criterio para pasar de sombra a canario, y quién
lo decide?

### Experimento 5 — Cerrar la brecha y hacer el corte

La homologación es una iniciativa del roadmap: alguien tiene que asignar los códigos que faltan.

```bash
docker compose run --rm migracion homologar
docker compose run --rm migracion ruta --sede N1 --modo sombra
docker compose run --rm migracion admisiones --sede N1 --peticiones 200
docker compose run --rm migracion estado
```

Cuando la comparación en sombra cumpla el criterio que definieron en el experimento 4, hagan el
corte de la sede:

```bash
docker compose run --rm migracion ruta --sede N1 --modo core
docker compose run --rm migracion admisiones --sede N1 --peticiones 100
```

**Registren:** el porcentaje de iguales después de homologar, la diferencia que queda y el éxito
de la sede en HIS-CORE.

**Para pensar:** la homologación quitó un tipo de diferencia, pero la «tarifa distinta» sigue ahí.
Esa no se arregla con tecnología: es una tarifa distinta en el contrato. ¿A quién le toca, y en qué
horizonte del roadmap va?

### Experimento 6 — Apagar HIS-NORTE

Repitan el camino con las otras cinco sedes (pueden hacerlas todas a la vez) y verifiquen si
HIS-NORTE se puede apagar:

```bash
docker compose run --rm migracion migrar-datos --sede todas
docker compose run --rm migracion ruta --sede todas --modo core
docker compose run --rm migracion admisiones
docker compose run --rm migracion apagar-norte
```

Lean la verificación. Después apáguenlo de todas maneras, esperen un minuto y miren el estado:

```bash
docker compose run --rm migracion apagar-norte --forzar
docker compose run --rm migracion estado
```

**Registren:** qué dice la verificación y qué pasa después de apagar.

**Para pensar:** la fachada solo ve lo que pasa por ella. ¿En qué documento de la organización
estaba ese otro consumidor? Revisen la sección 7 del dossier. ¿Qué iniciativa le falta al roadmap
para poder apagar HIS-NORTE antes de que venza el contrato?

---

## Del laboratorio a la propuesta

Los seis experimentos son una transición en miniatura. Al pasarla a la Actividad 4.2:

| Lo que vieron | Dónde va en la propuesta |
|---|---|
| La fachada sin valor visible (exp. 1) | Una capacidad habilitadora de T+0 en el roadmap, justificada por lo que permite después. |
| El atajo que falla (exp. 2) | Una dependencia explícita del gap analysis: los datos antes que la ruta. |
| La comparación en sombra (exp. 3 y 5) | El criterio de avance de cada sede, y la medición del C3 que exige la decisión del mes 18. |
| El canario antes de tiempo (exp. 4) | Un riesgo con su control: no se pasa a canario sin cumplir el criterio de la sombra. |
| La tarifa distinta (exp. 5) | Una iniciativa que no es de TI: la renegociación de tarifas, con su dueño en el negocio. |
| El consumidor oculto (exp. 6) | La iniciativa que falta para retirar HIS-NORTE: la interfaz formal hacia FACT-SALUD. |
| Una sede primero, luego las demás | La gestión del cambio: una sede piloto con su gente antes de las otras cinco. |

Dos advertencias para el análisis:

- **Es un modelo, no el sistema real.** Los pacientes, las tarifas y los porcentajes son
  inventados. Sirven para entender el orden y los criterios de la transición, no para estimar
  tiempos ni costos. Díganlo en la propuesta.
- **En el laboratorio, migrar una sede toma un segundo.** En la realidad, la migración de datos
  y la homologación son las iniciativas largas del roadmap, y las que más riesgo tienen.

---

## Problemas frecuentes

**`docker: command not found` o «Cannot connect to the Docker daemon».**
Docker Desktop no está instalado o no está abierto. Ábranlo y esperen a que diga que está
corriendo.

**«port is already allocated».**
Otro programa usa el puerto 8080. Ciérrenlo, o cambien el número de la izquierda en
`docker-compose.yml` (por ejemplo `"18080:8080"`).

**`estado` dice que algo no responde.**
Si acaban de levantar el laboratorio, esperen unos segundos y repitan.

**Los números no coinciden con los del experimento anterior.**
Las rutas y los datos migrados se conservan entre comandos, a propósito. Si quieren empezar de
nuevo, usen `reiniciar`.

---

## Licencia

Este laboratorio es parte del repositorio de la Sesión 4 y se distribuye con su misma licencia,
[Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es),
incluido el código del laboratorio.

*Nota: Red Salud Andina y Centro Médico del Norte son organizaciones simuladas con fines
pedagógicos.*
