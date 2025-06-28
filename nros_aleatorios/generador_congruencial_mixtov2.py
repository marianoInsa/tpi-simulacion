# Generador de números aleatorios
# Descripción: Este script implementa un generador de números aleatorios utilizando el método congruencial mixto.
from functools import reduce
import csv
import math
import random

def generador_nros_aleatorios(seed, a, c, m, n):
    """
    Genera una lista de números aleatorios utilizando el método congruencial mixto.
    
    Parámetros:
    seed (int): Semilla inicial.
      - Rango: Cualquier entero entre 0 y m-1
      - Recomendación: Usar un valor que sea primo relativo con m (no tengan factores comunes)
    a (int): Multiplicador.
      - Rango: 0 < a < m
      - Condiciones óptimas:
        - a mod 4 = 1 si m es potencia de 2
        - a debe ser relativamente grande
    c (int): Incremento.
      - Rango: 0 ≤ c < m
      - Condiciones óptimas:
        - c debe ser primo relativo con m (no tienen factores comunes)
        - Si c = 0, es un generador multiplicativo puro (requiere otras condiciones)
        - Si c ≠ 0, es un generador mixto
    m (int): Módulo.
      - Rango: m > 0, preferiblemente grande
      - Recomendación: Usar una potencia de 2 (2³¹-1 o 2⁴⁸) o un número primo grande
      - El valor de m determina el período máximo posible
    n (int): Cantidad de números aleatorios a generar.
    
    Retorna:
    list: Lista de números aleatorios generados.
    """
    
    numeros_aleatorios = []
    x = seed
    
    for _ in range(n):
        x = (a * x + c) % m
        
        numeros_aleatorios.append(round(x / m, 4))
    
    return numeros_aleatorios

# Crear un archivo csv y almacenar los números aleatorios generados
def guardar_nros_aleatorios_en_csv(numeros_aleatorios, nombre_archivo):
    """
    Guarda una lista de números aleatorios en un archivo CSV.
    
    Parámetros:
    numeros_aleatorios (list): Lista de números aleatorios.
    nombre_archivo (str): Nombre del archivo CSV donde se guardarán los números.
    """
    
    with open(nombre_archivo, 'w') as f:
        for numero in numeros_aleatorios:
            f.write(f"{numero}\n")

def generador_weekday(nros):
    """formula: 77*x+4
    va entre 4 y 81
    """
    return [math.floor(77 * x) + 4 for x in nros]

def generador_weekend(nros):
    """formula: 90x+18
    va entre 18 y 108
    """
    return [math.floor(90 * x) + 18 for x in nros]

def iterate(produccion,iteraciones, generador_var_al):
    
    with open('resultados.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write CSV header
        writer.writerow([
            'p',
            'beneficio_prom',
            'stddev',
            'delta',
            'lower',
            'upper',
        ])

        # Parámetros del generador
        a = 16807
        c = 0
        m = 2**31 - 1
        n = 100
        
        # Generar números aleatorios
        # falta verificar si pasan los tests


        precio_faltante = 3
        precio_sobrante = 7
        precio_venta = 10

        alpha = 0.1

        for p in produccion:

            mylist = []

            for _ in range (iteraciones):
                seed = random.randint(1,10000) 
                dias_demanda = generador_nros_aleatorios(seed, a, c, m, n)
                unidades_demanda = generador_var_al(dias_demanda)

                # acumuladores en 0
                unidades_sobrante = 0
                unidades_faltante = 0

                for d in unidades_demanda: 
                    if d < p:
                        unidades_sobrante += p - d
                    elif d > p:
                        unidades_faltante += d - p

                # acumular unidades
                unidades_d = reduce(lambda x, y: x+y, unidades_demanda)

                beneficio_ideal = unidades_d * precio_venta

                costo_f = unidades_faltante * precio_faltante
                costo_s = unidades_sobrante * precio_sobrante

                beneficio = beneficio_ideal - costo_f - costo_s 

                mylist.append(beneficio)


            length = len(mylist)
            beneficio_prom = sum(mylist) / length
            stddev = math.sqrt(sum((x - beneficio_prom) ** 2 for x in mylist) / (length - 1))

            # === STEP 3: Apply confidence interval formula ===
            delta = stddev / math.sqrt(length * alpha)
            lower = beneficio_prom - delta
            upper = beneficio_prom + delta

            writer.writerow([
                        p,
                        beneficio_prom,
                        stddev,
                        delta,
                        lower,
                        upper,
                    ])

        print("terminaron las ", iteraciones, " iteraciones")


def main():


    produccion_weekday = [x for x in range(4, 82)]
    # produccion_weekday = [x for x in range(22, 31)]
    produccion_weekend = [x for x in range(41, 48)]
    iterate(produccion_weekend, iteraciones=10_000_000, generador_var_al=generador_weekend)
    iterate(produccion_weekday, iteraciones=10_000_000, generador_var_al=generador_weekday)

                 




if __name__ == "__main__":
    main()

