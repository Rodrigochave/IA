# Problema del Puente y la Antorcha
# Estrategia óptima: siempre usar los dos más rápidos como "mensajeros"
# y en cada paso decidir la opción que minimiza el tiempo.

def cruzar_puente(tiempos):
    # Ordenamos los tiempos de menor a mayor
    tiempos.sort()
    pasos = []   # Aquí guardamos los movimientos
    total = 0    # Tiempo total

    # Mientras haya más de 3 personas en la orilla inicial
    while len(tiempos) > 3:
        a = tiempos[0]         # El más rápido
        b = tiempos[1]         # El segundo más rápido
        x = tiempos[-2]        # El penúltimo más lento
        y = tiempos[-1]        # El más lento

        # Estrategia 1: a y b cruzan, a regresa, x y y cruzan, b regresa
        tiempo_op1 = b + a + y + b

        # Estrategia 2: a y y cruzan, a regresa, a y x cruzan, a regresa
        tiempo_op2 = y + a + x + a

        # Elegimos la mejor estrategia
        if tiempo_op1 <= tiempo_op2:
            # Estrategia 1
            pasos.append(f"({a},{b}) -> {b}")
            pasos.append(f"{a} <- {a}")
            pasos.append(f"({x},{y}) -> {y}")
            pasos.append(f"{b} <- {b}")
            total += tiempo_op1
        else:
            # Estrategia 2
            pasos.append(f"({a},{y}) -> {y}")
            pasos.append(f"{a} <- {a}")
            pasos.append(f"({a},{x}) -> {x}")
            pasos.append(f"{a} <- {a}")
            total += tiempo_op2

        # Sacamos a los dos más lentos (ya cruzaron)
        tiempos = tiempos[:-2]

    # Casos finales (<=3 personas)
    if len(tiempos) == 3:
        a, b, c = tiempos
        pasos.append(f"({a},{b}) -> {b}")
        pasos.append(f"{a} <- {a}")
        pasos.append(f"({a},{c}) -> {c}")
        total += a + b + c
    elif len(tiempos) == 2:
        a, b = tiempos
        pasos.append(f"({a},{b}) -> {b}")
        total += b
    elif len(tiempos) == 1:
        pasos.append(f"{tiempos[0]} -> {tiempos[0]}")
        total += tiempos[0]

    return pasos, total


# ------------------- PROGRAMA PRINCIPAL -------------------
if __name__ == "__main__":
    n = int(input("Número de personas: "))
    tiempos = []
    print("Ingresa los tiempos de cruce:")
    for _ in range(n):
        tiempos.append(int(input()))

    pasos, total = cruzar_puente(tiempos)

    # Mostrar el recorrido
    print("\nRecorrido óptimo:")
    for p in pasos:
        print(p, end="; ")

    print(f"Total = {total}")
