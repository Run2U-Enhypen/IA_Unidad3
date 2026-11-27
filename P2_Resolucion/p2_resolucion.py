# Práctica 2. Demostración por resolución
# Inteligencia Artificial - Unidad 3
# Código extraído del Notebook de la práctica.


def neg(l):
    """Devuelve el literal complementario."""

    return l[1:] if l.startswith("~") else "~" + l


def es_tautologia(clausula):
    """Determina si una cláusula contiene literales complementarios."""

    return any(neg(l) in clausula for l in clausula)


def resolver(ci, cj):
    """Devuelve la lista de resolventes de dos cláusulas."""

    res = []

    # Recorrer los literales de la primera cláusula
    for l in sorted(ci):

        # Buscar el literal complementario
        if neg(l) in cj:

            # Eliminar los complementarios y unir
            nueva = (ci - {l}) | (cj - {neg(l)})

            # Descartar tautologías
            if not es_tautologia(nueva):

                # Evitar resolventes repetidos
                if nueva not in res:
                    res.append(nueva)

    return res


def formato_clausula(clausula):
    """Convierte una cláusula a una expresión lógica legible."""

    if not clausula:
        return "□"

    literales = [
        l.replace("~", "¬")
        for l in sorted(clausula)
    ]

    return " ∨ ".join(literales)


def pl_resolution(clausulas, meta_negada):
    """True si se deriva la cláusula vacía; False en caso contrario."""

    # Incorporar la KB y la meta negada sin duplicados
    C = list(dict.fromkeys(
        frozenset(c) for c in clausulas + meta_negada
    ))

    # Asignar un identificador a cada cláusula
    ids = {c: i for i, c in enumerate(C, start=1)}

    ronda = 0

    print("CLÁUSULAS INICIALES")
    print("-" * 55)

    for c in C:
        print(f"C{ids[c]}: {formato_clausula(c)}")

    # Comprobar si ya existe la cláusula vacía
    if frozenset() in ids:
        print("La KB inicial contiene la cláusula vacía.")
        return True

    while True:

        ronda += 1
        nuevas = []

        print(f"\nRONDA {ronda}")
        print("-" * 55)

        # Seleccionar todos los pares de cláusulas
        for i, a in enumerate(C):

            for b in C[i + 1:]:

                # Obtener los resolventes del par
                for r in resolver(a, b):

                    # Registrar únicamente cláusulas nuevas
                    if r not in ids:

                        ids[r] = len(ids) + 1
                        nuevas.append(r)

                        print(
                            f"C{ids[r]}: {formato_clausula(r)} "
                            f"(C{ids[a]}, C{ids[b]})"
                        )

                        # Si se obtiene la cláusula vacía
                        if not r:
                            print("\nCláusula vacía encontrada.")
                            return True

        # Si no se generaron nuevas cláusulas
        if not nuevas:
            print("\nNo se generaron nuevas cláusulas.")
            return False

        # Incorporar los resolventes a la KB
        C.extend(nuevas)


def pl_resolution_estadisticas(clausulas, meta_negada):
    """Ejecuta la resolución y registra estadísticas."""

    C = list(dict.fromkeys(
        frozenset(c) for c in clausulas + meta_negada
    ))

    conocidas = set(C)

    estadisticas = {
        "Cláusulas iniciales": len(C),
        "Rondas": 0,
        "Pares evaluados": 0,
        "Resolventes nuevos": 0,
        "Cláusulas totales": len(C),
        "Resultado": False
    }

    # Comprobar contradicción inicial
    if frozenset() in conocidas:
        estadisticas["Resultado"] = True
        return estadisticas

    while True:

        estadisticas["Rondas"] += 1

        nuevas = []

        for i, a in enumerate(C):

            for b in C[i + 1:]:

                estadisticas["Pares evaluados"] += 1

                for r in resolver(a, b):

                    if r not in conocidas:

                        conocidas.add(r)
                        nuevas.append(r)

                        estadisticas["Resolventes nuevos"] += 1
                        estadisticas["Cláusulas totales"] += 1

                        if not r:

                            estadisticas["Resultado"] = True

                            return estadisticas

        if not nuevas:
            return estadisticas

        C.extend(nuevas)


