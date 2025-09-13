import math
import random

# Función de Himmelblau
def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Función de recocido simulado con criterio de Boltzmann
def simulated_annealing(x0, y0, T=1000, T_min=1e-6, alpha=0.95, steps_per_T=100):
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
            
            delta = valor_nuevo - valor_actual
            
            # Criterio de aceptación (Boltzmann)
            if delta < 0:
                estado_actual, valor_actual = estado_nuevo, valor_nuevo
            else:
                p = math.exp(-delta / T)
                if random.random() < p:
                    estado_actual, valor_actual = estado_nuevo, valor_nuevo
            
            # Actualizar mejor solución encontrada
            if valor_actual < mejor_valor:
                mejor_estado, mejor_valor = estado_actual, valor_actual
        
        # Enfriar la temperatura
        T *= alpha
    
    return mejor_estado, mejor_valor


# Ejemplo: varias corridas para encontrar mínimos
if __name__ == "__main__":
    resultados = []
    for i in range(10):
        x0 = random.uniform(-6, 6)
        y0 = random.uniform(-6, 6)
        estado, valor = simulated_annealing(x0, y0)
        resultados.append((estado, valor))
        print(f"Run {i+1}: x={estado[0]:.4f}, y={estado[1]:.4f}, f={valor:.6f}")
