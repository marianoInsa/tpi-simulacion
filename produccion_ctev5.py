# generador_congruencial_mixtov2_optimizado.py

from functools import partial
import csv
import math
import multiprocessing
import time
from simulador import generar_numeros_aprobados
from scipy.stats import t 
from datetime import date, timedelta
# --- Las funciones originales no necesitan cambios ---

def generador_weekday(n_dias):
    nros = generar_numeros_aprobados(n_dias)
    """formula: 77*x+4"""
    return [math.floor(77 * x) + 4 for x in nros]

def generador_weekend(n_dias):
    nros = generar_numeros_aprobados(n_dias)
    """formula: 90x+18"""
    return [math.floor(90 * x) + 18 for x in nros]

def count_weekend_days_in_next_30():
    today = date(2025,7,6)
    weekend_days = 0

    for i in range(30):
        current_day = today + timedelta(days=i)
        if current_day.weekday() in (4, 5, 6):  # Friday=4, Saturday=5, Sunday=6
            weekend_days += 1

    return weekend_days

# --- PASO 1: Crear una función "trabajadora" para un solo valor de 'p' ---
# Esta función contiene la lógica del bucle de simulaciones.
def simular_para_un_p(p, iteraciones, generador_var_al):
    """
    Realiza la simulación completa para un único valor de producción 'p'.
    Esta función será ejecutada en paralelo por diferentes procesos.
    """
    # Parámetros del generador (se pueden pasar como argumentos si es necesario)

    n_dias = 30  # n es el número de días a simular por iteración
    n_dias = 30 - count_weekend_days_in_next_30()

    # Parámetros del modelo de negocio
    precio_faltante = 10
    precio_sobrante = 7
    precio_venta = 10
    alpha = 0.05

    beneficios_obtenidos = []

    for _ in range(iteraciones):
        unidades_demanda = generador_var_al(n_dias)

        unidades_sobrante = 0
        unidades_faltante = 0
        unidades_venta = 0

        for d in unidades_demanda:
            if d < p:
                unidades_sobrante += p - d
                unidades_venta += d
            else:
                unidades_faltante += d - p
                unidades_venta += p
        
        ventas = unidades_venta * precio_venta
        costo_f = unidades_faltante * precio_faltante
        costo_s = unidades_sobrante * precio_sobrante
        beneficio = ventas - costo_f - costo_s
        beneficios_obtenidos.append(beneficio)

    # Calcular estadísticas finales para este 'p'
    length = len(beneficios_obtenidos)
    beneficio_prom = sum(beneficios_obtenidos) / length
    stddev = math.sqrt(sum((x - beneficio_prom) ** 2 for x in beneficios_obtenidos) / (length - 1))
    t_critical = t.ppf(1 - alpha / 2, df=length - 1)
    delta = t_critical * (stddev / math.sqrt(length))
    lower = beneficio_prom - delta
    upper = beneficio_prom + delta
    
    # Imprimir progreso para saber que algo está pasando
    print(f"Terminada la simulación para p={p}")

    # Retornar la fila de resultados para este 'p'
    return [p, beneficio_prom, stddev, delta, lower, upper]

# --- PASO 2: Crear una función que orquesta la ejecución en paralelo ---
def ejecutar_simulacion_paralela(produccion, iteraciones, generador_var_al, nombre_archivo):
    """
    Ejecuta las simulaciones en paralelo para una lista de valores de producción
    y guarda los resultados en un archivo CSV.
    """
    print(f"\nIniciando simulación para {nombre_archivo} con {iteraciones} iteraciones...")
    num_nucleos = multiprocessing.cpu_count()
    print(f"Utilizando {num_nucleos} núcleos de CPU.")

    # Usamos functools.partial para "fijar" los argumentos que no cambian en nuestra función trabajadora.
    # `pool.map` solo puede pasar un argumento iterable (los valores de 'p').
    funcion_trabajadora = partial(simular_para_un_p, iteraciones=iteraciones, generador_var_al=generador_var_al)

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
    
    # Para la simulación real con 10 millones de iteraciones:
    iteraciones_simulacion = 10_000
    
    # Para una prueba rápida, puedes reducir el número de iteraciones:
    # iteraciones_simulacion = 10_000 

    # --- Simulación para Weekday ---
    #produccion_weekday = [x for x in range(4, 82)]
    # produccion_weekday = [x for x in range(22, 31)] # Para pruebas
    #ejecutar_simulacion_paralela(produccion_weekday, iteraciones=iteraciones_simulacion, 
                                 #generador_var_al=generador_weekday, nombre_archivo='resultados_weekday.csv')

    # --- Simulación para Weekend ---
    # produccion_weekend = [x*6 for x in range(1,19)]
    produccion_weekday = [x*6 for x in range(1,13)]
    # produccion_weekend = [x for x in range(41, 48)] # Para pruebas
    ejecutar_simulacion_paralela(produccion_weekday, iteraciones=iteraciones_simulacion, 
                                 generador_var_al=generador_weekday, nombre_archivo='resultados_weekend.csv')

    fin_total = time.time()
    print(f"\nTodas las simulaciones terminaron en {(fin_total - inicio_total) / 60:.2f} minutos.")

if __name__ == "__main__":
    main()
