# -*- coding: utf-8 -*-
"""Práctica 3 - Unificación y encadenamiento en lógica de primer orden.
Inteligencia Artificial (CDC-2411), Unidad 3.
Extraído del Notebook p3_unificacion.ipynb.
Apoyo de ChatGPT declarado en el Notebook.
Ejecutar: python p3_unificacion.py
"""
import itertools


def es_var(t):
    """
    Determina si un término representa una variable.

    Parámetro:
        t: término que se desea evaluar.

    Retorna:
        True si es una variable.
        False en caso contrario.
    """

    return isinstance(t, str) and bool(t) and t[0].islower()


def sustituir(t, s):
    """
    Aplica una sustitución a un término.

    Parámetros:
        t: término original.
        s: diccionario de sustituciones.

    Retorna:
        El término después de aplicar las sustituciones.
    """

    # Caso 1: el término es una variable
    if es_var(t):

        # Si existe una sustitución, aplicarla recursivamente
        if t in s:
            return sustituir(s[t], s)

        # Si no existe, conservar la variable
        return t

    # Caso 2: el término es una expresión compuesta
    if isinstance(t, tuple):

        # Aplicar las sustituciones a cada elemento
        return tuple(sustituir(a, s) for a in t)

    # Caso 3: el término es una constante
    return t


def ocurre(v, t, s):
    """
    Comprueba si una variable aparece dentro de un término.

    Parámetros:
        v: variable que se desea buscar.
        t: término que se desea evaluar.
        s: diccionario de sustituciones existentes.

    Retorna:
        True si la variable aparece dentro del término.
        False en caso contrario.
    """

    # Aplicar las sustituciones existentes
    t = sustituir(t, s)

    # Caso 1: la variable coincide con el término
    if v == t:
        return True

    # Caso 2: el término es una expresión compuesta
    if isinstance(t, tuple):

        # Buscar la variable dentro de sus argumentos
        return any(ocurre(v, a, s) for a in t[1:])

    # Caso 3: la variable no aparece
    return False


def unificar(x, y, s=None):
    """
    Calcula el unificador más general de dos términos.

    Parámetros:
        x: primer término.
        y: segundo término.
        s: diccionario de sustituciones existentes.

    Retorna:
        Diccionario con las sustituciones del UMG.
        None si los términos no pueden unificarse.
    """

    # Inicializar el diccionario de sustituciones
    if s is None:
        s = {}
    else:
        s = s.copy()

    # Aplicar las sustituciones existentes
    x = sustituir(x, s)
    y = sustituir(y, s)

    # Caso 1: los términos son iguales
    if x == y:
        return s

    # Caso 2: x es una variable
    if es_var(x):

        # Verificar que x no aparezca dentro de y
        if ocurre(x, y, s):
            return None

        # Agregar la sustitución
        s[x] = y
        return s

    # Caso 3: y es una variable
    if es_var(y):

        # Verificar que y no aparezca dentro de x
        if ocurre(y, x, s):
            return None

        # Agregar la sustitución
        s[y] = x
        return s

    # Caso 4: ambos términos son expresiones compuestas
    if isinstance(x, tuple) and isinstance(y, tuple):

        # Verificar que tengan la misma longitud
        if len(x) != len(y):
            return None

        # Verificar que tengan el mismo nombre
        if x[0] != y[0]:
            return None

        # Unificar los argumentos uno por uno
        for a, b in zip(x[1:], y[1:]):

            s = unificar(a, b, s)

            # Si algún argumento no unifica,
            # toda la expresión falla
            if s is None:
                return None

        return s

    # Caso 5: términos incompatibles
    return None


def formato_termino(t):
    """
    Convierte un término de Python en una
    expresión de lógica de primer orden.
    """

    # Si es una expresión compuesta
    if isinstance(t, tuple):

        nombre = t[0]

        argumentos = ", ".join(
            formato_termino(a) for a in t[1:]
        )

        return f"{nombre}({argumentos})"

    # Si es una variable o constante
    return str(t)


