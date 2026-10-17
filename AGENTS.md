# Instrucciones para agentes y personas que continúan este proyecto

Agregador resiliente de APIs en FastAPI (Parcial 2 de Sistemas Distribuidos, UIS):
consume Open-Meteo y un servicio que falla a propósito, y expone una API propia
resiliente con un dashboard encima. El requerimiento se trabaja con **SPDD**.

## Dónde quedó el trabajo

El 2026-10-17 Javier, con su agente, hizo los pasos 1 y 3 de SPDD, e iteró con el
equipo 15 decisiones en tres rondas de preguntas. **No hay código de la aplicación**:
el equipo pidió cerrar las decisiones antes de desarrollar. El trabajo quedó a medias
a propósito, en el PR de la rama `docs/requerimientos-iniciales`, para que otra
persona del equipo lo continúe.

Leer en este orden:

1. [`README.md`](README.md): estado, log de decisiones D01–D15, riesgos R1–R3,
   pendientes P01–P15 y supuestos S1–S3.
2. [`requirements/AR-001-…-[Story]-…`](requirements/): historias HU1–HU7 con sus
   criterios de aceptación.
3. [`spdd/analysis/AR-001-…-[Analysis]-…`](spdd/analysis/): lo que se encontró
   explorando Open-Meteo y leyendo `servicio_inestable.py`. Todo está verificado con
   peticiones reales.
4. [`spdd/template/REASONS-canvas.md`](spdd/template/REASONS-canvas.md): la plantilla
   del siguiente paso.

## Reglas

1. **No escribir código de la aplicación** hasta que el canvas REASONS esté escrito y
   el equipo lo haya revisado. Es una decisión del equipo, no una sugerencia.
2. **Las decisiones se iteran con el equipo; el agente no decide solo.** Se presenta
   cada pregunta con sus opciones, se marca una recomendada y se explica qué cambia
   con cada una. Cuando el equipo confirma:
   - se agrega una fila a la tabla «Log de decisiones» del README con el siguiente ID
     (D16, D17, …), las alternativas descartadas, el porqué, la sección REASONS que
     alimenta y la ronda;
   - si cierra un pendiente, se borra de la tabla de pendientes y la decisión dice
     «cierra P0X»;
   - se actualiza el contador de la sección «Estado».
3. **Primero el canvas, después el código.** Si cambia el comportamiento, se corrige
   el canvas y luego se regenera el código. Si es un refactor sin cambio de
   comportamiento, se cambia el código y luego se sincroniza el canvas. Las secciones
   del canvas no se editan a mano sin dejar constancia de por qué.
4. La sección «D12 en detalle» del README explica los reintentos función por función.
   El equipo la pidió porque es lo que más pesa en la evaluación. Cuando exista el
   código, esa sección debe describir el código real, función por función, sin
   adelantarse ni quedarse atrás.
5. **No modificar `servicio_inestable.py`**: es del docente y se configura por
   parámetros de arranque.
6. Idioma: español en la API, el código, los commits y los documentos (supuesto S1).
7. Los diagramas Mermaid deben renderizar en GitHub. Hay que probarlos antes de hacer
   commit.
8. Git: una rama y un PR por cada cosa terminada, con Conventional Commits. Nunca se
   hace push directo a `main`. Prefijos de rama: `docs/`, `feat/`, `fix/`.

## Próximos pasos, en orden

1. **Revisar el PR de `docs/requerimientos-iniciales`**: confirmar D07 (quedó como
   propuesta sin objeciones) y los supuestos S1–S3.
2. **Cerrar los pendientes P01–P14 con el equipo**, en rondas cortas de preguntas.
   Los primeros que conviene cerrar son P08, P09 y P12, porque dan forma a la
   resiliencia, que vale 30 puntos.
3. Revisar el análisis en equipo y cambiar su estado a «revisado».
4. Escribir el canvas en
   `spdd/prompt/AR-001-AAAAMMDDhhmm-[Feat]-agregador-backend.md` a partir de la
   plantilla. Cada afirmación debe citar las D y P de las que depende.
5. Revisar el canvas en equipo.
6. Solo entonces generar código, tarea por tarea según la sección Operations: primero
   el backend (D09) y después el dashboard.

## Cómo seguir sobre el mismo PR

Para que la colaboración se vea en el repo, lo ideal es continuar sobre la misma rama
y que los commits de cada integrante queden en el mismo PR:

```bash
gh repo clone javierchacon262/agregador-resiliente
cd agregador-resiliente
gh pr checkout docs/requerimientos-iniciales
# … trabajar, y luego:
git add -A && git commit -m "docs(decisiones): cierra P08, P09 y P12"
git push
```
