# Plantilla · Canvas REASONS (prompt estructurado de SPDD)

Copiar a `spdd/prompt/AR-NNN-AAAAMMDDhhmm-[Feat]-descripcion-corta.md` y llenar cada
sección. El canvas es la fuente de verdad del comportamiento: si el código y el canvas
no coinciden, **se corrige primero el canvas** y después el código.

Cada afirmación que dependa de una decisión debe citar su ID del
[log de decisiones](../../README.md#log-de-decisiones) (D01, D02, …). Si una sección
necesita algo que todavía no está decidido, se cita el pendiente (P01, P02, …) y **no**
se genera código para esa parte hasta cerrarlo.

| Campo | Valor |
|---|---|
| ID | AR-NNN |
| Historia | enlace a `requirements/…` |
| Análisis | enlace a `spdd/analysis/…` |
| Estado | borrador · revisado por el equipo · generado · sincronizado |
| Revisado por | nombres del equipo |

## R · Requirements (requisitos)

¿Qué problema resolvemos y cuál es la definición de terminado? Criterios de
aceptación verificables, con códigos de estado.

## E · Entities (entidades)

Entidades del dominio y sus relaciones, con los campos que viajan en la API (modelos
Pydantic de entrada, de salida y de las respuestas externas).

## A · Approach (enfoque)

Estrategia para cumplir R y por qué se eligió frente a las alternativas (citar las D).

## S · Structure (estructura)

Dónde encaja cada cosa: módulos, archivos, dependencias entre ellos y con los
servicios externos.

## O · Operations (operaciones)

La estrategia partida en pasos concretos y verificables, en el orden en que se van a
generar. Cada paso dice qué archivo toca y cómo se comprueba.

1. …
2. …

## N · Norms (normas)

Convenciones transversales: nombres, idioma, formato de logs, manejo de errores,
configuración por variables de entorno, estilo de commits.

## S · Safeguards (salvaguardas)

Límites que no se negocian: invariantes, límites de rendimiento, reglas de seguridad.
Lo que nunca debe pasar (p. ej. «nunca reintentar un 404»).