def formato_sustitucion(s):
    """
    Convierte un diccionario de sustituciones
    en una representación legible.
    """

    # Si la unificación falló
    if s is None:
        return "None"

    elementos = [
        f"{v} → {formato_termino(t)}"
        for v, t in s.items()
    ]

    return "{" + ", ".join(elementos) + "}"


HECHOS = {
    ("Posee", "Nono", "M1"),
    ("Misil", "M1"),
    ("Americano", "West"),
    ("Enemigo", "Nono", "America")
}


REGLAS = [

    # R1: Venta ilegal de armas
    (
        [
            ("Americano", "x"),
            ("Arma", "y"),
            ("Vende", "x", "y", "z"),
            ("Hostil", "z")
        ],
        ("Criminal", "x")
    ),

    # R2: Venta de misiles
    (
        [
            ("Misil", "x"),
            ("Posee", "Nono", "x")
        ],
        ("Vende", "West", "x", "Nono")
    ),

    # R3: Todo misil es un arma
    (
        [
            ("Misil", "x")
        ],
        ("Arma", "x")
    ),

    # R4: Todo enemigo de América es hostil
    (
        [
            ("Enemigo", "x", "America")
        ],
        ("Hostil", "x")
    )
]


def formato_regla(regla):
    """
    Convierte una regla de Python en una
    expresión de lógica de primer orden.
    """

    # Separar las premisas y la conclusión
    premisas, conclusion = regla

    # Convertir las premisas en texto
    texto_premisas = " ∧ ".join(
        formato_termino(p) for p in premisas
    )

    # Convertir la conclusión en texto
    texto_conclusion = formato_termino(conclusion)

    # Construir la representación de la regla
    return f"{texto_premisas} ⇒ {texto_conclusion}"


def renombrar(regla, k):
    """
    Renombra las variables de una regla.

    Parámetros:
        regla: tupla de premisas y conclusión.
        k: identificador utilizado como sufijo.

    Retorna:
        Una nueva regla con variables renombradas.
    """

    def renombrar_termino(t):

        # Caso 1: el término es una variable
        if es_var(t):
            return t + str(k)

        # Caso 2: expresión compuesta
        if isinstance(t, tuple):

            return (t[0],) + tuple(
                renombrar_termino(a)
                for a in t[1:]
            )

        # Caso 3: constante
        return t

    # Separar premisas y conclusión
    premisas, conclusion = regla

    # Renombrar las premisas
    nuevas_premisas = [
        renombrar_termino(p)
        for p in premisas
    ]

    # Renombrar la conclusión
    nueva_conclusion = renombrar_termino(conclusion)

    return nuevas_premisas, nueva_conclusion