def pl_resolution_soporte(clausulas, meta_negada):
    """Resolución mediante conjunto de soporte."""

    C = list(dict.fromkeys(
        frozenset(c) for c in clausulas
    ))

    soporte = list(dict.fromkeys(
        frozenset(c) for c in meta_negada
    ))

    conocidas = set(C) | set(soporte)

    pares = 0
    resolventes = 0

    if frozenset() in conocidas:
        return True, pares, resolventes

    while soporte:

        # Extraer una cláusula del conjunto de soporte
        a = soporte.pop(0)

        for b in C:

            pares += 1

            for r in resolver(a, b):

                if r not in conocidas:

                    conocidas.add(r)
                    soporte.append(r)

                    resolventes += 1

                    print(
                        f"({formato_clausula(a)}) + "
                        f"({formato_clausula(b)}) "
                        f"-> {formato_clausula(r)}"
                    )

                    if not r:
                        return True, pares, resolventes

        # Incorporar la cláusula procesada
        if a not in C:
            C.append(a)

    return False, pares, resolventes


if __name__ == "__main__":
    # Base de conocimiento del ejercicio A
    kb_A = [
        {"~B11"},
        {"~B11", "P12", "P21"},
        {"~P12", "B11"},
        {"~P21", "B11"}
    ]

    # Negación de la meta
    meta_A = [{"P12"}]

    print("EJERCICIO A\n")

    resultado_A = pl_resolution(kb_A, meta_A)

    print("\nKB ⊨ ¬P12:", resultado_A)

    # Base de conocimiento del ejercicio B
    kb_B = [
        {"~P", "Q"},
        {"~Q", "R"},
        {"~R", "S"},
        {"P"}
    ]

    # Negación de la meta
    meta_B = [{"~S"}]

    print("EJERCICIO B\n")

    resultado_B = pl_resolution(kb_B, meta_B)

    print("\nKB ⊨ S:", resultado_B)

    # Base de conocimiento del ejercicio C
    kb_C = [
        {"P", "Q"},
        {"~P", "R"}
    ]

    # Negación de la meta
    meta_C = [{"~R"}]

    print("EJERCICIO C\n")

    resultado_C = pl_resolution(kb_C, meta_C)

    print("\nKB ⊨ R:", resultado_C)

    # Verificar los resultados de los tres ejercicios
    assert resultado_A is True, "Error en el ejercicio A"
    assert resultado_B is True, "Error en el ejercicio B"
    assert resultado_C is False, "Error en el ejercicio C"

    print("Ejercicio A: CORRECTO")
    print("Ejercicio B: CORRECTO")
    print("Ejercicio C: CORRECTO")

    print("\nTodas las pruebas fueron superadas.")

    print("EJERCICIO B: CONJUNTO DE SOPORTE\n")

    resultado_soporte, pares_soporte, resolventes_soporte = (
        pl_resolution_soporte(kb_B, meta_B)
    )

    print("\nResultado:", resultado_soporte)
    print("Pares evaluados:", pares_soporte)
    print("Resolventes nuevos:", resolventes_soporte)

    estadisticas_B = pl_resolution_estadisticas(kb_B, meta_B)

    reduccion_pares = (
        1 - pares_soporte / estadisticas_B["Pares evaluados"]
    ) * 100

    reduccion_resolventes = (
        1 - resolventes_soporte
        / estadisticas_B["Resolventes nuevos"]
    ) * 100

    print(f"Reducción de pares: {reduccion_pares:.2f}%")

    print(
        f"Reducción de resolventes: "
        f"{reduccion_resolventes:.2f}%"
    )
