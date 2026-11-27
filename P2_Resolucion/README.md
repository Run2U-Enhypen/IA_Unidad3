
# Práctica 2. Demostración por resolución

## Objetivo

Aplicar la resolución proposicional para demostrar
consecuencias lógicas mediante refutación, utilizando
Python y la forma normal conjuntiva (FNC).

## Contenido

- Conversión a forma normal conjuntiva.
- Demostraciones manuales por resolución.
- Implementación del algoritmo PL-RESOLUTION.
- Identificación y eliminación de tautologías.
- Preferencia unitaria.
- Estrategia de conjunto de soporte.
- Análisis de eficiencia.
- Visualización de resultados.

## Archivos

| Archivo | Descripción |
|---|---|
| p2_resolucion.ipynb | Notebook completo con explicaciones, código, resultados y gráficas. |
| p2_resolucion.py | Código fuente ejecutable en Python. |

## Resultados

| Ejercicio | Meta | Resultado |
|---|---|---|
| A | ¬P12 | True |
| B | S | True |
| C | R | False |

## Análisis de eficiencia

En el ejercicio B se obtuvieron los siguientes resultados:

| Métrica | Resolución exhaustiva | Conjunto de soporte |
|---|---:|---:|
| Pares evaluados | 91 | 19 |
| Resolventes nuevos | 10 | 4 |

- Reducción de pares evaluados: 79.12 %.
- Reducción de resolventes nuevos: 60 %.

## Tecnologías utilizadas

- Python 3
- Jupyter Notebook
- PyCharm
- Pandas
- Matplotlib

## Ejecución

El archivo Python puede ejecutarse mediante:

```bash
python p2_resolucion.py
```

## Asignatura

- Inteligencia Artificial (CDC-2411).
- Unidad 3. Representación del conocimiento y razonamiento.
- Ingeniería en Ciencia de Datos.
- Tecnológico Nacional de México.