def fol_fc_ask(hechos, meta):
    """
    Implementa el encadenamiento hacia adelante.

    Parámetros:
        hechos: conjunto de hechos iniciales.
        meta: expresión que se desea demostrar.

    Retorna:
        True si la meta puede demostrarse.
        False si no se generan nuevos hechos
        y la meta no ha sido encontrada.
    """

    # Crear una copia de los hechos iniciales
    conocidos = set(hechos)

    # Inicializar el contador de rondas
    ronda = 0

    # Mostrar la meta
    print("META:", formato_termino(meta))

    # Comprobar si la meta ya es un hecho conocido
    for hecho in sorted(conocidos):

        if unificar(meta, hecho) is not None:

            print("La meta ya es un hecho conocido.")
            return True

    # Iniciar el proceso de inferencia
    while True:

        ronda += 1

        # Almacenar los nuevos hechos de la ronda
        nuevos = set()

        print(f"\nRONDA {ronda}")
        print("=" * 60)

        # Obtener los hechos disponibles al iniciar la ronda
        hechos_ronda = sorted(conocidos)

        # Recorrer todas las reglas
        for i, regla in enumerate(REGLAS, start=1):

            # Renombrar las variables de la regla
            premisas, conclusion = renombrar(
                regla, f"{ronda}_{i}"
            )

            # Generar las combinaciones de hechos
            combinaciones = itertools.product(
                hechos_ronda,
                repeat=len(premisas)
            )

            # Evaluar cada combinación
            for combinacion in combinaciones:

                # Inicializar las sustituciones
                s = {}

                # Unificar cada premisa con un hecho
                for premisa, hecho in zip(
                    premisas, combinacion
                ):

                    s = unificar(premisa, hecho, s)

                    # Si una premisa falla,
                    # descartar la combinación
                    if s is None:
                        break

                # Si todas las premisas se satisfacen
                if s is not None:

                    # Generar la conclusión
                    nuevo_hecho = sustituir(
                        conclusion, s
                    )

                    # Evitar hechos duplicados
                    if (
                        nuevo_hecho not in conocidos
                        and nuevo_hecho not in nuevos
                    ):

                        nuevos.add(nuevo_hecho)

                        # Mostrar la regla disparada
                        print(f"Regla R{i} disparada:")

                        print(
                            "  Sustituciones:",
                            formato_sustitucion(s)
                        )

                        print(
                            "  Nuevo hecho:",
                            formato_termino(nuevo_hecho)
                        )

        # Comprobar si se generaron nuevos hechos
        if not nuevos:

            print("No se generaron nuevos hechos.")
            print("No se pudo demostrar la meta.")

            return False

        # Incorporar los nuevos hechos
        conocidos.update(nuevos)

        print(f"\nHechos nuevos: {len(nuevos)}")
        print(f"Hechos acumulados: {len(conocidos)}")

        # Comprobar si se alcanzó la meta
        for hecho in sorted(nuevos):

            respuesta = unificar(meta, hecho)

            if respuesta is not None:

                print("\nMETA DEMOSTRADA")

                print(
                    "Hecho encontrado:",
                    formato_termino(hecho)
                )

                print(
                    "Sustituciones:",
                    formato_sustitucion(respuesta)
                )

                print(f"Rondas necesarias: {ronda}")

                return True


def fol_fc_estadisticas(hechos, meta):
    """
    Ejecuta el encadenamiento hacia adelante
    y recopila estadísticas por ronda.

    Retorna:
        Resultado de la consulta.
        Conjunto de hechos finales.
        Lista de estadísticas.
        Lista de hechos derivados.
    """

    conocidos = set(hechos)

    estadisticas = []
    derivaciones = []

    ronda = 0

    # Comprobar los hechos iniciales
    if any(
        unificar(meta, h) is not None
        for h in conocidos
    ):

        return True, conocidos, estadisticas, derivaciones

    while True:

        ronda += 1

        nuevos = set()

        hechos_ronda = sorted(conocidos)

        combinaciones_evaluadas = 0
        intentos_unificacion = 0
        combinaciones_validas = 0
        reglas_disparadas = 0

        for i, regla in enumerate(REGLAS, start=1):

            premisas, conclusion = renombrar(
                regla, f"{ronda}_{i}"
            )

            for combinacion in itertools.product(
                hechos_ronda,
                repeat=len(premisas)
            ):

                combinaciones_evaluadas += 1

                s = {}

                for premisa, hecho in zip(
                    premisas, combinacion
                ):

                    intentos_unificacion += 1

                    s = unificar(premisa, hecho, s)

                    if s is None:
                        break

                if s is not None:

                    combinaciones_validas += 1

                    nuevo = sustituir(conclusion, s)

                    if (
                        nuevo not in conocidos
                        and nuevo not in nuevos
                    ):

                        nuevos.add(nuevo)

                        reglas_disparadas += 1

                        derivaciones.append({
                            "Ronda": ronda,
                            "Regla": f"R{i}",
                            "Hecho": formato_termino(nuevo),
                            "Sustituciones": formato_sustitucion(s)
                        })

        # Registrar las estadísticas de la ronda
        estadisticas.append({
            "Ronda": ronda,
            "Hechos iniciales": len(hechos_ronda),
            "Combinaciones": combinaciones_evaluadas,
            "Intentos de unificación": intentos_unificacion,
            "Combinaciones válidas": combinaciones_validas,
            "Reglas disparadas": reglas_disparadas,
            "Hechos nuevos": len(nuevos),
            "Hechos acumulados": len(conocidos | nuevos)
        })

        if not nuevos:

            return (
                False,
                conocidos,
                estadisticas,
                derivaciones
            )

        conocidos.update(nuevos)

        if any(
            unificar(meta, h) is not None
            for h in nuevos
        ):

            return (
                True,
                conocidos,
                estadisticas,
                derivaciones
            )


