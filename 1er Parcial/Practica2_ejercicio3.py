'''Empleando recocido simulado, crea un programa que optimice la función de Himmelblau(benchmark).
-El sistema comienza con una “temperatura” alta que permite aceptar soluciones incluso peores que la actual (esto ayuda a escapar de mínimos locales).
-Conforme la temperatura baja (enfriamiento controlado), el algoritmo se vuelve más estricto y sólo acepta mejoras o cambios muy cercanos, estabilizándose 
alrededor de un mínimo.
-Su objetivo: encontrar el mínimo global de una función, evitando quedarse atrapado en mínimos locales.'''
import math
import random

# Función de Himmelblau, toma dos variables x y y
def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Función de recocido simulado con criterio de Boltzmann
def simulated_annealing(x0, y0, T=1000, T_min=1e-6, alpha=0.95, steps_per_T=100):
    """
    x0, y0: punto inicial aleatorio.
    T: temperatura inicial (empezamos “calientes”).
    T_min: temperatura mínima (criterio de parada).
    alpha: factor de enfriamiento (qué tan rápido baja la temperatura).
    steps_per_T: intentos de movimiento en cada temperatura."""
    # Estado inicial
    estado_actual = (x0, y0)
    valor_actual = himmelblau(*estado_actual)
    mejor_estado = estado_actual
    mejor_valor = valor_actual
    
    # Mientras la temperatura sea mayor a T_min
    while T > T_min:
        for _ in range(steps_per_T):
            # Generar estado vecino (movimiento pequeño)
            x_new = estado_actual[0] + random.uniform(-0.5, 0.5)
            y_new = estado_actual[1] + random.uniform(-0.5, 0.5)
            estado_nuevo = (x_new, y_new)
            valor_nuevo = himmelblau(*estado_nuevo)
            '''Se crea un estado vecino moviéndose un poco en x y y (entre -0.5 y 0.5).
            Se evalúa Himmelblau en ese punto → valor_nuevo.'''
            delta = valor_nuevo - valor_actual
            '''Si delta < 0, el nuevo estado es mejor.
            Si delta > 0, el nuevo estado es peor.'''
            # Criterio de aceptación (Boltzmann)
            if delta < 0:
                estado_actual, valor_actual = estado_nuevo, valor_nuevo
            else:
                p = math.exp(-delta / T)
                if random.random() < p:
                    estado_actual, valor_actual = estado_nuevo, valor_nuevo
            '''Si el nuevo estado es mejor → lo aceptamos siempre.
            Si es peor → lo aceptamos con criterio de descenso de boltzmann
            random.random() genera un número entre [0,1].
            Si es menor que p, aceptamos el cambio.
            Esto permite “subir” a estados peores al inicio, evitando caer en mínimos locales.'''
            # Actualizar mejor solución encontrada
            if valor_actual < mejor_valor:
                mejor_estado, mejor_valor = estado_actual, valor_actual
            '''Guardamos el mejor estado encontrado hasta ahora.'''
        # Enfriar la temperatura
        T *= alpha
    
    return mejor_estado, mejor_valor


# Ejemplo: varias corridas para encontrar mínimos
if __name__ == "__main__":
    resultados = []
    for i in range(5):
        x0 = random.uniform(-6, 6)
        y0 = random.uniform(-6, 6)
        estado, valor = simulated_annealing(x0, y0)
        resultados.append((estado, valor))
        print(f"Run {i+1}: x={estado[0]:.4f}, y={estado[1]:.4f}, f={valor:.6f}")
'''Se obtienen al menos uno de los cuatro minimos globales.
    (3.0,2.0)
    (-2.805,3.131)
    (-3.779,-3.283)
    (3.584,-1.848)'''

