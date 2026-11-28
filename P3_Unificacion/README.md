
# Práctica 3. Unificación y encadenamiento en lógica de primer orden

## Datos generales

- Asignatura: Inteligencia Artificial (CDC-2411).
- Unidad 3: Representación del conocimiento y razonamiento.
- Institución: Tecnológico Nacional de México.
- Lenguajes: Python y Prolog.

## Objetivo

Implementar el algoritmo de unificación y el encadenamiento hacia adelante en lógica de primer orden, comparar su funcionamiento con el encadenamiento hacia atrás en Prolog y analizar las limitaciones de la búsqueda en profundidad.

## Contenido de la práctica

### Parte A. Implementación en Python

- Algoritmo de unificación.
- Unificador más general (UMG).
- Verificación de ocurrencia (occurs check).
- Renombramiento de variables.
- Encadenamiento hacia adelante.
- Demostración del caso del coronel West.
- Análisis de eficiencia.
- Tablas y gráficas.

### Parte B. Implementación en Prolog

- Representación de hechos y reglas.
- Encadenamiento hacia atrás.
- Consultas en SWISH.
- Traza de ejecución.
- Árbol de pruebas Y-O (AND-OR).

### Parte C. Recursividad izquierda

- Relaciones de parentesco.
- Análisis de la recursividad infinita.
- Error de agotamiento de pila.
- Implementación del caso base.
- Corrección del orden de los objetivos.
- Búsqueda en profundidad y retroceso.

## Archivos

| Archivo | Descripción |
|---|---|
| p3_unificacion.ipynb | Notebook completo con teoría, código, resultados, nueve gráficas y cuestionario. |
| p3_unificacion.py | Implementación independiente del algoritmo de unificación y encadenamiento hacia adelante. |
| west.pl | Base de conocimiento del coronel West en Prolog. |
| ancestro.pl | Implementación corregida de las relaciones de parentesco. |
| README.md | Documentación general de la práctica. |

## Resultados obtenidos

### Unificación

| Indicador | Resultado |
|---|---:|
| Pares evaluados | 5 |
| Unificaciones exitosas | 3 |
| Unificaciones fallidas | 2 |

### Encadenamiento hacia adelante

| Indicador | Resultado |
|---|---:|
| Hechos iniciales | 4 |
| Reglas de inferencia | 4 |
| Hechos derivados | 4 |
| Hechos finales | 8 |
| Rondas necesarias | 2 |
| Combinaciones evaluadas | 2744 |
| Intentos de unificación | 3218 |
| Combinaciones válidas | 7 |

La meta Criminal(West) fue demostrada correctamente en la segunda ronda.

### Encadenamiento hacia atrás

| Indicador | Resultado |
|---|---|
| Consulta criminal(Q) | Q = west |
| Consulta criminal(west) | true |
| Consulta criminal(nono) | false |
| Eventos Call | 9 |
| Eventos Exit | 9 |
| Eventos Redo | 0 |
| Eventos Fail | 0 |

### Recursividad izquierda

La versión incorrecta produjo un error de agotamiento de pila:

- Error: Stack limit exceeded.
- Límite de pila: 0.2 GB.
- Profundidad alcanzada: 2567717.

La versión corregida permitió obtener:

- Cuatro relaciones de parentesco directas.
- Dos relaciones de parentesco indirectas.
- Seis relaciones de parentesco en total.

## Herramientas utilizadas

- Python 3.
- PyCharm.
- Jupyter Notebook.
- Pandas.
- Matplotlib.
- itertools.
- SWI-Prolog.
- SWISH.
- GitHub.

## Instrucciones de ejecución

### Python

Ejecutar desde una terminal:

```bash
python p3_unificacion.py
```

El archivo Python independiente utiliza únicamente la biblioteca estándar.

Para ejecutar el Notebook completo se requieren Pandas y Matplotlib:

```bash
pip install pandas matplotlib
```

### Prolog

Abrir SWISH:

https://swish.swi-prolog.org/

Cargar el contenido de west.pl y ejecutar:

```prolog
criminal(Q).
```

Para observar la traza:

```prolog
trace, criminal(west).
```

Para comprobar las relaciones de parentesco, cargar ancestro.pl en un programa independiente y ejecutar:

```prolog
ancestro(A, b).
```

## Conclusión

Ambas estrategias de inferencia permitieron demostrar que el coronel West es un criminal.

El encadenamiento hacia adelante generó nuevos hechos a partir de la base de conocimiento, mientras que el encadenamiento hacia atrás buscó los subobjetivos necesarios para demostrar la meta.

También se comprobó que el orden de los objetivos y la existencia de un caso base son fundamentales para evitar problemas de recursividad en Prolog.

## Uso de inteligencia artificial

Se utilizó ChatGPT como herramienta de apoyo para la comprensión de conceptos, implementación de algoritmos, documentación y análisis de resultados.

Los programas fueron ejecutados y verificados en PyCharm y SWISH.