def main():
    print("CINCO PRUEBAS DE UNIFICACIÓN")
    pruebas = [
        (
            ("Conoce", "Juan", "x"),
            ("Conoce", "Juan", "Juana")
        ),
        (
            ("Conoce", "Juan", "x"),
            ("Conoce", "y", "Isabel")
        ),
        (
            ("Conoce", "Juan", "x"),
            ("Conoce", "y", ("Madre", "y"))
        ),
        (
            ("Conoce", "Juan", "x"),
            ("Conoce", "x", "Isabel")
        ),
        (
            ("P", "x"),
            ("P", ("F", "x"))
        )
    ]
    # Verificación de los cinco ejercicios

    resultados_esperados = [
        {"x": "Juana"},
        {"y": "Juan", "x": "Isabel"},
        {"y": "Juan", "x": ("Madre", "Juan")},
        None,
        None
    ]

    for i, (a, b) in enumerate(pruebas):

        umg = unificar(a, b)

        # Comprobar el resultado esperado
        assert umg == resultados_esperados[i]

        # Si existe un UMG, verificar ambas expresiones
        if umg is not None:

            expresion_a = sustituir(a, umg)
            expresion_b = sustituir(b, umg)

            assert expresion_a == expresion_b

        print(f"Prueba {i + 1}: CORRECTA")

    print("\nLos cinco ejercicios fueron verificados.")
    for i, (a, b) in enumerate(pruebas, start=1):
        print(f"Prueba {i}: {formato_termino(a)} / {formato_termino(b)}")
        print("UMG:", formato_sustitucion(unificar(a, b)))

    print("\nHECHOS Y REGLAS")
    for hecho in sorted(HECHOS):
        print(formato_termino(hecho))
    for i, regla in enumerate(REGLAS, start=1):
        print(f"R{i}: {formato_regla(regla)}")

    for meta, esperado in [
        (("Criminal", "West"), True),
        (("Criminal", "w"), True),
        (("Criminal", "Nono"), False),
        (("Americano", "West"), True),
    ]:
        print()
        resultado = fol_fc_ask(HECHOS, meta)
        print(f"¿{formato_termino(meta)}? {resultado}")
        assert resultado is esperado

    resultado, finales, estadisticas, derivaciones = fol_fc_estadisticas(
        HECHOS, ("Criminal", "West")
    )
    print("\nESTADÍSTICAS POR RONDA")
    for ronda in estadisticas:
        print(ronda)
    print("\nESTADÍSTICAS TOTALES")
    for indicador in ("Combinaciones", "Intentos de unificación", "Combinaciones válidas", "Hechos nuevos", "Reglas disparadas"):
        print(f"{indicador}: {sum(r[indicador] for r in estadisticas)}")
    assert resultado is True
    assert len(HECHOS) == 4 and len(finales) == 8
    assert [r["Hechos nuevos"] for r in estadisticas] == [3, 1]
    assert [r["Combinaciones"] for r in estadisticas] == [280, 2464]
    assert [r["Intentos de unificación"] for r in estadisticas] == [348, 2870]
    assert sum(r["Combinaciones válidas"] for r in estadisticas) == 7
    assert ("Criminal", "West") in finales
    print("Todas las verificaciones fueron superadas.")


if __name__ == "__main__":
    main()
