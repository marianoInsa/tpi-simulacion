# generador_congruencial_mixtov2_optimizado.py

from functools import reduce, partial
import csv
import math
import random
import multiprocessing
import time

# --- Las funciones originales no necesitan cambios ---

def generador_nros_aleatorios(seed, a, c, m, n):
    """
    Genera una lista de números aleatorios utilizando el método congruencial mixto.
    """
    numeros_aleatorios = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        numeros_aleatorios.append(round(x / m, 4))
    return numeros_aleatorios

def generador_weekday(nros):
    """formula: 77*x+4"""
    return [math.floor(77 * x) + 4 for x in nros]

def generador_weekend(nros):
    """formula: 90x+18"""
    return [math.floor(90 * x) + 18 for x in nros]

# --- PASO 1: Crear una función "trabajadora" para un solo valor de 'p' ---
# Esta función contiene la lógica del bucle de simulaciones.
def simular_para_un_p(p, generador_var_al):
    """
    Realiza la simulación completa para un único valor de producción 'p'.
    Esta función será ejecutada en paralelo por diferentes procesos.
    """
    # Parámetros del generador (se pueden pasar como argumentos si es necesario)
    a = 16807
    c = 0
    m = 2**31 - 1
    n_dias = 30  # n es el número de días a simular por iteración

    # Parámetros del modelo de negocio
    precio_faltante = 3
    precio_sobrante = 7
    precio_venta = 10
    alpha = 0.05
    iteraciones = 100_000

    print(f"\nIniciando simulación con {iteraciones} iteraciones...")

    beneficios_obtenidos = []

    for _ in range(iteraciones):
        seed = random.randint(1, 10000)
        dias_demanda = generador_nros_aleatorios(seed, a, c, m, n_dias)
        unidades_demanda = generador_var_al(dias_demanda)

        unidades_sobrante = 0
        unidades_faltante = 0

        for d in unidades_demanda:
            if d < p:
                unidades_sobrante += p - d
            elif d > p:
                unidades_faltante += d - p
        
        unidades_d_total = sum(unidades_demanda)
        beneficio_ideal = unidades_d_total * precio_venta
        costo_f = unidades_faltante * precio_faltante
        costo_s = unidades_sobrante * precio_sobrante
        beneficio = beneficio_ideal - costo_f - costo_s
        beneficios_obtenidos.append(beneficio)

    # Calcular estadísticas finales para este 'p'
    length = len(beneficios_obtenidos)
    beneficio_prom = sum(beneficios_obtenidos) / length
    stddev = math.sqrt(sum((x - beneficio_prom) ** 2 for x in beneficios_obtenidos) / (length - 1))
    delta = stddev / math.sqrt(length * alpha)
    lower = beneficio_prom - delta
    upper = beneficio_prom + delta
    
    # Imprimir progreso para saber que algo está pasando
    print(f"Terminada la simulación para p={p}")

    # Retornar la fila de resultados para este 'p'
    return [p, beneficio_prom, stddev, delta, lower, upper]

# --- PASO 2: Crear una función que orquesta la ejecución en paralelo ---
def ejecutar_simulacion_paralela(produccion, generador_var_al, nombre_archivo):
    """
    Ejecuta las simulaciones en paralelo para una lista de valores de producción
    y guarda los resultados en un archivo CSV.
    """
    print(f"\nIniciando simulación para {nombre_archivo}")
    num_nucleos = multiprocessing.cpu_count()
    print(f"Utilizando {num_nucleos} núcleos de CPU.")

    # Usamos functools.partial para "fijar" los argumentos que no cambian en nuestra función trabajadora.
    # `pool.map` solo puede pasar un argumento iterable (los valores de 'p').
    funcion_trabajadora = partial(simular_para_un_p, generador_var_al=generador_var_al)

    # Creamos el pool de procesos
    with multiprocessing.Pool(processes=num_nucleos) as pool:
        # `pool.map` distribuye la lista 'produccion' entre los procesos disponibles
        # y ejecuta 'funcion_trabajadora' para cada elemento.
        resultados = pool.map(funcion_trabajadora, produccion)

    # --- Escribir todos los resultados en el archivo CSV de una vez ---
    with open(nombre_archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['p', 'beneficio_prom', 'stddev', 'delta', 'lower', 'upper'])
        writer.writerows(resultados) # Escribe todas las filas de golpe

    print(f"Simulación completada. Resultados guardados en {nombre_archivo}")

def main():
    inicio_total = time.time()
    
    # Para una prueba rápida, puedes reducir el número de iteraciones:
    # iteraciones_simulacion = 10_000 

    # --- Simulación para Weekday ---
    #produccion_weekday = [x for x in range(4, 82)]
    # produccion_weekday = [x for x in range(22, 31)] # Para pruebas
    #ejecutar_simulacion_paralela(produccion_weekday, iteraciones=iteraciones_simulacion, 
                                 #generador_var_al=generador_weekday, nombre_archivo='resultados_weekday.csv')

    # --- Simulación para Weekend ---
    produccion_weekend = [x*6 for x in range(1,19)]
    # produccion_weekend = [x for x in range(41, 48)] # Para pruebas
    ejecutar_simulacion_paralela(produccion_weekend, 
                                 generador_var_al=generador_weekend, nombre_archivo='resultados_weekend.csv')

    fin_total = time.time()
    print(f"\nTodas las simulaciones terminaron en {(fin_total - inicio_total) / 60:.2f} minutos.")

if __name__ == "__main__":
    main()
